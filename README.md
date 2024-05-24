![](https://socialify.git.ci/saltyfishyu/wscan-Fingerprint/image?font=Raleway&language=1&name=1&owner=1&pattern=Formal%20Invitation&stargazers=1&theme=Dark)

# wscan-Fingerprint
wscan自用指纹库

自己写的资产探测扫描器使用的指纹库，用的goby的指纹格式，因此将其他的指纹库都转为goby格式了。
```
指纹数量:  11569

指纹库:
  - Goby 2022/9/5
  - FingerprintHub  2024/01/26
  - EHole 2023/12/14
  - Dismap 2023/12/14

指纹详情:
  - title_contains       标题中包含
  - body_contains        HTTP响应包中包含
  - protocol_contains    协议中包含
  - banner_contains      响应包中包含 包括HTTP以及TCP等
  - header_contains      HTTP响应头中包含
  - server_contains      HTTP响应头中Server值包含
  - cert_contains        证书包含
  - port_contains        端口包含
  - favicon_hash_is      网站图标ico的hash
``` 

因为是不同的指纹库合并的，可能存在同时命中几个规则的情况，已经在几个指纹库合并的时候去重过一次，还是有部分残留，不过不影响使用。

#### *欢迎推荐指纹库以及提供新版本指纹库*
