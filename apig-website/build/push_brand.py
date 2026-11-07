"""Incremental push of changed files onto the remote GitHub tree.

Rebuilds only the entries that actually changed and layers them on top of the
current remote base tree, which keeps the tree payload small enough for the
GitHub API to accept.
"""

import base64
import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

SOURCE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PREFIX = "apig-website"
API = "https://api.github.com/repos/boppfilmsales-design/apig-blog"

TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    sys.exit("GH_TOKEN is not set")

CTX = ssl.create_default_context()


def req(method, url, data=None, retries=4):
    body = json.dumps(data).encode("utf-8") if data is not None else None
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "apig-site",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    last = None
    for attempt in range(retries):
        r = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(r, timeout=120, context=CTX) as resp:
                raw = resp.read()
                return json.loads(raw.decode("utf-8")) if raw else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            last = "HTTP %s %s" % (e.code, detail)
            if e.code in (422, 500, 502, 503, 504) and attempt < retries - 1:
                continue
            raise SystemExit("%s %s -> %s" % (method, url, last))
        except Exception as e:  # network hiccup
            last = str(e)
            if attempt < retries - 1:
                continue
            raise SystemExit("%s %s -> %s" % (method, url, last))
    raise SystemExit("unreachable")


def blob_sha(data):
    """Compute the git blob sha locally so unchanged files can be skipped.

    The bytes on disk are hashed verbatim: GitHub stores the raw file content,
    so any re-encoding would produce a mismatching digest.
    """
    header = ("blob %d\0" % len(data)).encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def collect():
    """Map remote path -> absolute local path for every publishable file."""
    skip_names = {"apig_key.pem", ".DS_Store", "Thumbs.db", "blob_cache.json",
                  ".deploy_trigger"}
    skip_dirs = {".git", "__pycache__", "raw_images", ".venv", "venv", "dist"}
    skip_ext = {".pem", ".key", ".p12", ".pfx", ".log"}
    skip_paths = {"about.html"}

    files = {}
    for root, dirs, names in os.walk(SOURCE):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
        for name in names:
            if name in skip_names:
                continue
            if os.path.splitext(name)[1].lower() in skip_ext:
                continue
            absolute = os.path.join(root, name)
            rel = os.path.relpath(absolute, SOURCE).replace(os.sep, "/")
            if rel in skip_paths:
                continue
            files["%s/%s" % (PREFIX, rel)] = absolute
    return files


def remote_blobs():
    """Fetch the current remote tree as path -> sha."""
    tree = req("GET", API + "/git/trees/main?recursive=1")
    entries = tree.get("tree") or []
    return {e["path"]: e["sha"] for e in entries if e.get("type") == "blob"}


def main():
    local = collect()
    remote = remote_blobs()
    print("local files: %d   remote files: %d" % (len(local), len(remote)))

    changed = []
    for path, absolute in local.items():
        with open(absolute, "rb") as f:
            data = f.read()
        sha = blob_sha(data)
        if remote.get(path) != sha:
            changed.append((path, data, sha))

    removed = [p for p in remote if p not in local]
    print("changed: %d   removed: %d" % (len(changed), len(removed)))

    if not changed and not removed:
        print("nothing to push")
        return

    # Upload the changed blobs concurrently. A sequential loop over several
    # hundred files takes far too long against the GitHub API.
    import base64
    from concurrent.futures import ThreadPoolExecutor

    def upload(item):
        path, data, sha = item
        payload = base64.b64encode(data).decode("ascii")
        result = req("POST", API + "/git/blobs", {"content": payload, "encoding": "base64"})
        if result.get("sha") != sha:
            raise SystemExit("blob upload digest mismatch: %s" % path)
        return path, sha

    uploaded = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for index, (path, sha) in enumerate(pool.map(upload, changed), 1):
            uploaded[path] = sha
            if index % 100 == 0:
                print("  blobs %d/%d" % (index, len(changed)), flush=True)

    # Layer the new blobs on top of the remote base tree.
    ref = req("GET", API + "/git/refs/heads/main")
    parent = ref["object"]["sha"]
    commit = req("GET", API + "/git/commits/" + parent)
    base_tree = commit["tree"]["sha"]

    entries = []
    for path, sha in uploaded.items():
        entries.append({"path": path, "mode": "100644", "type": "blob", "sha": sha})
    for path in removed:
        entries.append({"path": path, "mode": "100644", "type": "blob", "sha": None})

    tree = req("POST", API + "/git/trees",
               {"base_tree": base_tree, "tree": entries})
    print("tree:", tree["sha"])

    new_commit = req("POST", API + "/git/commits", {
        "message": "Update brand mark to API",
        "tree": tree["sha"],
        "parents": [parent],
    })
    req("PATCH", API + "/git/refs/heads/main", {"sha": new_commit["sha"], "force": False})
    print("commit:", new_commit["sha"])


if __name__ == "__main__":
    main()
