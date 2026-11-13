# JavaScript 逆向学习路线

课程按能力组织，站点名称和旧版本案例不作为工具可用性的保证。

| 阶段 | 需要掌握 | 对应资源 |
|---|---|---|
| 工程准备 | Windows 路径、PowerShell、UTF-8、Git、包管理器、依赖锁、退出码 | Python、Node、Git 与各项目 README |
| JS 语义 | 类型转换、闭包、提升、TDZ、this、箭头函数、严格模式 | js-runtime-semantics |
| 对象和字节 | 原型、描述符、Proxy/Reflect、品牌检查、Buffer、TypedArray、端序、BigInt | js-runtime-semantics |
| 异步与模块 | CJS/ESM、动态 import、Promise、async/await、任务与微任务、取消、Worker | js-runtime-semantics |
| 浏览器和 HTTP | DOM、事件传播、Cookie、同源/CORS、重定向、缓存、Content-Type | DevTools、Playwright、mitmproxy/whistle |
| 请求取证 | Network、Initiator、调用栈、断点、HAR、source map、WebSocket 帧 | js-browser-evidence、websocat |
| 编码和密码 | UTF-8/UTF-16、Hex/Base64/Base64url、摘要、MAC、加密、签名、密钥格式 | js-crypto-interop、sm-crypto、forge、CyberChef |
| Hook | 接收者、参数、返回值、异常、时序、描述符恢复、跨 realm | js-browser-evidence、jshookmcp |
| 混淆与打包 | 压缩/转译/打包/混淆的区别、webpack runtime/chunk、ESM 输出 | webcrack、javascript-obfuscator |
| AST | parser/traverse/types/generator、scope/binding、副作用、短路、顺序和异常 | js-ast-validation、Babel、AST Explorer |
| 环境差异 | 对象、DOM、存储、调度、随机值与时钟的基准对照 | js-environment-diff、jsdom、sdenv |
| 图像与交互 | 切片重组、像素/CSS 坐标、缩放、识别误差、事件与协议的区别 | Canvas、自建页面、ddddocr |
| WASM 与传输 | import/export、线性内存、JS 桥接、TLS/ALPN/HTTP 分层 | js-wasm-boundary、WABT、curl_cffi |
| 验证与交付 | 原始散列、版本、最小样本、预期结果、失败反例、已验证范围 | 各技能的交付要求与本地测试 |

## 常见误区

- 对象传参仍是按值传递；修改对象和重新给形参赋值不同。
- `const` 不会冻结对象；修改 `prototype.constructor` 不会替换构造函数本体。
- Hex/Base64 是编码，摘要与 HMAC 也不等于可逆加密。算法名称不足以描述模式、填充、KDF 和序列化。
- eval/Function 是动态执行机制；改变 toString 外观不会把函数变成引擎原生函数。
- DOM 实现、JavaScript 引擎、完整浏览器和系统隔离是不同层次。补 window 不会改变 TLS 指纹。
- 未引用的绑定仍可能有初始化副作用；AST 输出能解析不代表变换保持语义。
- 图像识别成功、本地参数一致、HTTP 成功状态和服务端业务完成分别验证。

语言查询使用 [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)，AST API 使用 [Babel 文档](https://babeljs.io/docs/babel-traverse)，浏览器取证使用 [DevTools Network](https://developer.chrome.com/docs/devtools/network/reference)。
