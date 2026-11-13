"""Fetch pinned upstream sources and materialize only the selected core skills.

No dependencies are installed and no downloaded program is executed.
Default invocation lists resources. Python 3.10+ and Git are required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OMIT = {".git", ".claude", ".claude-plugin", ".agents", "node_modules", "__pycache__"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def inside(path: Path, parent: Path) -> Path:
    resolved = path.resolve()
    resolved.relative_to(parent.resolve())
    return resolved


def git(directory: Path | None, *arguments: str) -> str:
    command = ["git"]
    if directory is not None:
        command.extend(["-C", str(directory)])
    command.extend(arguments)
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                            errors="strict", env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Git command failed")
    return result.stdout.strip()


def source_checkout(root: Path, source: dict) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9._-]+", source["id"]):
        raise ValueError("Invalid source ID")
    if not re.fullmatch(r"[0-9a-f]{40}", source["commit"]):
        raise ValueError("Sources must use a full commit SHA")
    repository = source["repository"]
    if not repository.startswith(("https://github.com/", "file://")):
        raise ValueError("Expected a public GitHub URL or a local test repository")
    cache = inside(root / ".cache/upstream" / (source["id"] + "-" + source["commit"]), root)
    if cache.exists():
        if not (cache / ".git").is_dir():
            raise RuntimeError(f"Existing cache is not a checkout: {cache}")
        if git(cache, "remote", "get-url", "origin").removesuffix(".git") != repository.removesuffix(".git"):
            raise RuntimeError("Existing checkout has a different origin")
        if git(cache, "rev-parse", "HEAD") != source["commit"]:
            raise RuntimeError("Existing checkout is incomplete or points to a different commit")
        if git(cache, "status", "--porcelain"):
            raise RuntimeError(f"Existing checkout has local changes; preserved: {cache}")
        return cache
    cache.parent.mkdir(parents=True, exist_ok=True)
    git(None, "-c", "http.version=HTTP/1.1", "clone", "--depth", "1", "--no-checkout",
        "--filter=blob:none", "--no-tags", repository, str(cache))
    git(cache, "-c", "http.version=HTTP/1.1", "fetch", "--depth", "1", "origin", source["commit"])
    git(cache, "checkout", "--detach", source["commit"])
    if git(cache, "rev-parse", "HEAD") != source["commit"]:
        raise RuntimeError("Fetched commit mismatch")
    return cache


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def materialize_skill(root: Path, skill: dict, source: dict, checkout: Path) -> Path:
    name = skill["name"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Invalid skill name")
    relative = PurePosixPath(skill["source_path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Skill source must stay inside the upstream checkout")
    skill_root = inside(checkout / str(relative), checkout)
    prefix = skill_root.relative_to(checkout).as_posix()
    prefix = "" if prefix == "." else prefix + "/"
    tracked = [item for item in git(checkout, "ls-files", "-z").split("\0") if item]
    selected = [item[len(prefix):] for item in tracked if item.startswith(prefix)]
    nested = [PurePosixPath(item).parent for item in selected
              if PurePosixPath(item).name.lower() == "skill.md" and item != "SKILL.md"]
    files: dict[str, Path] = {}
    for item in selected:
        rel = PurePosixPath(item)
        if any(part in OMIT for part in rel.parts):
            continue
        if any(parent == rel or parent in rel.parents for parent in nested):
            continue
        origin = inside(skill_root / item, checkout)
        if origin.is_symlink():
            raise RuntimeError(f"Symlink requires manual handling: {item}")
        if origin.is_file():
            files[item] = origin
    if "SKILL.md" not in files:
        raise RuntimeError("Selected skill has no SKILL.md")
    for license_name in source.get("license_files", []):
        license_path = inside(checkout / license_name, checkout)
        if license_path.is_file() and license_path not in files.values():
            files["UPSTREAM-" + Path(license_name).name] = license_path
    provenance = {"name": name, "repository": source["repository"], "commit": source["commit"],
                  "source_path": skill["source_path"],
                  "files": {rel: sha256(path) for rel, path in sorted(files.items())}}
    destination = inside(root / skill["path"], root / "downloaded-skills")
    if destination.exists():
        marker = destination / "_SOURCE.json"
        if not marker.is_file() or read_json(marker) != provenance:
            raise RuntimeError(f"Different export already exists; preserved: {destination}")
        for rel, digest in provenance["files"].items():
            existing = inside(destination / rel, destination)
            if not existing.is_file() or sha256(existing) != digest:
                raise RuntimeError(f"Export has local changes; preserved: {existing}")
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".staging-" + name + "-", dir=destination.parent))
    for rel, original in files.items():
        target = inside(staging / rel, staging)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, target)
    (staging / "_SOURCE.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")
    inside(staging, destination.parent)
    staging.rename(destination)
    return destination


def load_catalog(root: Path):
    sources = read_json(root / "catalog/sources.lock.json")["sources"]
    skills = read_json(root / "catalog/skills.json")["skills"]
    tools = read_json(root / "catalog/tools.json")["tools"]
    if len({source["id"] for source in sources}) != len(sources):
        raise ValueError("Duplicate source IDs")
    by_id = {source["id"]: source for source in sources}
    for item in [*tools, *(skill for skill in skills if skill["kind"] == "upstream")]:
        if item["source_id"] not in by_id:
            raise ValueError("Unknown upstream source")
    return by_id, skills, tools


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", action="store_true", help="fetch and export the 16 upstream skills")
    parser.add_argument("--tools", action="store_true", help="fetch all selected tool source repositories")
    parser.add_argument("--tool", action="append", default=[], help="fetch one named tool; repeatable")
    args = parser.parse_args()
    sources, skills, tools = load_catalog(ROOT)
    selected_tools = tools if args.tools else [tool for tool in tools if tool["name"] in args.tool]
    unknown = set(args.tool) - {tool["name"] for tool in tools}
    if unknown:
        parser.error("Unknown tool: " + ", ".join(sorted(unknown)))
    if not args.skills and not selected_tools:
        print("Skills:", ", ".join(skill["name"] for skill in skills))
        print("Tools:", ", ".join(tool["name"] for tool in tools))
        print("Listing only. Use --skills, --tool NAME, or --tools to download sources.")
        return
    exports = [skill for skill in skills if args.skills and skill["kind"] == "upstream"]
    needed = {item["source_id"] for item in [*exports, *selected_tools]}
    checkouts = {}
    for source_id in sorted(needed):
        print("Fetching", source_id, sources[source_id]["commit"][:12], flush=True)
        checkouts[source_id] = source_checkout(ROOT, sources[source_id])
    for skill in exports:
        destination = materialize_skill(ROOT, skill, sources[skill["source_id"]], checkouts[skill["source_id"]])
        print("Skill ready:", destination.relative_to(ROOT), flush=True)
    for tool in selected_tools:
        print("Tool source:", tool["name"], checkouts[tool["source_id"]].relative_to(ROOT))
    print("Sources ready. Dependencies, submodules, models, browsers and builds were not installed.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        print("ERROR:", error, file=sys.stderr)
        sys.exit(1)
