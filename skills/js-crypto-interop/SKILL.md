---
name: js-crypto-interop
description: 对照 JavaScript、Node、Web Crypto 和 Python 的编码及密码协议输入输出，定位字节、模式、填充、密钥格式和序列化差异。用于已提供算法或样本的互操作验证，不根据密文外观断言算法或密钥。
---

# 编码与密码协议互操作

从已提供的调用代码或已授权采样取得参数，建立输入到输出的分层记录。先验证编码，再验证算法；不要连续试换算法掩盖字节不一致。

## 参数清单

| 层次 | 必须明确 |
|---|---|
| 消息 | 字段顺序、缺省值、空值、换行、Unicode 规范化、URL 编码、JSON 序列化 |
| 字节 | 文本编码、Hex/Base64/Base64url、是否去 padding、大小端、实际字节长度 |
| 对称算法 | 算法与 key 长度、mode、padding、IV/nonce、AAD、tag 长度及拼接位置 |
| 派生 | 原始 key 还是 passphrase；KDF、salt、迭代次数、摘要、派生长度 |
| RSA/签名 | PEM/DER/JWK、PKCS#1/SPKI/PKCS#8、加密或签名填充、OAEP hash/MGF/label、PSS saltLength |
| 国密 | SM2 密文分段次序/编码、用户标识/摘要约定、签名编码；SM4 mode、IV、padding |

区分编码、摘要、MAC、签名和加密。HMAC 不是普通 SHA，也不是公钥数字签名。MD5/SHA/SM3 的摘要不能称为解密。

CryptoJS 的字符串 passphrase API 与显式 WordArray key API 分开处理；记录 WordArray 的 sigBytes。`Salted__` 等格式线索只能形成假设，必须用调用链和参数确认。

## 验证

1. 用自建数据或脱敏后的固定向量复现第一层输入字节，输出长度与 hex。
2. 在原实现和另一实现中逐层对照，定位第一个差异；将随机性、时钟和外部状态作为显式输入。
3. 对带随机填充、nonce 或 salt 的算法，验证解密/验签和结构约束，不要求不同运行的密文必然一致。固定随机值只用于标明的测试向量。
4. 至少覆盖 ASCII、非 ASCII、空值和边界长度；错误密钥、标签或签名应出现预期失败。

优先复用项目已有库。新增依赖按目标环境锁定版本；CryptoJS 用于旧实现兼容，现代 API 能力查 [Node crypto](https://nodejs.org/api/crypto.html) 和 [Web Crypto](https://nodejs.org/api/webcrypto.html)。不把某个库有算法名当作支持全部格式和模式。

交付参数表、最小复现、可公开的输入输出向量、差异位置和验证范围；使用虚构密钥，不在日志或报告中保存真实凭据。
