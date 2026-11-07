# -*- coding: utf-8 -*-
"""Rewrite the repository history without the leaked private key.

``apig-website/apig_key.pem`` was published in the first two commits of this
public repository.  Removing it from the branch tip is not enough - the old
commits stay reachable by SHA and the key can still be downloaded.

This script replays every commit in order, drops the key from each tree and
re-creates the commit with the original message, author and dates.  The
branch is then force-updated to the rewritten tip.
"""
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
        "User-Agent": "apig-history-rewrite",
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
            detail = exc.read().decode("utf-8", "replace")[:300]
            last = "HTTP %s %s" % (exc.code, detail)
            if exc.code in (422, 401, 403):
                raise RuntimeError("%s %s -> %s" % (method, url, last))
        except Exception as exc:
            last = repr(exc)
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("%s %s failed: %s" % (method, url, last))


def main():
    # 1. list the commits oldest first
    status, commits = request(
        "GET", "%s/commits?per_page=100&sha=%s" % (API, BRANCH))
    commits = list(reversed(commits))
    print("待重写提交: %d" % len(commits))

    # 2. replay them without the key
    parent = None
    mapping = {}
    for entry in commits:
        sha = entry["sha"]
        status, commit = request("GET", "%s/git/commits/%s" % (API, sha))
        tree_sha = commit["tree"]["sha"]
        status, tree = request("GET", "%s/git/trees/%s?recursive=1" % (API, tree_sha))

        entries = [{"path": node["path"], "mode": node["mode"],
                    "type": node["type"], "sha": node["sha"]}
                   for node in tree.get("tree", []) if node["type"] == "blob"]
        had_key = any(node["path"] == TARGET for node in tree.get("tree", []))
        if had_key:
            entries = [node for node in entries if node["path"] != TARGET]

        status, new_tree = request("POST", "%s/git/trees" % API, {"tree": entries})

        payload = {
            "message": commit["message"],
            "tree": new_tree["sha"],
            "parents": [parent] if parent else [],
        }
        author = commit.get("author") or {}
        if author.get("name"):
            payload["author"] = {"name": author["name"], "email": author["email"],
                                  "date": author.get("date")}
        committer = commit.get("committer") or {}
        if committer.get("name"):
            payload["committer"] = {"name": committer["name"],
                                     "email": committer["email"],
                                     "date": committer.get("date")}

        status, new_commit = request("POST", "%s/git/commits" % API, payload)
        mapping[sha] = new_commit["sha"]
        parent = new_commit["sha"]
        flag = " (已移除私钥)" if had_key else ""
        print("   %s -> %s  %s%s" % (sha[:10], new_commit["sha"][:10],
                                     commit["message"].splitlines()[0][:52], flag))

    if not parent:
        print("没有需要重写的提交")
        return

    # 3. move the branch
    status, ref = request("PATCH", "%s/git/refs/heads/%s" % (API, BRANCH),
                          {"sha": parent, "force": True})
    print("分支已重写: %s -> %s" % (BRANCH, ref["object"]["sha"]))

    # 4. verify no commit in the new history carries the key
    status, commits2 = request("GET", "%s/commits?per_page=100&sha=%s" % (API, BRANCH))
    residual = []
    for entry in commits2:
        status, tree = request(
            "GET", "%s/git/trees/%s?recursive=1" % (API, entry["sha"]))
        if any(node["path"].endswith(".pem") for node in tree.get("tree", [])):
            residual.append(entry["sha"][:10])
    print("新历史中的 pem 残留:", residual if residual else "无")
    print("https://github.com/%s" % REPO)


if __name__ == "__main__":
    main()
