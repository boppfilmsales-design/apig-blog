# -*- coding: utf-8 -*-
"""Push the rebuilt site to GitHub through the Git Data API.

The local checkout keeps the site files at the repository root, while the
remote repository nests them under ``apig-website/``.  This script mirrors
the working tree into that layout, uploads every file as a blob, rebuilds
the tree with ``base_tree`` and lands a single commit on ``main``.

Only one commit is produced, so the diff stays reviewable in the GitHub UI.
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
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOKEN = os.environ.get("GH_TOKEN", "").strip()
if not TOKEN:
    raise SystemExit("请先设置环境变量 GH_TOKEN（GitHub Personal Access Token）")
REPO = "boppfilmsales-design/apig-blog"
BRANCH = "main"
PREFIX = "apig-website"          # remote folder that holds the site
SOURCE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.github.com/repos/%s" % REPO

# Files that must never be published.
SKIP_NAMES = {"apig_key.pem", ".DS_Store", "Thumbs.db", "blob_cache.json"}
SKIP_DIRS = {".git", "__pycache__", "raw_images", ".venv", "venv", "dist"}
SKIP_EXT = {".pem", ".key", ".p12", ".pfx", ".log"}
# Legacy page from the previous site build; superseded by en/ and zh/.
SKIP_PATHS = {"about.html"}


def request(method, url, data=None, raw=False):
    """Call the GitHub API with a small retry budget."""
    body = None
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "apig-deploy",
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
                if raw:
                    return resp.status, payload
                return resp.status, (json.loads(payload.decode("utf-8")) if payload else {})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            last = "HTTP %s %s" % (exc.code, detail)
            if exc.code in (422, 401, 403):
                raise RuntimeError("%s %s -> %s" % (method, url, last))
        except Exception as exc:                       # network hiccup
            last = repr(exc)
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("%s %s failed: %s" % (method, url, last))


def collect():
    """Walk the working tree and return {remote_path: absolute_local_path}."""
    files = {}
    for root, dirs, names in os.walk(SOURCE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in names:
            if name in SKIP_NAMES:
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in SKIP_EXT:
                continue
            absolute = os.path.join(root, name)
            rel = os.path.relpath(absolute, SOURCE).replace(os.sep, "/")
            if rel in SKIP_PATHS:
                continue
            files["%s/%s" % (PREFIX, rel)] = absolute
    return files


def git_blob_sha(path):
    """Git blob SHA-1 of a file, computed the way GitHub does."""
    with open(path, "rb") as handle:
        payload = handle.read()
    header = ("blob %d\0" % len(payload)).encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def main():
    files = collect()
    print("待上传文件: %d" % len(files))

    # 1. current remote commit -> the parent of the new commit
    status, ref = request("GET", "%s/git/refs/heads/%s" % (API, BRANCH))
    parent_sha = ref["object"]["sha"]
    status, head = request("GET", "%s/git/commits/%s" % (API, parent_sha))
    print("远端 HEAD 提交: %s" % parent_sha)

    # 2. create blobs (skip ones already present with the same content)
    status, remote = request("GET", "%s/git/trees/%s?recursive=1" % (API, BRANCH))
    existing = {}
    for entry in remote.get("tree", []):
        if entry["type"] == "blob":
            existing[entry["path"]] = entry["sha"]

    # a local cache keeps a restarted run from re-uploading finished blobs
    cache_path = os.path.join(SOURCE, "build", "blob_cache.json")
    cache = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, encoding="utf-8") as handle:
                cache = json.load(handle)
        except Exception:
            cache = {}

    def cache_save():
        with open(cache_path, "w", encoding="utf-8") as handle:
            json.dump(cache, handle)

    entries = []
    reused = created = 0
    todo = []
    for remote_path, local_path in sorted(files.items()):
        sha = git_blob_sha(local_path)
        if existing.get(remote_path) == sha or cache.get(remote_path) == sha:
            reused += 1
            entries.append({"path": remote_path, "mode": "100644",
                            "type": "blob", "sha": sha})
        else:
            todo.append((remote_path, local_path))

    # upload the missing blobs concurrently - a serial pass takes minutes
    print("需新建 blob: %d (复用 %d)" % (len(todo), reused))
    done = [0]

    def upload(job):
        remote_path, local_path = job
        with open(local_path, "rb") as handle:
            payload = handle.read()
        expected = git_blob_sha(local_path)
        # A blob can be reported as created while the request actually failed
        # in transit, so the returned SHA is checked against the local one
        # and re-uploaded when it does not match.
        for attempt in range(3):
            status, blob = request(
                "POST", "%s/git/blobs" % API,
                {"content": base64.b64encode(payload).decode("ascii"),
                 "encoding": "base64"})
            if blob.get("sha") == expected:
                done[0] += 1
                if done[0] % 100 == 0 or done[0] == len(todo):
                    print("  blobs %d/%d" % (done[0], len(todo)), flush=True)
                return remote_path, expected
            time.sleep(1.5 * (attempt + 1))
        raise RuntimeError("blob 上传结果不一致: %s" % remote_path)

    with ThreadPoolExecutor(max_workers=8) as pool:
        for remote_path, sha in pool.map(upload, todo):
            entries.append({"path": remote_path, "mode": "100644",
                            "type": "blob", "sha": sha})
            cache[remote_path] = sha
            created += 1
            if created % 50 == 0:
                cache_save()

    cache_save()
    print("blob 完成: 新建 %d, 复用 %d" % (created, reused))

    # 3. rebuild the tree
    #    The full tree is sent without `base_tree`, so the new layout replaces
    #    the old one wholesale - stale paths (old root pages, the leaked key)
    #    simply disappear.  Mixing `base_tree` with deletions trips
    #    GitRPC::BadObjectState on the GitHub side.
    status, new_tree = request("POST", "%s/git/trees" % API, {"tree": entries})
    print("新树: %s" % new_tree["sha"])

    status, check = request("GET", "%s/git/trees/%s?recursive=1" % (API, new_tree["sha"]))
    print("新树条目数: %d" % len(check.get("tree", [])))

    # 4. commit
    status, commit = request("POST", "%s/git/commits" % API, {
        "message": "Rebuild site as a bilingual blog (EN/ZH) with full catalogue",
        "tree": new_tree["sha"],
        "parents": [parent_sha],
    })
    print("提交: %s" % commit["sha"])

    # 5. move the branch
    status, ref = request("PATCH", "%s/git/refs/heads/%s" % (API, BRANCH),
                          {"sha": commit["sha"], "force": False})
    print("分支已更新: %s -> %s" % (BRANCH, ref["object"]["sha"]))
    print("https://github.com/%s/commit/%s" % (REPO, commit["sha"]))


if __name__ == "__main__":
    main()
