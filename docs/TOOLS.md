# 主线工具

所有条目均为按需拉取的上游源码。单项命令为 `python scripts/fetch_resources.py --tool 名称`；不会自动安装依赖或执行程序。

| 工具 | 分类 | 能力与边界 | 锁定来源 |
|---|---|---|---|
| babel | AST与反混淆 | parser、traverse、types、generator 等语法与 AST 工具链；完整 monorepo 源码。 | [上游](https://github.com/babel/babel/tree/44a7bb02c0a7f8a6f96fb9560d7df855a2366644) |
| astexplorer | AST与反混淆 | 可视化不同 parser 的 AST，辅助编写和验证最小 visitor。 | [上游](https://github.com/fkling/astexplorer/tree/8888701e97c2efebe6fb118484e67cfc0077d08c) |
| webcrack | AST与反混淆 | JS 反混淆、展开压缩与 webpack/browserify 模块抽取；基于实际输入验证支持范围。 | [上游](https://github.com/j4k0xb/webcrack/tree/c80eec5f00622b86cea871d68349750ce950201f) |
| source-map | AST与反混淆 | 读取与生成 source map，进行生成代码和原始源码位置映射。 | [上游](https://github.com/mozilla/source-map/tree/8c668f3dd3916e96d06131dec97c78a3e62bd0f3) |
| javascript-obfuscator | AST与反混淆 | 生成字符串数组、控制流等混淆样本，用于原理学习和本地变换回归。 | [上游](https://github.com/javascript-obfuscator/javascript-obfuscator/tree/4db5ea3da717f8a4b1aafee6a8fabaeab1804659) |
| jshookmcp | JSHook与CDP | 浏览器控制、CDP、Hook、网络和 JS 分析工具集合；须满足 Node 要求、构建并接入客户端后才可调用。 | [上游](https://github.com/vmoranv/jshookmcp/tree/5ecd198c67358b8e4a0d9ccbd30285d124bc37eb) |
| mitmproxy | 抓包与代理 | 可编程交互式代理、流量检查与插件处理；源码下载不包含系统代理/证书配置。 | [上游](https://github.com/mitmproxy/mitmproxy/tree/af5d15709bd09d1eb80bf88064540787f6c3e27e) |
| whistle | 抓包与代理 | Node HTTP/HTTPS/WebSocket 调试代理、规则改写与本地 mock。 | [上游](https://github.com/avwo/whistle/tree/b962b8a3b3753557d92dae6a61ec8a7c082b5296) |
| websocat | 抓包与代理 | 命令行 WebSocket 与数据流桥接工具，用于文本和二进制帧实验。 | [上游](https://github.com/vi/websocat/tree/734de478c6175fe15004dba07d31e8ce85d1bca9) |
| playwright | 浏览器自动化 | 浏览器自动化、上下文、网络观测和 Trace 调试的官方源码；浏览器二进制需独立安装。 | [上游](https://github.com/microsoft/playwright/tree/8534271f0413bae6a455b7cf43b2637391bc614b) |
| puppeteer | 浏览器自动化 | 浏览器控制和 DevTools 协议相关 API 官方源码；需匹配浏览器与运行环境。 | [上游](https://github.com/puppeteer/puppeteer/tree/a2465981c2618a829cd27b3cdfe046b3e5d0fc19) |
| jsdom | JS引擎与DOM环境 | 在 Node 中实现部分 Web 标准的 DOM/HTML 环境；不提供完整浏览器渲染。 | [上游](https://github.com/jsdom/jsdom/tree/b76da26fd3b2786771b493f0bbec8dbd7a3d36d0) |
| sdenv | 补环境 | 浏览器对象和宿主 API 的兼容实现与示例；用真实浏览器基线验证所需部分。 | [上游](https://github.com/pysunday/sdenv/tree/9a0f2a75369ba256550c637fa1f4c67f2aaec911) |
| isolated-vm | JS引擎与DOM环境 | 提供独立 V8 isolate；维护模式，集成方式影响安全，不等于完整浏览器或系统隔离。 | [上游](https://github.com/laverdet/isolated-vm/tree/d180c5539e2d889d6e1048256b162156af6b1ad2) |
| sm-crypto | 国密与加密 | JavaScript SM2/SM3/SM4 实现；不与 gm-crypto 的 API 或默认参数混用。 | [上游](https://github.com/JuneAndGreen/sm-crypto/tree/24d38a724aae939597657dcd3f6612e0e2c2d2f2) |
| forge | 国密与加密 | node-forge 的密钥、证书、ASN.1、RSA/AES 等能力，用于格式和协议互操作。 | [上游](https://github.com/digitalbazaar/forge/tree/01119d67bf65e7898717501ff6417bed9cc37233) |
| CyberChef | 国密与加密 | 编码、压缩、密码和数据格式操作的可视化配方工具；本地构建后使用。 | [上游](https://github.com/gchq/CyberChef/tree/d4d96c6c3d2597fef836d81bfc04617d97c681a5) |
| curl_cffi | TLS指纹 | 基于 curl 的 Python HTTP 客户端及浏览器配置；不是运行 JavaScript 的浏览器。 | [上游](https://github.com/lexiforest/curl_cffi/tree/78301ad1ce8bb042a451ffdb05d3037ac9fa2ed1) |
| ddddocr | 验证码与滑块 | 字符识别、检测与滑块相关图像能力；算法、模型和输入形式分别验证。 | [上游](https://github.com/sml2h3/ddddocr/tree/c40f56f95412e10bcb9bd0bd24411e92f896d238) |
| wabt | WASM与二进制 | wasm2wat、wasm-objdump、wasm-validate 等 WebAssembly 格式、反汇编和验证工具。 | [上游](https://github.com/WebAssembly/wabt/tree/4fbd7198c766e3d450edfe3847ff6f45f360e078) |
| frida-skeleton | 移动端与Frida | Android Java/native Frida Hook 工程模板与辅助封装。 | [上游](https://github.com/Margular/frida-skeleton/tree/82db1b25bd7134cd5917cc95628d057ae28e48a0) |

按任务选用：浏览器观测先建立 DevTools 基线；AST 学习使用 Babel/AST Explorer；反混淆和模块抽取按输入选择 webcrack；环境模拟以真实浏览器结果为对照。

下载目录保留 Git 元数据，脚本校验完整 commit SHA。需要子模块、额外模型、浏览器二进制、原生编译工具链或服务接入时，遵循该版本上游说明；这些内容不会由本集合自动安装。
