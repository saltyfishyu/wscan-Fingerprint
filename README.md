# wscan-Fingerprint
wscan自用指纹库

自己写的资产探测扫描器使用的指纹库，用的goby的指纹格式，因此将其他的指纹库都转为goby格式了。
```
指纹库:
  - Goby
  - FingerprintHub
  - EHole
  - Dismap

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
