---
name: js-environment-diff
description: 用浏览器基准与本地样本对照定位 JavaScript 宿主环境差异，并实现任务所需的最小 DOM、存储、描述符或异步兼容层。用于补环境和运行结果不一致排查，不将 QuickJS、V8、DOM 库或 TLS 客户端视为同一种环境。
---

# JavaScript 环境差异定位

记录原始样本、浏览器和本地运行时版本、入口、输入、输出及外部状态。先建立基准，再修补第一个能解释输出差异的环境点；不要按一长串全局对象清单盲目造值。

## 分层检查

| 层次 | 需要比较的内容 |
|---|---|
| 引擎语义 | ECMAScript 特性、realm、错误类型、浮点/BigInt、栈与函数行为 |
| 对象模型 | 属性存在性、自有/继承、descriptor、enumerability、prototype、brand check、identity |
| 浏览器宿主 | document/location/navigator、URL 解析、DOM 集合与节点关系、事件对象 |
| 状态 | Cookie 的作用域/属性、Storage、IndexedDB、缓存、页面初始化顺序 |
| 调度 | Promise 微任务、timer、事件监听、Worker 消息、异步资源完成顺序 |
| 传输 | HTTP headers、TLS/ALPN/HTTP2 等；此层通常不由补 window 解决 |

`window = globalThis` 只增加一个别名，不能建立 Window 原型链和浏览器行为。空函数返回 undefined、伪造固定长度或提前 resolve Promise 都可能掩盖真实依赖。

## 实施

1. 优先使用能满足任务的现有运行时；浏览器、jsdom/happy-dom、isolated-vm、QuickJS 各自缺失的宿主能力分别列出。
2. 用相同探针收集两个环境的结果，保存可比较的快照；避免 getter 执行或代理本身污染观察。
3. 对差异写最小兼容实现和反例，保留真实异常、接收者及描述符约束；包装日志避免重复代理。
4. 随机数、时钟、网络等作为显式依赖；固定值仅用于标明的可重复测试，不写成目标环境真实值。
5. 验证入口结果与事件顺序；移除不必要的宽泛 stub。无浏览器基准时，只能报告本地兼容假设。

DOM 库不提供完整渲染、字体、Canvas/WebGL 或网络指纹一致性。单独的 V8 isolate 也不自动提供应用安全；具体隔离和暴露的宿主能力按执行对象选择。参考 [Node vm 的边界说明](https://nodejs.org/api/vm.html) 和所用运行时的上游文档。

交付差异表、最小补丁、基准与本地输入输出、适用版本、未覆盖 API。只报告实际验证的样本，不将本地输出一致扩大为服务端验证通过。
