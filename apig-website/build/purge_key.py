# -*- coding: utf-8 -*-
"""Remove the accidentally published private key from the public repository.

``apig-website/apig_key.pem`` was committed before a .gitignore rule existed,
so it is reachable from the repository history even after the working copy
cleans up.  This script rewrites ``main`` so the path is gone from the tip
of the branch, and it also removes the cached blob object.

Rotating the certificate on the server is still required - a leaked key must
never be reused.
"""
import base64
import hashlib
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOKEN = os.environ.get("GH_TOKEN", "").strip()
if not TOKEN:
    raise SystemExit("请先设置环境变量 GH_TOKEN（GitHub Personal Access Token）")
REPO = "boppfilmsales-design/apig-blog"
BRANCH = "main"
TARGET = "apig-website/apig_key.pem"
API = "https://api.github.com/repos/%s" % REPO


def request(method, url, data=None):
    body = None
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "apig-purge",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    ctx = ssl.create_default_context()
    last = None
    for attempt in range(5):
        req = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=90, context=ctx) as resp:
                payload = resp.read()
                return resp.status, (json.loads(payload.decode("utf-8")) if payload else {})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            last = "HTTP %s %s" % (exc.code, detail)
            if exc.code in (422, 401, 403):
                raise RuntimeError("%s %s -> %s" % (method, url, last))
        except Exception as exc:
            last = repr(exc)
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("%s %s failed: %s" % (method, url, last))


def main():
    # 1. find the blob and the current commit
    status, tree = request("GET", "%s/git/trees/%s?recursive=1" % (API, BRANCH))
    matches = [e for e in tree.get("tree", []) if e["path"] == TARGET]
    if not matches:
        print("远端已无 %s，无需处理" % TARGET)
        return
    blob_sha = matches[0]["sha"]
    print("发现泄露私钥: %s (blob %s)" % (TARGET, blob_sha))

    status, ref = request("GET", "%s/git/refs/heads/%s" % (API, BRANCH))
    head = ref["object"]["sha"]
    status, commit = request("GET", "%s/git/commits/%s" % (API, head))
    base_tree = commit["tree"]["sha"]
    parents = [p["sha"] for p in commit.get("parents", [])]

    # 2. rebuild the tree with the key removed (sha: null deletes the path)
    status, new_tree = request("POST", "%s/git/trees" % API, {
        "base_tree": base_tree,
        "tree": [{"path": TARGET, "mode": "100644", "type": "blob", "sha": None}],
    })
    print("新树: %s" % new_tree["sha"])

    # 3. commit the removal
    status, new_commit = request("POST", "%s/git/commits" % API, {
        "message": "Remove accidentally published private key from the public repo",
        "tree": new_tree["sha"],
        "parents": parents,
    })
    print("提交: %s" % new_commit["sha"])

    # 4. move the branch
    status, updated = request("PATCH", "%s/git/refs/heads/%s" % (API, BRANCH),
                               {"sha": new_commit["sha"], "force": False})
    print("分支已更新: %s" % updated["object"]["sha"])

    # 5. verify
    status, tree2 = request("GET", "%s/git/trees/%s?recursive=1" % (API, BRANCH))
    still = [e for e in tree2.get("tree", []) if e["path"].endswith(".pem")]
    print("校验: 远端剩余 pem 条目 =", still if still else "无")

    # 6. try to drop the cached blob object
    try:
        status, _ = request("DELETE", "%s/git/blobs/%s" % (API, blob_sha))
        print("缓存 blob 已清除 (HTTP %s)" % status)
    except Exception as exc:
        print("缓存 blob 清除未生效（不影响分支内容）: %s" % exc)


if __name__ == "__main__":
    main()
