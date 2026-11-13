"""Install the core-22 profile into a DSH plugin, preserving existing directories.

Default is a read-only plan. Fetch upstream skills first, then pass --apply.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def skill_name(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---", text, re.S)
    if not frontmatter:
        return None
    match = re.search(r"^name:\s*(.+)$", frontmatter.group(1), re.M)
    return match.group(1).strip().strip("\"'") if match else None


def inside(path: Path, parent: Path):
    resolved = path.resolve()
    resolved.relative_to(parent.resolve())
    return resolved


def prepare(root: Path, destination: Path, skills: list[dict]):
    if len({item["name"] for item in skills}) != len(skills):
        raise ValueError("Duplicate skill names in profile")
    expected = {item["name"] for item in skills}
    installed = {}
    if destination.exists():
        for entry in destination.iterdir():
            if entry.is_symlink() or getattr(entry, "is_junction", lambda: False)():
                raise ValueError("Linked destination requires manual review")
            if entry.is_dir():
                manifest = entry / "SKILL.md"
                if not manifest.is_file() or skill_name(manifest) != entry.name:
                    raise ValueError("Existing destination does not contain a matching skill: " + entry.name)
                installed[entry.name] = entry
    extra = set(installed) - expected
    if extra:
        raise ValueError("Non-profile entries preserved; archive them outside DSH scan roots first: " +
                         ", ".join(sorted(extra)))
    plan = []
    for skill in skills:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill["name"]):
            raise ValueError("Invalid skill name")
        source = inside(root / skill["path"], root)
        if not (source / "SKILL.md").is_file():
            raise ValueError("Source missing; run fetch_resources.py --skills first: " + skill["name"])
        if skill_name(source / "SKILL.md") != skill["name"]:
            raise ValueError("Source skill name mismatch")
        if len(list(source.rglob("SKILL.md"))) != 1:
            raise ValueError("Nested skill entries must not be installed together")
        for path in source.rglob("*"):
            inside(path, source)
            if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                raise ValueError("Linked source requires manual review")
        target = inside(destination / skill["name"], destination)
        plan.append({"name": skill["name"], "source": source, "target": target,
                     "action": "preserve" if skill["name"] in installed else "install"})
    return plan


def install(root: Path, destination: Path, skills: list[dict], apply: bool):
    plan = prepare(root, destination, skills)
    if apply:
        destination.mkdir(parents=True, exist_ok=True)
        for item in plan:
            if item["action"] == "install":
                shutil.copytree(item["source"], item["target"])
        records = [{"name": skill["name"], "source": skill["path"], "kind": skill["kind"]}
                   for skill in sorted(skills, key=lambda value: value["name"])]
        text = json.dumps({"profile": "core-22", "skills": records}, ensure_ascii=False, indent=2) + "\n"
        manifest = destination / "_MANIFEST.json"
        if not manifest.exists() or manifest.read_text(encoding="utf-8-sig") != text:
            temporary = destination / "_MANIFEST.json.tmp"
            temporary.write_text(text, encoding="utf-8")
            os.replace(temporary, manifest)
    return [{"name": item["name"], "action": item["action"]} for item in plan]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--package-dir", type=Path, help="installed @dhicoc/dsh-reverse-skill directory")
    args = parser.parse_args()
    package = args.package_dir or Path.home() / ".dsh/profiles/web/node_modules/@dhicoc/dsh-reverse-skill"
    if not (package / "package.json").is_file():
        raise ValueError("DSH plugin not found; specify --package-dir")
    package_info = json.loads((package / "package.json").read_text(encoding="utf-8-sig"))
    if package_info.get("name") != "@dhicoc/dsh-reverse-skill":
        raise ValueError("Destination is not the expected DSH plugin")
    destination = inside(package / "skills/_ext", package)
    skills = json.loads((ROOT / "catalog/skills.json").read_text(encoding="utf-8"))["skills"]
    plan = install(ROOT, destination, skills, args.apply)
    print(json.dumps({"applied": args.apply, "skills": plan}, ensure_ascii=False, indent=2))
    if args.apply:
        print("Reload the DSH plugin or restart DSH to refresh its cached catalog.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print("ERROR:", error, file=sys.stderr)
        sys.exit(1)
