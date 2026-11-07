# -*- coding: utf-8 -*-
"""Check every cached blob against the GitHub API in parallel.

A blob that the API does not know about cannot be referenced from a tree,
so it has to be uploaded again.  Running the checks concurrently keeps the
sweep to a few seconds instead of several minutes.
"""
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOKEN = os.environ.get("GH_TOKEN", "").strip()
REPO = "boppfilmsales-design/apig-blog"
API = "https://api.github.com/repos/%s/git/blobs/" % REPO


def head(sha):
    req = urllib.request.Request(API + sha)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("User-Agent", "apig-verify")
    try:
        with urllib.request.urlopen(req, timeout=45,
                                    context=ssl.create_default_context()) as resp:
            resp.read()
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:
        return 0


def main():
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "blob_cache.json")
    with open(cache_path, encoding="utf-8") as handle:
        cache = json.load(handle)

    items = list(cache.items())
    print("检查 %d 个缓存 blob ..." % len(items))

    invalid = []

    def check(item):
        path, sha = item
        status = head(sha)
        if status != 200:
            return path, sha, status
        return None

    with ThreadPoolExecutor(max_workers=12) as pool:
        for result in pool.map(check, items):
            if result:
                invalid.append(result)

    print("无效 blob: %d" % len(invalid))
    for path, sha, status in invalid[:20]:
        print("   %s  %s  %s" % (status, path, sha[:12]))

    if invalid:
        broken = {path for path, _, _ in invalid}
        with open(cache_path, "w", encoding="utf-8") as handle:
            json.dump({p: s for p, s in cache.items() if p not in broken},
                      handle)
        print("已从缓存中移除 %d 条无效记录" % len(broken))
    else:
        print("缓存全部有效")


if __name__ == "__main__":
    main()
