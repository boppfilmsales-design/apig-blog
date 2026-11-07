# -*- coding: utf-8 -*-
"""Diagnose why GitHub refuses the tree payload.

Walks the entry list in growing slices and reports the first size that the
API rejects, plus the raw response body.
"""
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TOKEN = os.environ.get("GH_TOKEN", "").strip()
REPO = "boppfilmsales-design/apig-blog"
API = "https://api.github.com/repos/%s" % REPO


def call(method, url, data=None):
    body = None
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "apig-diag",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept-Encoding": "identity",
    }
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120,
                                    context=ssl.create_default_context()) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw.decode("utf-8")) if raw else {})
    except urllib.error.HTTPError as exc:
        try:
            raw = exc.read()
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            payload = {"raw": "unreadable"}
        return exc.code, payload
    except Exception as exc:
        return 0, {"raw": repr(exc)}


def main():
    import push_github as pg

    files = pg.collect()
    entries = []
    for remote_path, local_path in sorted(files.items()):
        entries.append({"path": remote_path, "mode": "100644",
                        "type": "blob", "sha": pg.git_blob_sha(local_path)})
    print("总条目: %d" % len(entries))

    # 1. does a single-entry tree work at all?
    status, out = call("POST", "%s/git/trees" % API, {"tree": entries[:1]})
    print("单条目树: HTTP %s %s" % (status, out.get("sha") or out.get("message")))

    # 2. binary search for the first failing slice size
    for size in (50, 100, 200, 400, 600, len(entries)):
        status, out = call("POST", "%s/git/trees" % API, {"tree": entries[:size]})
        ok = status == 201
        print("  前 %4d 条: HTTP %s %s" % (
            size, status, "OK" if ok else json.dumps(out, ensure_ascii=False)[:220]))
        if not ok:
            break
        time.sleep(1)

    # 3. inspect the raw JSON of a failing payload
    payload = json.dumps({"tree": entries})
    print("\n请求体大小: %d 字节" % len(payload.encode("utf-8")))

    # 4. look for entries whose blob is not actually present
    missing = []
    for entry in entries[::37]:
        status, out = call("GET", "%s/git/blobs/%s" % (API, entry["sha"]))
        if status != 200:
            missing.append((entry["path"], status))
    print("抽样 blob 检查: %d 个不可达 %s" % (len(missing), missing[:5] if missing else ""))


if __name__ == "__main__":
    main()
