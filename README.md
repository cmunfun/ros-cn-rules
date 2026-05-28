# ros-cn-rules

本仓库用于生成 MikroTik RouterOS 可导入的 `CN` IPv4 地址列表，供 RB5009 的 `/ip firewall address-list` 使用。

## 数据来源

数据来源为 MetaCubeX 的 CN GeoIP 列表：

```text
https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.list
```

## 生成方式

GitHub Actions 定时拉取上游 `cn.list`，通过 Python 脚本提取 IPv4 CIDR，合并可聚合网段，然后生成 RouterOS 可导入的 `CN.rsc` 文件。

生成格式示例：

```routeros
/ip firewall address-list
add list=CN address=1.1.8.0/24 comment="CN MetaCubeX"
add list=CN address=1.2.4.0/24 comment="CN MetaCubeX"
```

RouterOS 实际匹配的是 `list=CN`，`comment="CN MetaCubeX"` 只是备注，不影响路由或防火墙规则。

## 下载链接

Raw：

```text
https://raw.githubusercontent.com/cmunfun/ros-cn-rules/main/CN.rsc
```

jsDelivr：

```text
https://cdn.jsdelivr.net/gh/cmunfun/ros-cn-rules/CN.rsc
```

jsDelivr 指定 main 分支：

```text
https://cdn.jsdelivr.net/gh/cmunfun/ros-cn-rules@main/CN.rsc
```

Fastly jsDelivr：

```text
https://fastly.jsdelivr.net/gh/cmunfun/ros-cn-rules/CN.rsc
```

GCore jsDelivr：

```text
https://gcore.jsdelivr.net/gh/cmunfun/ros-cn-rules/CN.rsc
```

TestingCF jsDelivr：

```text
https://testingcf.jsdelivr.net/gh/cmunfun/ros-cn-rules/CN.rsc
```

## 另一种数据源（未使用）
```text
https://www.iwik.org/ipcountry/mikrotik/CN
```
