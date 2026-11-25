import urllib.request
import urllib.parse
import json
import re
import os
import time

UPSTREAM_REPO = "Johnshall/Shadowrocket-ADBlock-Rules-Forever"
BRANCH = "release"

# Set up proxy if running locally in restricted network environment
proxy_url = os.environ.get("https_proxy") or os.environ.get("http_proxy")
if proxy_url:
    proxy_handler = urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)

def fetch_tree():
    url = f"https://api.github.com/repos/{UPSTREAM_REPO}/git/trees/{BRANCH}?recursive=1"
    req = urllib.request.Request(url, headers={"User-Agent": "Shadowrocket-Rule-Syncer"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]

def fetch_raw_content(path, retries=3):
    quoted_path = urllib.parse.quote(path)
    urls = [
        # 1. GitHub API (handles direct access reliably across regions)
        (f"https://api.github.com/repos/{UPSTREAM_REPO}/contents/{quoted_path}?ref={BRANCH}",
         {"User-Agent": "Shadowrocket-Rule-Syncer", "Accept": "application/vnd.github.v3.raw"}),
        # 2. Raw GitHub UserContent fallback
        (f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{BRANCH}/{quoted_path}",
         {"User-Agent": "Shadowrocket-Rule-Syncer"})
    ]

    for attempt in range(retries):
        for url, headers in urls:
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=20) as resp:
                    return resp.read()
            except Exception as e:
                pass
        time.sleep(1.5)
    
    raise RuntimeError(f"Failed to fetch content for: {path} after {retries} retries")

def patch_conf(text):
    # 1. Remove 10.0.0.0/8 from skip-proxy and tun-excluded-routes
    def clean_item(match):
        key = match.group(1)
        val = match.group(2)
        items = [x.strip() for x in val.split(",") if x.strip()]
        items = [x for x in items if x != "10.0.0.0/8"]
        return f"{key} = {', '.join(items)}"

    text = re.sub(r"^(skip-proxy)\s*=\s*(.+)$", clean_item, text, flags=re.MULTILINE)
    text = re.sub(r"^(tun-excluded-routes)\s*=\s*(.+)$", clean_item, text, flags=re.MULTILINE)

    # 2. Add tun-included-routes = 10.10.0.0/24 (forces iOS routing table to capture 10.10.0.0/24 into TUN)
    if re.search(r"^tun-included-routes\s*=", text, flags=re.MULTILINE):
        text = re.sub(r"^tun-included-routes\s*=\s*(.*)$", r"tun-included-routes = 10.10.0.0/24, \1", text, flags=re.MULTILINE)
        text = text.replace("10.10.0.0/24, \n", "10.10.0.0/24\n")
    elif re.search(r"^#\s*tun-included-routes\s*=", text, flags=re.MULTILINE):
        text = re.sub(r"^#\s*tun-included-routes\s*=\s*.*$", "tun-included-routes = 10.10.0.0/24", text, flags=re.MULTILINE)
    else:
        text = text.replace("[General]\n", "[General]\ntun-included-routes = 10.10.0.0/24\n", 1)

    # 3. Pre-inject placeholder rule at the top of [Rule]
    placeholder_rule = (
        "[Rule]\n"
        "IP-CIDR,10.10.0.0/24,DIRECT,no-resolve\n"
    )
    if "[Rule]\n" in text:
        text = text.replace("[Rule]\n", placeholder_rule, 1)
    elif "[Rule]" in text:
        text = text.replace("[Rule]", placeholder_rule, 1)

    return text

# =============================================================================
# 第三方模块合成（Optional module injection）
# 上游每天重新生成 .conf，手工往 conf 里加的 [Script] / MITM 会被覆盖，
# 所以把需要长期保留的外部模块写在这里，由 sync.py 每次同步后重新注入。
# 每项 = 一个 Surge/Shadowrocket 模块里的 http-response 脚本 + 对应 MITM 主机名。
# =============================================================================
INJECTED_SCRIPTS = [
    {
        "tag": "Duolingo_Max",
        "pattern": (
            r"^https?:\/\/(ios-api-[a-z0-9-]+|api\d+)\.duolingo\.c(n|om)"
            r"\/2023-05-23\/(batch|users\/[^\/?#]+)(?:[?#]|$)"
        ),
        "script_path": (
            "https://raw.githubusercontent.com/AnonyJcy/MyScripts"
            "/main/lingoDuo/lingoDuo-xaM.js"
        ),
        "type": "http-response",
        "options": "requires-body=1,max-size=31457280,timeout=120",
        "mitm_hosts": [
            "ios-api-*.duolingo.com",
            "ios-api-*.duolingo.cn",
            "api*.duolingo.com",
            "api*.duolingo.cn",
        ],
    },
]


def inject_modules(text):
    """把 INJECTED_SCRIPTS 合并进 conf：补 [MITM] hostname、补 [Script] 段落。

    幂等：同一个 tag 已存在时不会重复追加；不改变文件中其他任何字节。
    """
    if not INJECTED_SCRIPTS:
        return text
    if "[General]" not in text:
        # 纯规则集（如 sr_ad_only.conf 只有 [Rule]），不属于完整配置，跳过注入
        return text

    eol = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(eol)

    # ---------- 1. [MITM] hostname 合并 ----------
    wanted = [h for item in INJECTED_SCRIPTS for h in item["mitm_hosts"]]
    mitm_idx = next((i for i, l in enumerate(lines) if l.strip() == "[MITM]"), None)
    if mitm_idx is not None:
        end = len(lines)
        for i in range(mitm_idx + 1, len(lines)):
            if lines[i].lstrip().startswith("["):
                end = i
                break
        host_idx = next(
            (i for i in range(mitm_idx + 1, end)
             if re.match(r"^\s*hostname\s*=", lines[i])),
            None,
        )
        if host_idx is None:
            lines.insert(mitm_idx + 1, "hostname = " + ", ".join(wanted))
        else:
            key, _, value = lines[host_idx].partition("=")
            # 去掉 %APPEND%（那是模块专用语法，写进 conf 会变成字面主机名）
            current = [
                x.strip()
                for x in value.replace("%APPEND%", "").split(",")
                if x.strip()
            ]
            lower = {x.lower() for x in current}
            added = [h for h in wanted if h.lower() not in lower]
            if added:
                # 保留上游原本的写法，只在行尾追加缺失的主机名
                base = value.strip().rstrip(",").rstrip()
                lines[host_idx] = f"{key.rstrip()} = {base}, " + ", ".join(added)

    # ---------- 2. [Script] 段落合并 ----------
    block = []
    for item in INJECTED_SCRIPTS:
        if any(re.search(rf"^\s*{re.escape(item['tag'])}\s*=", l) for l in lines):
            continue
        block.append(
            "{tag} = type={type},pattern={pattern},script-path={path},{options}".format(
                tag=item["tag"],
                type=item["type"],
                pattern=item["pattern"],
                path=item["script_path"],
                options=item["options"],
            )
        )
    if block:
        script_idx = next(
            (i for i, l in enumerate(lines) if l.strip() == "[Script]"), None
        )
        if script_idx is not None:
            end = len(lines)
            for i in range(script_idx + 1, len(lines)):
                if lines[i].lstrip().startswith("["):
                    end = i
                    break
            while end > script_idx + 1 and not lines[end - 1].strip():
                end -= 1
            lines[end:end] = block
        elif mitm_idx is not None:
            lines[mitm_idx:mitm_idx] = ["[Script]"] + block + [""]
        else:
            if lines and lines[-1] != "":
                lines.append("")
            lines += ["[Script]"] + block

    return eol.join(lines)


def main():
    tree_paths = fetch_tree()
    print(f"Total upstream files found: {len(tree_paths)}")

    for path in tree_paths:
        if path.startswith(".github/"):
            continue
        
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        print(f"Processing: {path}")
        raw_bytes = fetch_raw_content(path)
        
        if path.endswith(".conf"):
            text = raw_bytes.decode("utf-8")

            # 1. Standard / Official Upstream Config (+ injected modules)
            with open(path, "wb") as f:
                f.write(inject_modules(text).encode("utf-8"))
            
            # 2. WireGuard / TUN Patched Config (wg_ prefix, + injected modules)
            patched_text = patch_conf(text)
            file_name = os.path.basename(path)
            wg_path = os.path.join(dir_name, f"wg_{file_name}") if dir_name else f"wg_{file_name}"
            with open(wg_path, "wb") as f:
                f.write(inject_modules(patched_text).encode("utf-8"))
        elif path.lower() == "readme.md":
            continue
        else:
            with open(path, "wb") as f:
                f.write(raw_bytes)

    print("All upstream files synchronized and patched successfully.")

if __name__ == "__main__":
    main()
