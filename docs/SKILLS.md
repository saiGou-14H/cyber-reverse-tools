# 核心 Skills

core-22 共 22 项。仅 6 项本地技能直接随仓库提供；其余 16 项运行 `python scripts/fetch_resources.py --skills` 后出现在 `downloaded-skills/`。

| Skill | 分组 | 能力 | 获取方式与入口 |
|---|---|---|---|
| jshook-reverse | JavaScript | CDP 调试、Hook 和 JS 代码分析；运行 CLI 前需构建并配置依赖。 | [锁定上游入口](https://github.com/wuji66dde/jshook-skill/tree/ffbd3e87c4e3f4631a51b45393a919216f38a2ba//SKILL.md) |
| js-reverse-ops | JavaScript | 按定位、运行观测、恢复和复核组织 JS 分析任务。 | [锁定上游入口](https://github.com/DQmyth/js-reverse-ops/tree/fa399b93a55fe2ba5da09ec46ef0c7072d7bd6cf//SKILL.md) |
| ruishu-reverse | JavaScript | 特定瑞数实现的 Cookie 与 URL 参数分析方法，按目标版本验证。 | [锁定上游入口](https://github.com/waterbili/ruishu-re/tree/97ec3d4ab208694c454a5ec69b9f3bacfe34c75d/agentskill/SKILL.md) |
| iv8-env-runtime | JavaScript | 基于 iv8 的宿主环境重建和本地执行，依赖指定运行时。 | [锁定上游入口](https://github.com/zhizhuodemao/ai-reverse-resources/tree/ef143189c160eac4f2b55921c586a5e38611b015/plugins/js-reverse-plugin/skills/iv8-env-runtime/SKILL.md) |
| iv8-jsvmp-recovery | JavaScript | iv8 工作流中的 JSVMP 分析与边界恢复。 | [锁定上游入口](https://github.com/zhizhuodemao/ai-reverse-resources/tree/ef143189c160eac4f2b55921c586a5e38611b015/plugins/js-reverse-plugin/skills/iv8-jsvmp-recovery/SKILL.md) |
| js-ast-deobfuscation | JavaScript | 基于源码证据的 AST 反混淆与可读性分析。 | [锁定上游入口](https://github.com/zhizhuodemao/ai-reverse-resources/tree/ef143189c160eac4f2b55921c586a5e38611b015/plugins/js-reverse-plugin/skills/js-ast-deobfuscation/SKILL.md) |
| js-ast-validation | JavaScript | 分析并验证 JavaScript AST 变换、反混淆与 bundle 抽取，区分阅读视图和可执行等价产物。用于 Babel visitor、作用域重命名、常量折叠、控制流和模块依赖检查，不承诺恢复作者原名或自动还原任意 VM。 | [本地 SKILL.md](../skills/js-ast-validation/SKILL.md) |
| js-browser-evidence | JavaScript | 对用户提供的网页、HAR 或脚本建立请求到 JavaScript 调用链的可复核证据，使用 DevTools、现有浏览器工具或已连接 CDP 服务进行定位与小范围 Hook。用于浏览器 JS 观察和调试，不等同于 Android Frida 或验证码通过服务。 | [本地 SKILL.md](../skills/js-browser-evidence/SKILL.md) |
| js-crypto-interop | JavaScript | 对照 JavaScript、Node、Web Crypto 和 Python 的编码及密码协议输入输出，定位字节、模式、填充、密钥格式和序列化差异。用于已提供算法或样本的互操作验证，不根据密文外观断言算法或密钥。 | [本地 SKILL.md](../skills/js-crypto-interop/SKILL.md) |
| js-environment-diff | JavaScript | 用浏览器基准与本地样本对照定位 JavaScript 宿主环境差异，并实现任务所需的最小 DOM、存储、描述符或异步兼容层。用于补环境和运行结果不一致排查，不将 QuickJS、V8、DOM 库或 TLS 客户端视为同一种环境。 | [本地 SKILL.md](../skills/js-environment-diff/SKILL.md) |
| js-runtime-semantics | JavaScript | 分析 JavaScript 逆向中的语言语义差异并制作最小可运行示例，涵盖类型转换、闭包、this、原型、描述符、二进制数据和异步顺序。用于基础练习、跨 Node 与浏览器行为比较；不用于站点参数破解或完整环境模拟。 | [本地 SKILL.md](../skills/js-runtime-semantics/SKILL.md) |
| js-wasm-boundary | JavaScript | 检查 JavaScript 与 WebAssembly 的调用边界，整理模块、导入导出、线性内存和输入输出编码，并用已授权样本做对照。用于 JS AST 无法覆盖的 WASM 计算定位，不自动扩大为任意虚拟机的完整反编译。 | [本地 SKILL.md](../skills/js-wasm-boundary/SKILL.md) |
| android-reverse-engineering | Android/native | Android APK、smali、组件及动态分析工作流。 | [锁定上游入口](https://github.com/SimoneAvogadro/android-reverse-engineering-skill/tree/0c7cf89830993df7dfc178498f69952262808bea/plugins/android-reverse-engineering/skills/android-reverse-engineering/SKILL.md) |
| rev-dex-dumper | Android/native | Android DEX 运行时提取与分析辅助。 | [锁定上游入口](https://github.com/P4nda0s/reverse-skills/tree/a2baa31c58a3567977188414da68c8c842057152/skills/rev-dex-dumper/SKILL.md) |
| rev-frida | Android/native | 移动端及原生程序 Frida 动态观测。 | [锁定上游入口](https://github.com/P4nda0s/reverse-skills/tree/a2baa31c58a3567977188414da68c8c842057152/skills/rev-frida/SKILL.md) |
| rev-idapython | Android/native | IDA Python 分析与自动化。 | [锁定上游入口](https://github.com/P4nda0s/reverse-skills/tree/a2baa31c58a3567977188414da68c8c842057152/skills/rev-idapython/SKILL.md) |
| rev-struct | Android/native | 原生程序结构体识别与恢复。 | [锁定上游入口](https://github.com/P4nda0s/reverse-skills/tree/a2baa31c58a3567977188414da68c8c842057152/skills/rev-struct/SKILL.md) |
| rev-symbol | Android/native | 原生程序符号识别与恢复。 | [锁定上游入口](https://github.com/P4nda0s/reverse-skills/tree/a2baa31c58a3567977188414da68c8c842057152/skills/rev-symbol/SKILL.md) |
| rev-u3d-dump | Android/native | Unity 资源或程序结构提取与分析。 | [锁定上游入口](https://github.com/P4nda0s/reverse-skills/tree/a2baa31c58a3567977188414da68c8c842057152/skills/rev-u3d-dump/SKILL.md) |
| rev-unicorn-debug | Android/native | 基于 Unicorn 的模拟执行与调试。 | [锁定上游入口](https://github.com/P4nda0s/reverse-skills/tree/a2baa31c58a3567977188414da68c8c842057152/skills/rev-unicorn-debug/SKILL.md) |
| playwright-cli | Browser | 通过 Playwright CLI 操作浏览器并进行页面检查。 | [锁定上游入口](https://github.com/microsoft/playwright/tree/8534271f0413bae6a455b7cf43b2637391bc614b/packages/playwright-core/src/tools/skills/playwright-cli/SKILL.md) |
| playwright-trace | Browser | 查看 Playwright trace 中的动作、网络、日志与页面快照。 | [锁定上游入口](https://github.com/microsoft/playwright/tree/8534271f0413bae6a455b7cf43b2637391bc614b/packages/playwright-core/src/tools/skills/playwright-trace/SKILL.md) |

每个入口都有独立前提。jshook-reverse 的 CLI 需要构建与相关配置；iv8 两项依赖指定运行时。读取技能文件不代表其工具已安装。

js-reverse-ops、jshook-reverse 与 AST/环境工作流有能力交集，按当前任务选择入口；不要把来源文档中的历史授权或默认路线当成当前用户授权。
