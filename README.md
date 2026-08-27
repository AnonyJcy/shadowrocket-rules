# Shadowrocket-Rules

本项目自动每日同步上游 [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) 的全部规则，并自动移除 `tun-excluded-routes` 与 `skip-proxy` 中对 `10.0.0.0/8` 私网段的强制内核级旁路，以便在开启分流/去广告的同时兼容自建虚拟内网与隧道。

---

## 🚀 规则订阅链接列表

在 Shadowrocket（小火箭）中进入 **配置** -> 右上角 **`+`** -> 粘贴以下任一链接并下载使用：

| 规则名称 | 规则描述 | 订阅链接 (Raw) |
| :--- | :--- | :--- |
| **lazy.conf** | 懒人配置（无策略组，推荐） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/lazy.conf` |
| **lazy_group.conf** | 懒人配置（带策略组） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/lazy_group.conf` |
| **sr_ad_only.conf** | 仅广告拦截 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_ad_only.conf` |
| **sr_adb.conf** | 广告与行为拦截 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_adb.conf` |
| **sr_backcn.conf** | 回国模式 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_backcn.conf` |
| **sr_backcn_ad.conf** | 回国模式 + 去广告 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_backcn_ad.conf` |
| **sr_cnip.conf** | 国内 IP 直连 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_cnip.conf` |
| **sr_cnip_ad.conf** | 国内 IP 直连 + 去广告 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_cnip_ad.conf` |
| **sr_direct_banad.conf** | 直连模式 + 去广告 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_direct_banad.conf` |
| **sr_proxy_banad.conf** | 全局代理 + 去广告 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_proxy_banad.conf` |
| **sr_top500_banlist.conf** | Top500 常用黑名单 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_banlist.conf` |
| **sr_top500_banlist_ad.conf** | Top500 黑名单 + 去广告 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_banlist_ad.conf` |
| **sr_top500_whitelist.conf** | Top500 白名单 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_whitelist.conf` |
| **sr_top500_whitelist_ad.conf** | Top500 白名单 + 去广告 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_whitelist_ad.conf` |

---

## ⚙️ 自动化构建机制

- **每日定时同步**：由 GitHub Actions 于每天 08:30 (UTC 00:30) 自动从上游 `release` 分支拉取最新文件并重新应用补丁。
- **纯净修补**：仅移除阻碍内网调度的 `10.0.0.0/8` 旁路限制，不修改、不注入任何其他规则。
