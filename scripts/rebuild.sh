#!/usr/bin/env bash
# Decode a Meeye APK, apply icons/, rebuild, zipalign, sign, and verify.
#
# usage: rebuild.sh <original.apk> <icons_dir> <out.apk>
#
# Signing (stable across builds when these are set):
#   KEYSTORE_FILE KEYSTORE_PASSWORD KEY_ALIAS KEY_PASSWORD
# If KEYSTORE_FILE is unset, a throwaway key is generated in the temp work
# directory and a warning is printed. That key is not reusable.
#
# Apktool:
#   Uses $APKTOOL_JAR when set, otherwise `apktool` on PATH.
# zipalign and apksigner must be on PATH (Android build-tools).
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: rebuild.sh <original.apk> <icons_dir> <out.apk>" >&2
  exit 2
fi

ORIG=$1
ICONS=$2
OUT=$3

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
APPLY="$ROOT/scripts/apply_icons.py"
WORK=${WORK_DIR:-$(mktemp -d)}
cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

for cmd in java python3 zipalign apksigner keytool; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "error: '$cmd' is not on PATH" >&2
    exit 1
  fi
done
if [[ ! -f "$ORIG" ]]; then
  echo "error: base apk not found: $ORIG" >&2
  exit 1
fi
if [[ ! -d "$ICONS" ]]; then
  echo "error: icons dir not found: $ICONS" >&2
  exit 1
fi

run_apktool() {
  if [[ -n "${APKTOOL_JAR:-}" ]]; then
    java -Xmx4g -Dfile.encoding=utf-8 \
      -Djdk.util.zip.disableZip64ExtraFieldValidation=true \
      -Djdk.nio.zipfs.allowDotZipEntry=true \
      -jar "$APKTOOL_JAR" "$@"
  elif command -v apktool >/dev/null 2>&1; then
    apktool "$@"
  else
    echo "error: apktool not found. Install it or set APKTOOL_JAR." >&2
    exit 1
  fi
}

echo "decoding $ORIG"
run_apktool d -f -o "$WORK/dec" "$ORIG"

echo "applying icons from $ICONS"
python3 "$APPLY" "$WORK/dec" "$ICONS"

# Version bump: a custom build must never look older than the store build, or
# Google Play offers an "update" that would replace it. Package name and
# signing stay unchanged. VERSION_CODE defaults to 900000.
echo "setting version (VERSION_CODE=${VERSION_CODE:-900000})"
VERSION_CODE=${VERSION_CODE:-900000} python3 - "$WORK/dec/apktool.yml" <<'PY'
import os, re, sys
path = sys.argv[1]
code = os.environ["VERSION_CODE"]
if not code.isdigit():
    sys.exit(f"error: VERSION_CODE must be an integer, got {code!r}")
with open(path, encoding="utf-8") as fh:
    text = fh.read()
m = re.search(r"^(\s*)versionName:\s*(.*?)\s*$", text, re.M)
if not m or not re.search(r"^\s*versionCode:", text, re.M):
    sys.exit(f"error: {path} has no versionInfo versionCode/versionName")
name = m.group(2).strip("'\"")
if not name.endswith("-custom"):
    name += "-custom"
text = re.sub(r"^(\s*)versionCode:.*$", lambda x: f"{x.group(1)}versionCode: {code}", text, count=1, flags=re.M)
text = re.sub(r"^(\s*)versionName:.*$", lambda x: f"{x.group(1)}versionName: {name}", text, count=1, flags=re.M)
with open(path, "w", encoding="utf-8") as fh:
    fh.write(text)
print(f"versionCode={code} versionName={name}")
PY

echo "rebuilding"
# apktool 2.11.1 accepts --use-aapt2 (aapt2 is also its default). 2.12 removed the flag.
run_apktool b --use-aapt2 -o "$WORK/unsigned.apk" "$WORK/dec"

echo "zipalign"
zipalign -f -p 4 "$WORK/unsigned.apk" "$WORK/aligned.apk"

if [[ -n "${KEYSTORE_FILE:-}" ]]; then
  if [[ ! -f "$KEYSTORE_FILE" ]]; then
    echo "error: KEYSTORE_FILE does not exist: $KEYSTORE_FILE" >&2
    exit 1
  fi
  : "${KEYSTORE_PASSWORD:?KEYSTORE_PASSWORD is required when KEYSTORE_FILE is set}"
  : "${KEY_ALIAS:?KEY_ALIAS is required when KEYSTORE_FILE is set}"
  : "${KEY_PASSWORD:?KEY_PASSWORD is required when KEYSTORE_FILE is set}"
  echo "signing with stable keystore $KEYSTORE_FILE (alias $KEY_ALIAS)"
else
  echo "WARNING: no KEYSTORE_FILE set. Signing with a one-off throwaway key." >&2
  echo "WARNING: this APK will NOT update over a previous install. Configure the repo secrets to keep a stable signature." >&2
  KEYSTORE_FILE="$WORK/throwaway.p12"
  KEYSTORE_PASSWORD=$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')
  KEY_PASSWORD=$KEYSTORE_PASSWORD
  KEY_ALIAS=meeye-throwaway
  keytool -genkeypair \
    -keystore "$KEYSTORE_FILE" \
    -storetype PKCS12 \
    -storepass "$KEYSTORE_PASSWORD" \
    -keypass "$KEY_PASSWORD" \
    -alias "$KEY_ALIAS" \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000 \
    -dname "CN=Meeye Custom Throwaway, OU=Personal" >/dev/null
fi

export KEYSTORE_PASSWORD KEY_PASSWORD
mkdir -p "$(dirname "$OUT")"
# env: keeps the passwords out of the process arguments.
apksigner sign \
  --ks "$KEYSTORE_FILE" \
  --ks-pass env:KEYSTORE_PASSWORD \
  --key-pass env:KEY_PASSWORD \
  --ks-key-alias "$KEY_ALIAS" \
  --v1-signing-enabled true \
  --v2-signing-enabled true \
  --v3-signing-enabled true \
  --out "$OUT" \
  "$WORK/aligned.apk"

echo "verifying $OUT"
verify_out=$(apksigner verify --verbose --print-certs "$OUT")
printf '%s\n' "$verify_out"
for scheme in v1 v2 v3; do
  if ! grep -q "Verified using ${scheme} scheme.*: true" <<<"$verify_out"; then
    echo "error: ${scheme} signature did not verify" >&2
    exit 1
  fi
done

if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  digest=$(grep -m1 "certificate SHA-256 digest:" <<<"$verify_out" | sed 's/.*: //')
  {
    echo
    echo "### 校验"
    echo "- v1 / v2 / v3 签名均通过"
    if [[ -n "$digest" ]]; then
      echo "- 证书 SHA-256: \`$digest\`"
      echo "  同一把稳定密钥每次构建这个值应保持不变。变了就说明没用同一把密钥，手机上需要先卸载再装。"
    fi
  } >>"$GITHUB_STEP_SUMMARY"
fi

echo "wrote $OUT"
