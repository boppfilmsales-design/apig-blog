# -*- coding: utf-8 -*-
"""Add a single file to the remote repository without rebuilding the tree.

Rebuilding the whole tree can hit GitHub's "input was too large" timeout when
the site carries several hundred entries. When only one file changes, sending
a small tree that only lists that path on top of the current ``base_tree``
is enough - GitHub keeps every other path from the base untouched.
"""
import base64
import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOKEN = os.environ.get("GH_TOKEN", "").strip()
if not TOKEN:
    raise SystemExit("请先设置环境变量 GH_TOKEN")
REPO = "boppfilmsales-design/apig-blog"
BRANCH = "main"
PREFIX = "apig-website"
API = "https://api.github.com/repos/%s" % REPO
SOURCE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def request(method, url, data=None):
    body = None
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "apig-push-one",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    ctx = ssl.create_default_context()
    last = None
    for attempt in range(6):
        req = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=90, context=ctx) as resp:
                payload = resp.read()
                return resp.status, (json.loads(payload.decode("utf-8")) if payload else {})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            last = "HTTP %s %s" % (exc.code, detail)
            if exc.code in (401, 403, 422) and "too large" not in last and "timed out" not in last:
                raise RuntimeError("%s %s -> %s" % (method, url, last))
        except Exception as exc:
            last = repr(exc)
        import time
        time.sleep(2.0 * (attempt + 1))
    raise RuntimeError("%s %s failed: %s" % (method, url, last))


def blob_sha(path):
    with open(path, "rb") as handle:
        payload = handle.read()
    header = ("blob %d\0" % len(payload)).encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def main():
    rel_paths = sys.argv[1:]
    if not rel_paths:
        raise SystemExit("用法: python push_one.py <相对路径> [...]")

    status, ref = request("GET", "%s/git/refs/heads/%s" % (API, BRANCH))
    parent_sha = ref["object"]["sha"]
    print("远端 HEAD:", parent_sha)

    status, commit_info = request("GET", "%s/git/commits/%s" % (API, parent_sha))
    base_tree = commit_info["tree"]["sha"]
    print("基准树:", base_tree)

    entries = []
    for rel in rel_paths:
        local = os.path.join(SOURCE, rel.replace("/", os.sep))
        if not os.path.isfile(local):
            raise SystemExit("本地文件不存在: " + local)
        with open(local, "rb") as handle:
            payload = handle.read()
        expected = blob_sha(local)
        status, blob = request("POST", "%s/git/blobs" % API,
                               {"content": base64.b64encode(payload).decode("ascii"),
                                "encoding": "base64"})
        if blob.get("sha") != expected:
            raise SystemExit("blob sha 不一致: %s" % rel)
        entries.append({"path": "%s/%s" % (PREFIX, rel), "mode": "100644",
                        "type": "blob", "sha": expected})
        print("blob 已上传:", rel, expected[:10])

    status, tree = request("POST", "%s/git/trees" % API,
                            {"base_tree": base_tree, "tree": entries})
    print("新树:", tree["sha"])

    status, commit = request("POST", "%s/git/commits" % API, {
        "message": "Add Cloudflare Pages build script for Git-based deployment",
        "tree": tree["sha"],
        "parents": [parent_sha],
    })
    print("提交:", commit["sha"])

    status, updated = request("PATCH", "%s/git/refs/heads/%s" % (API, BRANCH),
                               {"sha": commit["sha"], "force": False})
    print("分支已更新 ->", commit["sha"])


if __name__ == "__main__":
    main()
