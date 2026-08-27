# Shadowrocket-Rules (WireGuard & LAN Bypass Enhanced)

[中文](#-中文文档) | [English](#-english-documentation)

---

## 🇨🇳 中文文档

> 🚀 **自动每日同步上游 [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) 最新去广告与分流规则，并自动修复 iOS 虚拟内网（WireGuard / Tailscale / 自建隧道）原始 Socket 路由穿透问题。**

### 💡 痛点与技术原理 (Why & How)

#### 1. 遇到什么痛点？
在 iOS / iPadOS 上使用 Shadowrocket（小火箭）接入自建 WireGuard 节点或虚拟内网（如 `10.x.x.x`）时，经常会遇到以下现象：
- **Safari 浏览器正常**：访问内网 Web 控制台完全通畅；
- **第三方 App 超时失败**：使用 **SSH 客户端（Termius、ServerBox、Blink）、数据库工具、远程桌面（RDP/VNC）** 等通过原始 TCP/UDP Socket 连接内网时，连接直接卡住并报错 `SocketException: Connection timed out (errno = 110)`；
- **官方 WireGuard App 却完全正常**。

#### 2. 根本原因剖析
- **HTTP 代理 vs 原始 Socket**：Safari 使用的是系统级 WebKit/CFNetwork 栈，会主动走小火箭的 Local HTTP Proxy 端口，因此能被正确分流；而 SSH、ServerBox 等第三方 App 发起的是底层的 **POSIX raw TCP Socket**。
- **iOS 路由优先级机制**：默认情况下，小火箭的虚拟网卡声明的是全局默认路由（`0.0.0.0/0`）。但在 iOS 内部路由表中，Wi-Fi 物理网卡（`en0`）具有更具体的子网掩码优先级。如果规则文件将 `10.0.0.0/8` 排除或未显式声明包含，iOS 会**绕过小火箭虚拟网卡，直接把数据包扔给物理 Wi-Fi 网卡**，导致链路直接超时。
- **官方 App 为什么正常**：官方 WireGuard App 是纯 Layer 3 IP 隧道，会强制向系统内核注册具体的网段路由表。

#### 3. 本库的自动修补方案
本项目通过 GitHub Actions 每天全自动拉取上游最新规则，并执行以下底层热修补：
1. **强制声明 TUN 包含路由 (`tun-included-routes`)**：
   在 `[General]` 中注入 `tun-included-routes = 10.10.0.0/24`，强制指示 iOS 内核将内网网段的数据包送入小火箭虚拟网卡接管，彻底解决 SSH、ServerBox 等非 Web 流量超时问题。
2. **清理内核级旁路限制**：
   剥离上游默认配置中 `tun-excluded-routes` 与 `skip-proxy` 对 `10.0.0.0/8` 的拦截。
3. **预埋无感分流规则**：
   在 `[Rule]` 最顶端预埋 `IP-CIDR,10.10.0.0/24,DIRECT,no-resolve` 占位规则，用户导入后只需在 UI 中将策略切换为自己的 WireGuard 节点即可，零配置门槛且不泄露任何节点私密信息。

---

### 📋 规则订阅链接列表

在 Shadowrocket（小火箭）中进入 **配置 (Config)** -> 右上角 **`+`** -> 粘贴以下任一链接并下载使用：

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

### 🛠 使用教程 (3 步极简上手)

1. **添加/更新配置**：
   复制上方任一规则链接，在小火箭「配置」中下载并勾选使用；
2. **绑定内网节点**：
   点击该配置右侧的 **(i)** 详情 -> 点击 **规则 (Rules)** -> 点击最顶部第一条 `10.10.0.0/24` 规则，将策略（Policy）从 `DIRECT` 切换为你自己的 **WireGuard 节点**；
3. **开启连接**：
   首页全局路由保持 **配置 (Config)**，主节点选择你的常用代理节点，开启小火箭开关即可实现：
   - 访问外网（GitHub / Google 等）走常规代理；
   - 访问自建内网（SSH / Web / ServerBox 等）走 WireGuard；
   - 国内流量与广告拦截正常分流。

---

### 🤖 自动化运维

- **定时同步**：由 GitHub Actions 于每日北京时间 08:30 (UTC 00:30) 自动拉取上游发布版本并自动修补推送。
- **纯净开源**：不含任何私人服务器 IP、凭据或密钥，安全透明。

---

## 🇬🇧 English Documentation

> 🚀 **Daily automated synchronization of upstream [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) rules, with automated routing fixes for iOS raw TCP/UDP sockets over WireGuard and private LAN tunnels.**

### 💡 Background & Technical Details

#### 1. The Problem
When using Shadowrocket on iOS/iPadOS connected to a private WireGuard node (e.g., `10.x.x.x` subnet):
- **Safari / Web Browsers work fine**: Internal web dashboards load as expected.
- **Third-party Apps fail with timeout**: SSH clients (**Termius, ServerBox, Blink**), database tools, or remote desktop (RDP/VNC) fail to connect, throwing `SocketException: Connection timed out (errno = 110)`.
- **The official WireGuard App works without issues**.

#### 2. Root Cause Analysis
- **HTTP Proxy vs. Raw Socket**: Safari routes traffic through Shadowrocket's local HTTP proxy listener via `CFNetwork`/`WebKit`. However, non-HTTP tools (SSH, Flutter apps, ServerBox) establish POSIX raw TCP sockets.
- **iOS Route Table Priority**: Shadowrocket's virtual TUN interface advertises a default route (`0.0.0.0/0`). In iOS kernel routing, the physical Wi-Fi interface (`en0`) has a more specific subnet metric. If `10.0.0.0/8` is not explicitly declared in `tun-included-routes`, iOS routes raw socket packets to the physical Wi-Fi adapter instead of the VPN TUN interface.
- **Why the official App works**: The official WireGuard client establishes a pure Layer 3 network interface and registers explicit CIDR subnet routes directly with the iOS kernel.

#### 3. Automated Patching Solution
This repository uses GitHub Actions to sync and patch rules daily:
1. **Force Include TUN Routes (`tun-included-routes`)**:
   Injects `tun-included-routes = 10.10.0.0/24` into `[General]`, ensuring all raw socket packets destined for the subnet are routed into Shadowrocket's TUN stack.
2. **Remove Kernel-Level Bypasses**:
   Strips `10.0.0.0/8` from `tun-excluded-routes` and `skip-proxy`.
3. **Pre-injected Rule Placeholder**:
   Injects `IP-CIDR,10.10.0.0/24,DIRECT,no-resolve` at the top of `[Rule]`. Users simply tap to select their WireGuard node policy without exposing sensitive credentials.

---

### 📋 Rule Subscription URLs (Raw)

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

### 🛠 Quick Start (3 Steps)

1. **Import Config**: Copy any raw configuration link above and import it in Shadowrocket under **Config**;
2. **Bind Node Policy**: Tap the **(i)** info icon of the config -> tap **Rules** -> tap the top `10.10.0.0/24` rule -> change the policy from `DIRECT` to your **WireGuard node**;
3. **Connect**: Set global routing mode to **Config** and toggle the main switch on.

---

### 🤖 Automation

- **Daily Sync**: Automatically pulls, patches, and pushes upstream updates daily via GitHub Actions at 08:30 CST (00:30 UTC).
- **Clean & Safe**: Zero sensitive information, private endpoints, or credentials stored.
