# Shadowrocket-Rules (Dual-Track: Standard & WireGuard Enhanced)

[中文](#-中文文档) | [English](#-english-documentation)

---

## 🇨🇳 中文文档

> 🚀 **双轨全自动同步 [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) 去广告与分流规则，同时提供「官方纯净标准版」与「WireGuard / 内网穿透增强版」。**

### 💡 为什么提供双轨版本？ (Why Dual-Track)

1. **标准官方原版（Standard）**：
   - 适合已在路由器 / 软路由部署了内核级 WireGuard、Tailscale 或本身处于校园网/内网环境的场景。
   - 保持官方纯净规则，不注入任何特定内网网段 TUN 路由，10.0.0.0/8 默认走内网直连/旁路。
2. **WireGuard 内网穿透增强版（`wg_` 前缀）**：
   - 适合在 iOS / iPadOS 上使用蜂窝网络或普通 Wi-Fi 时，通过小火箭自建 WireGuard 节点连接远端内网的场景。
   - **解决的核心痛点**：修复 Termius、ServerBox、Blink 等第三方非 Web 客户端发起原始 POSIX raw TCP Socket 连接 `10.10.0.0/24` 时被 iOS 物理网卡抢占导致超时（errno=110）的问题。
   - **技术补丁**：自动在 `[General]` 注入 `tun-included-routes = 10.10.0.0/24`，并清理旁路拦截，在 `[Rule]` 预埋分流占位规则。
3. **独立文件名不冲突**：
   - 两套配置采用不同的文件名发布（如 `lazy.conf` vs `wg_lazy.conf`），在 Shadowrocket 中可同时订阅共存，切换 Wi-Fi/蜂窝场景一键无缝切换，绝不相互覆盖。

---

### 📋 1. 标准官方纯净规则（适合校园网/路由器已连 WireGuard 环境）

| 规则名称 | 规则特性 | 订阅链接 (Raw) |
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
| **sr_top500_whitelist.conf** | Top500 常用白名单 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_whitelist.conf` |
| **sr_top500_whitelist_ad.conf** | Top500 白名单 + 去广告 | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_whitelist_ad.conf` |

---

### 📋 2. WireGuard / 内网穿透增强规则（`wg_` 前缀，适合蜂窝/移动网络）

| 规则名称 | 规则特性 | 订阅链接 (Raw) |
| :--- | :--- | :--- |
| **wg_lazy.conf** | 懒人配置（无策略组，WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_lazy.conf` |
| **wg_lazy_group.conf** | 懒人配置（带策略组，WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_lazy_group.conf` |
| **wg_sr_ad_only.conf** | 仅广告拦截（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_ad_only.conf` |
| **wg_sr_adb.conf** | 广告与行为拦截（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_adb.conf` |
| **wg_sr_backcn.conf** | 回国模式（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_backcn.conf` |
| **wg_sr_backcn_ad.conf** | 回国模式 + 去广告（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_backcn_ad.conf` |
| **wg_sr_cnip.conf** | 国内 IP 直连（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_cnip.conf` |
| **wg_sr_cnip_ad.conf** | 国内 IP 直连 + 去广告（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_cnip_ad.conf` |
| **wg_sr_direct_banad.conf** | 直连模式 + 去广告（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_direct_banad.conf` |
| **wg_sr_proxy_banad.conf** | 全局代理 + 去广告（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_proxy_banad.conf` |
| **wg_sr_top500_banlist.conf** | Top500 常用黑名单（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_top500_banlist.conf` |
| **wg_sr_top500_banlist_ad.conf** | Top500 黑名单 + 去广告（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_top500_banlist_ad.conf` |
| **wg_sr_top500_whitelist.conf** | Top500 常用白名单（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_top500_whitelist.conf` |
| **wg_sr_top500_whitelist_ad.conf** | Top500 白名单 + 去广告（WG 增强） | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_top500_whitelist_ad.conf` |

---

### 🛠 使用教程

#### 场景 1：在寝室 / 连上了已配置 WireGuard 的路由器 Wi-Fi
1. 在 Shadowrocket「配置」中下载并勾选 **标准版**（例如 `lazy.conf`）；
2. 首页开启连接，内网流量由路由器底层直接路由，外网流量走小火箭代理分流。

#### 场景 2：在室外 / 蜂窝网络下需要访问 10.x 内网
1. 在 Shadowrocket「配置」中下载并勾选 **`wg_` 增强版**（例如 `wg_lazy.conf`）；
2. 点击配置详情 **(i)** -> **规则 (Rules)** -> 点击顶部的 `10.10.0.0/24` 规则，将策略切换为你的 **WireGuard 节点**；
3. 首页开启连接即可享受完整的 Raw Socket 内网穿透。

---

### 🤖 自动化运维

- **定时同步**：由 GitHub Actions 于每日北京时间 08:30 (UTC 00:30) 自动拉取上游发布版本并同时生成两套规则推送到仓库。
- **纯净开源**：不含任何私人服务器 IP、凭据或密钥，安全透明。

---

## 🇬🇧 English Documentation

> 🚀 **Daily automated dual-track synchronization of upstream [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) rules, providing both untouched "Standard" profiles and "WireGuard Enhanced" profiles with iOS raw socket routing patches.**

### 💡 Dual-Track Architecture

1. **Standard Profiles**:
   - Ideal when connected to a router/gateway with kernel-level WireGuard or on local intranet.
   - Clean upstream rules without forcing subnet TUN routing.
2. **WireGuard Enhanced (`wg_` prefix)**:
   - Injects `tun-included-routes = 10.10.0.0/24` and placeholder rules to resolve iOS POSIX raw socket timeout issues for SSH/ServerBox on cellular/public networks.
3. **No Name Collision**:
   - Standard and `wg_` profiles have distinct filenames so both can be imported side-by-side in Shadowrocket without overwriting each other.

---

### 📋 Standard Subscription URLs (Raw)

| Rule Name | Features | Raw Subscription URL |
| :--- | :--- | :--- |
| **lazy.conf** | Lazy config (No policy groups, recommended) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/lazy.conf` |
| **lazy_group.conf** | Lazy config (With policy groups) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/lazy_group.conf` |
| **sr_ad_only.conf** | Ad blocking only | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_ad_only.conf` |
| **sr_adb.conf** | Ad + tracker blocking | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_adb.conf` |
| **sr_backcn.conf** | Mainland China direct / return | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_backcn.conf` |
| **sr_backcn_ad.conf** | Mainland China direct + Ad blocking | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_backcn_ad.conf` |
| **sr_cnip.conf** | China IP Direct | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_cnip.conf` |
| **sr_cnip_ad.conf** | China IP Direct + Ad blocking | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_cnip_ad.conf` |
| **sr_direct_banad.conf** | Direct mode + Ad blocking | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_direct_banad.conf` |
| **sr_proxy_banad.conf** | Global proxy + Ad blocking | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_proxy_banad.conf` |
| **sr_top500_banlist.conf** | Top 500 blocklist | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_banlist.conf` |
| **sr_top500_banlist_ad.conf**| Top 500 blocklist + Ad blocking | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_banlist_ad.conf` |
| **sr_top500_whitelist.conf** | Top 500 whitelist | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_whitelist.conf` |
| **sr_top500_whitelist_ad.conf**| Top 500 whitelist + Ad blocking | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/sr_top500_whitelist_ad.conf` |

---

### 📋 WireGuard Enhanced URLs (Raw)

| Rule Name | Features | Raw Subscription URL |
| :--- | :--- | :--- |
| **wg_lazy.conf** | Lazy config (No policy groups, WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_lazy.conf` |
| **wg_lazy_group.conf** | Lazy config (With policy groups, WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_lazy_group.conf` |
| **wg_sr_ad_only.conf** | Ad blocking only (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_ad_only.conf` |
| **wg_sr_adb.conf** | Ad + tracker blocking (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_adb.conf` |
| **wg_sr_backcn.conf** | Mainland China direct / return (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_backcn.conf` |
| **wg_sr_backcn_ad.conf** | Mainland China direct + Ad blocking (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_backcn_ad.conf` |
| **wg_sr_cnip.conf** | China IP Direct (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_cnip.conf` |
| **wg_sr_cnip_ad.conf** | China IP Direct + Ad blocking (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_cnip_ad.conf` |
| **wg_sr_direct_banad.conf** | Direct mode + Ad blocking (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_direct_banad.conf` |
| **wg_sr_proxy_banad.conf** | Global proxy + Ad blocking (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_proxy_banad.conf` |
| **wg_sr_top500_banlist.conf** | Top 500 blocklist (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_top500_banlist.conf` |
| **wg_sr_top500_banlist_ad.conf**| Top 500 blocklist + Ad blocking (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_top500_banlist_ad.conf` |
| **wg_sr_top500_whitelist.conf** | Top 500 whitelist (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_top500_whitelist.conf` |
| **wg_sr_top500_whitelist_ad.conf**| Top 500 whitelist + Ad blocking (WG Enhanced) | `https://raw.githubusercontent.com/AnonyJcy/shadowrocket-rules/main/wg_sr_top500_whitelist_ad.conf` |
