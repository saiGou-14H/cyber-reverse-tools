---
name: js-browser-evidence
description: 对用户提供的网页、HAR 或脚本建立请求到 JavaScript 调用链的可复核证据，使用 DevTools、现有浏览器工具或已连接 CDP 服务进行定位与小范围 Hook。用于浏览器 JS 观察和调试，不等同于 Android Frida 或验证码通过服务。
---

# 浏览器 JavaScript 证据定位

以用户指定页面或离线材料为范围，先记录目标请求、触发动作和期望观察的字段。区分静态推断、实际调用和服务端结果。

## 路径选择

- 已有 HAR/源码时先离线读材料；需要浏览器证据时使用当前环境实际提供的浏览器控制接口。
- 不假设 jshookmcp、js-reverse、Playwright 或调试端口已经存在。已连接服务先发现工具与 schema；源码目录不代表服务已接入。
- 浏览器请求使用 Network/Initiator/XHR 或 fetch 断点回到调用栈；iframe、Worker、Service Worker 需记录具体 target/realm。
- WebSocket 记录握手和每条帧的方向、类型、时间、编码；不能把 HTTP 200 或 WebSocket 101 当成业务完成。

## 最小采样

1. 保留触发前后请求样本、脚本来源、版本/散列和时间；区分业务响应、重定向、挑战页、缓存及错误页。
2. 沿调用栈定位目标值实际生成与传递处，记录源位置、函数实参与返回值。动态源码保存为独立派生文件。
3. 需要 Hook 时只包裹有关边界，保留接收者、参数顺序、返回值、异常和 Promise 语义。记录原描述符并在结束时恢复。
4. 用有/无 Hook 的同一组本地动作比较，检查是否出现递归、重复代理、时序变化或对象身份改变。
5. 将输入、输出和外部状态交给后续算法或环境工作流；缺少证据时说明具体缺哪个事件或样本。

`Function.prototype.toString` 外观不是原生性证明。不要因为存在 Proxy handler 就假定所有对象操作已被拦截；需要识别提前缓存的函数引用、其他 realm 和不可配置属性。

HAR、请求头和脚本日志可能包含会话材料；报告用脱敏副本。需要产生真实提交时沿用当前任务授权范围；仅观察请求不会自动授权额外业务操作。

交付请求/脚本定位表、带上下文的调用链、最小采样记录、Hook 的恢复方式、已验证与未验证结论。[DevTools Network 参考](https://developer.chrome.com/docs/devtools/network/reference) 提供具体操作入口。
