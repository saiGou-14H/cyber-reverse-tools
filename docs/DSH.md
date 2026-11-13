# DSH 安装 core-22

先安装 DSH 及其 `@dhicoc/dsh-reverse-skill` 插件。此仓库只管理 core-22 扩展目录，不安装插件本身，也不改动它原有的技能。

```powershell
# 先补齐 16 个第三方技能
python scripts/fetch_resources.py --skills

# 默认只预览
python scripts/install_dsh_skills.py

# 确认计划后安装白名单内缺失项
python scripts/install_dsh_skills.py --apply
```

默认插件位置为当前用户主目录下的 `.dsh/profiles/web/node_modules/@dhicoc/dsh-reverse-skill`。其他安装位置使用：

```powershell
python scripts/install_dsh_skills.py --package-dir "你的插件目录"
python scripts/install_dsh_skills.py --package-dir "你的插件目录" --apply
```

安装器会检查目标 package.json 中的包名，只向 `skills/_ext/` 补齐清单内缺失的目录。已有目录与本地修改保持原样。出现重名、来源缺失、路径越界、嵌套技能或白名单外的现有目录时停止，不删除或覆盖这些内容。

如果之前加载过维护/发版等非核心技能，应先把它们备份到插件扫描根目录以外。仅改名为 `skills/_disabled` 无法阻止递归扫描。此发布版不提供整包删除命令。

安装完成后，重新加载插件或重启 DSH 刷新运行中的目录缓存。22 是这个扩展集的数量；整个平台的总技能数取决于原有技能和其他 provider，不保证固定为 110。

技能说明与工具依赖是两层内容。拉取或安装 skill 不会构建 jshook CLI、安装 iv8、下载浏览器、写入 API 密钥或注册 MCP 服务。需要执行相关任务时，再按上游说明准备环境。
