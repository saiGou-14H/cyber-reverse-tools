# Cyber Reverse Tools

面向 JavaScript 逆向学习与已授权分析的精简资源集合：**22 项核心技能、21 个主线工具**，按能力分类并锁定上游版本。

仓库直接包含 6 个本地方法论 skill。其余 16 个第三方 skill 和 21 个工具通过清单按需拉取；保留上游来源和许可文件，不在本仓库重复托管第三方代码。下载只是准备源码，不代表依赖、模型、浏览器或 MCP 服务已经安装运行。

## 快速使用

需要 Python 3.10+ 和 Git。各工具的 Node、Python、编译器要求以锁定版本的上游说明为准。

```powershell
git clone https://github.com/saiGou-14H/cyber-reverse-tools.git
cd cyber-reverse-tools

# 只列出可选技能和工具
python scripts/fetch_resources.py

# 拉取 16 个上游 skill，与仓库内 6 个组成 core-22
python scripts/fetch_resources.py --skills

# 按需拉取工具，也可以重复指定 --tool
python scripts/fetch_resources.py --tool webcrack --tool jshookmcp

# 确实需要全部主线工具时
python scripts/fetch_resources.py --tools
```

源码位于 `.cache/upstream/`，已导出的第三方技能位于 `downloaded-skills/`。这两个目录不会提交到 Git。已有内容发生变化时脚本会停止并保留现场，不执行 reset 或覆盖。

## 分类索引

- [22 项技能能力与来源](docs/SKILLS.md)：JavaScript 12、Android/native 8、浏览器 2。
- [21 个工具能力与用途](docs/TOOLS.md)：AST、调试、浏览器、环境、密码、网络、图像和 WASM。
- [学习路线与课程补充](docs/LEARNING_PATH.md)：异步、字节编码、协议、source map、AST 验证和 WASM。
- [DSH 安装说明](docs/DSH.md)：仅安装 core-22，保留已有内容。
- [第三方来源与许可记录](THIRD_PARTY.md)。

## 目录结构

```text
catalog/
  skills.json           22 项技能与精确来源目录
  tools.json            21 个主线工具
  sources.lock.json     27 个去重上游的完整 commit SHA
skills/                 6 个本地方法论 skill
scripts/                拉取与 DSH 安装脚本
docs/                   能力说明、学习路线和安装说明
tests/                  本地合成仓库与安装场景测试
```

22 项是精简后的核心集合。上游维护、发版、漏洞公告处理、内部 CI 等入口不进入技能清单；历史站点案例、重复工具备选和本机操作备份不在发布范围内。

## 验证

```powershell
python -m unittest discover -s tests -v
```

测试使用临时目录和本地 Git 仓库，不访问真实目标网站，不写入当前机器的 DSH 配置。它们验证拉取版本、技能导出、白名单、内容保留和路径边界；不证明第三方工具能运行或适配某个网站。
