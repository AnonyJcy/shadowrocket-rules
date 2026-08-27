import urllib.request
import urllib.parse
import json
import re
import os

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

def fetch_raw_content(path):
    quoted_path = urllib.parse.quote(path)
    url = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{BRANCH}/{quoted_path}"
    req = urllib.request.Request(url, headers={"User-Agent": "Shadowrocket-Rule-Syncer"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

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
            patched_text = patch_conf(text)
            with open(path, "w", encoding="utf-8") as f:
                f.write(patched_text)
        elif path.lower() == "readme.md":
            continue
        else:
            with open(path, "wb") as f:
                f.write(raw_bytes)

    print("All upstream files synchronized and patched successfully.")

if __name__ == "__main__":
    main()
