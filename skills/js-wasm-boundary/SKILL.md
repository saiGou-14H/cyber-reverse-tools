---
name: js-wasm-boundary
description: 检查 JavaScript 与 WebAssembly 的调用边界，整理模块、导入导出、线性内存和输入输出编码，并用已授权样本做对照。用于 JS AST 无法覆盖的 WASM 计算定位，不自动扩大为任意虚拟机的完整反编译。
---

# JavaScript 与 WASM 边界

先从 JS 加载代码确认模块来自 URL、内联字节、缓存还是动态生成，并记录原始 wasm 的散列、加载顺序和 JS wrapper。不要把压缩数据或自定义字节码仅凭后缀认成 WASM。

## 静态检查

- 对可信文件可用 WABT 的 `wasm-validate`、`wasm-objdump`、`wasm2wat` 检查格式、段、导入导出和函数关系；先核对本地二进制版本与帮助，工具不在环境中时报告这一点。
- 区分 WASM 的模块指令与模块内部自定义 VM；WAT 文本不等于恢复了原始高级语言。
- 记录 import module/name/signature、memory/table、start function、数据段、导出入口；使用本机支持的 WASM 特性解析。

## 边界复现

1. 在用户授权的执行环境里观察 JS wrapper 调用，包括编码、分配、指针/长度、返回值和释放逻辑。
2. 记录内存字节的偏移、长度、端序、字符串终止方式；memory.grow 后旧视图可能失效，重新获取视图。
3. 区分 i32/i64/f32/f64 与 JS number/BigInt 的桥接；不要在 JSON 中静默损失 i64 精度。
4. 若需要离线调用，逐个实现已观察到的 imports，保留调用顺序和错误行为；不要把全部 import 都 stub 成零。
5. 用固定且可公开的输入比较浏览器边界记录和本地输出，并包含边界长度或失败样例。

WASM 文件格式本身不保证宿主安全；实际能力由暴露的 imports 和执行环境决定。不向未知模块提供文件、网络或真实密钥，仅为任务需要暴露最小接口。

交付模块散列、JS 到导出的映射、import 清单、内存布局观察、最小 harness 和结果差异。[WABT 上游](https://github.com/WebAssembly/wabt) 是工具入口；缺少证据的内部逻辑明确保留为未解析。
