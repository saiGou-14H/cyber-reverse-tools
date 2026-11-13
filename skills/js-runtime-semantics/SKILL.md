---
name: js-runtime-semantics
description: 分析 JavaScript 逆向中的语言语义差异并制作最小可运行示例，涵盖类型转换、闭包、this、原型、描述符、二进制数据和异步顺序。用于基础练习、跨 Node 与浏览器行为比较；不用于站点参数破解或完整环境模拟。
---

# JavaScript 语义核验

先确定代码运行位置：普通浏览器脚本、ESM、Node CommonJS、Worker 或其他 realm；记录版本、严格模式和输入。相同源码在不同宿主中的结果不能直接互推。

围绕用户遇到的现象缩小代码，先给出预测，再运行可信的最小示例，比较实际值、类型、异常与执行顺序。保留可以解释差异的最小反例。

## 判断要点

- 对象传参也是按值传递；区分修改同一个对象与给形参赋新值。不要用“对象按引用传参”解释全部行为。
- `const` 限制绑定重赋值，不冻结对象；闭包捕获绑定而不是某次值的快照。
- 普通函数的 this 与调用方式有关；箭头函数捕获外层 this。分别验证 strict/non-strict，不假设顶层 this 总是 window。
- `constructor` 属性与构造函数实际身份分开；原型链、实例自身属性和描述符分别观察。
- getter、Proxy trap、Symbol.toPrimitive 可能产生副作用；读取属性不总是纯操作。
- JS number 的位运算通常转到 32 位整数；BigInt、浮点数、JSON 数字、Python 整数不能无条件互换。
- UTF-16 code unit、Unicode code point、UTF-8 字节长度分别记录。使用 Buffer/TypedArray/DataView 时明确 byteOffset、byteLength 与端序。
- Promise/async 的微任务和定时器任务分开记录；Node 的调度细节不能直接代替浏览器事件循环。
- JSON 往返不是通用深拷贝；检查 BigInt、undefined、循环引用、Date、Map/Set 和原型丢失。

## 交付

给出最小源码、执行命令/宿主、实际输出、语义解释及一个容易混淆的反例。只执行自建或已审查的样例；未知目标脚本需要与宿主文件和凭据隔离。不要为演示改全局运行时配置。

查语义时使用 [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)，按用户运行版本核对宿主 API。
