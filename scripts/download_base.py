#!/usr/bin/env python3
"""Resolve and download the upstream Meeye base APK.

Order:
  1. --url / APK_URL. A failure here stops the build (no silent fallback).
  2. Latest GitHub release of yeyebbc/meeye-releases that ships a Meeye *.apk.
  3. Pinned release: tag E-10.0, asset Meeye-E-10.0-c400-release.apk.

Prints one JSON object. When GITHUB_OUTPUT is set, also appends
path, version, filename, source, and url for later workflow steps.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request

UPSTREAM = "yeyebbc/meeye-releases"
PIN_TAG = "E-10.0"
PIN_ASSET = "Meeye-E-10.0-c400-release.apk"
PIN_URL = (
    f"https://github.com/{UPSTREAM}/releases/download/{PIN_TAG}/{PIN_ASSET}"
)
API = "https://api.github.com"


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(1)


class GitHubLookupError(Exception):
    pass


def gh_json(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "meeye-custom-build",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        raise GitHubLookupError(f"GitHub API {exc.code} for {url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise GitHubLookupError(f"GitHub API request failed for {url}: {exc}") from exc


def filename_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    name = urllib.parse.unquote(path.rstrip("/").split("/")[-1])
    if not name or name.endswith(".apk") is False and "apk" not in name.lower():
        # Keep a usable name even if the override URL has no filename.
        if not name.lower().endswith(".apk"):
            return "base.apk"
    return name or "base.apk"


def version_from_filename(name: str) -> str:
    match = re.match(r"(?i)Meeye-(.+)-release\.apk$", name)
    raw = match.group(1) if match else re.sub(r"(?i)\.apk$", "", name)
    cleaned = re.sub(r"[^A-Za-z0-9._+-]+", "-", raw).strip("-")
    return cleaned or "custom"


def score_asset(asset: dict) -> float:
    name = asset.get("name") or ""
    score = 0.0
    if name.startswith("Meeye-") and name.endswith("-release.apk"):
        score += 100
    elif name.startswith("Meeye") and name.lower().endswith(".apk"):
        score += 50
    if "meeyo" in name.lower():
        score -= 80
    size = asset.get("size") or 0
    score += min(size, 10**12) / 10**12
    return score


def pick_asset(assets: list) -> dict | None:
    apks = [a for a in assets if (a.get("name") or "").lower().endswith(".apk")]
    if not apks:
        return None
    best = max(apks, key=score_asset)
    if score_asset(best) < 50:
        return None
    return best


def resolve(explicit_url: str | None) -> dict:
    if explicit_url:
        name = filename_from_url(explicit_url)
        return {
            "url": explicit_url,
            "filename": name if name.lower().endswith(".apk") else "base.apk",
            "version": version_from_filename(name),
            "source": "override",
        }

    print(f"querying latest release of {UPSTREAM}", file=sys.stderr)
    try:
        latest = gh_json(f"{API}/repos/{UPSTREAM}/releases/latest")
    except GitHubLookupError as exc:
        print(f"latest release lookup failed ({exc}); trying pin {PIN_TAG}", file=sys.stderr)
        latest = None

    if latest:
        asset = pick_asset(latest.get("assets") or [])
        if asset and asset.get("browser_download_url"):
            tag = latest.get("tag_name") or version_from_filename(asset["name"])
            version = re.sub(r"[^A-Za-z0-9._+-]+", "-", tag).strip("-") or "custom"
            return {
                "url": asset["browser_download_url"],
                "filename": asset["name"],
                "version": version,
                "source": "latest",
            }
        print(
            "latest release has no Meeye *.apk asset; trying pin "
            f"{PIN_TAG}/{PIN_ASSET}",
            file=sys.stderr,
        )

    try:
        pinned = gh_json(f"{API}/repos/{UPSTREAM}/releases/tags/{PIN_TAG}")
    except GitHubLookupError as exc:
        print(f"pinned release lookup failed ({exc}); using {PIN_URL}", file=sys.stderr)
        pinned = None
    if pinned:
        for asset in pinned.get("assets") or []:
            if asset.get("name") == PIN_ASSET and asset.get("browser_download_url"):
                return {
                    "url": asset["browser_download_url"],
                    "filename": PIN_ASSET,
                    "version": PIN_TAG,
                    "source": "pin",
                }
        print(f"pin asset missing from the API; using {PIN_URL}", file=sys.stderr)
    return {
        "url": PIN_URL,
        "filename": PIN_ASSET,
        "version": PIN_TAG,
        "source": "pin",
    }


def download(url: str, dest: str) -> None:
    headers = {"User-Agent": "meeye-custom-build"}
    request = urllib.request.Request(url, headers=headers)
    tmp = dest + ".partial"
    try:
        with urllib.request.urlopen(request, timeout=180) as response, open(tmp, "wb") as handle:
            shutil.copyfileobj(response, handle, length=1024 * 1024)
    except urllib.error.HTTPError as exc:
        die(f"download failed HTTP {exc.code}: {url}")
    except urllib.error.URLError as exc:
        die(f"download failed: {url}: {exc}")
    os.replace(tmp, dest)
    with open(dest, "rb") as handle:
        magic = handle.read(4)
    if magic != b"PK\x03\x04":
        die(f"downloaded file is not an apk/zip: {dest}")
    size = os.path.getsize(dest)
    if size < 1_000_000:
        die(f"downloaded apk is unexpectedly small ({size} bytes)")


def write_github_output(meta: dict) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        for key in ("path", "version", "filename", "source", "url"):
            value = str(meta[key]).replace("\n", "")
            handle.write(f"{key}={value}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", required=True, help="directory to write the apk into")
    parser.add_argument("--url", default=os.environ.get("APK_URL") or "", help="override download URL")
    parser.add_argument("--dry-run", action="store_true", help="resolve only; do not download")
    args = parser.parse_args()
    explicit = args.url.strip() or None
    meta = resolve(explicit)
    os.makedirs(args.dest, exist_ok=True)
    dest = os.path.join(args.dest, meta["filename"])
    meta["path"] = dest
    if not args.dry_run:
        print(f"downloading {meta['source']} {meta['url']}", file=sys.stderr)
        download(meta["url"], dest)
        print(f"saved {dest} ({os.path.getsize(dest)} bytes)", file=sys.stderr)
    write_github_output(meta)
    json.dump(meta, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
