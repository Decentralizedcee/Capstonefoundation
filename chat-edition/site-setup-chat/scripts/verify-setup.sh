#!/usr/bin/env bash
# Verify a website project set up for the blog / service-page skills.
# Usage: bash verify-setup.sh [project_root] [nextjs|astro]
# Prints PASS / WARN / FAIL lines. Never prints secret values. Exit code 1 if any FAIL.

ROOT="${1:-.}"
FW="${2:-}"
cd "$ROOT" 2>/dev/null || { echo "FAIL  cannot open folder: $ROOT"; exit 2; }

PASS=0; WARN=0; FAIL=0
ok()   { echo "PASS  $*"; PASS=$((PASS+1)); }
warn() { echo "WARN  $*"; WARN=$((WARN+1)); }
bad()  { echo "FAIL  $*"; FAIL=$((FAIL+1)); }

# First word after "key:" in the Stack adapter (empty if absent).
adapter() {
  [ -f CLAUDE.md ] || return 0
  awk -v k="$1:" '$1==k {print $2; exit}' CLAUDE.md
}
is_placeholder() { case "$1" in "{{"*|"") return 0 ;; *) return 1 ;; esac; }

echo "Project: $(pwd)"
echo "------------------------------------------------------------"

# ---- CLAUDE.md and the Stack adapter ----
if [ -f CLAUDE.md ]; then
  ok "CLAUDE.md exists"
  A_FW="$(adapter framework)"
  if is_placeholder "$A_FW"; then bad "Stack adapter: framework is not filled in"; else ok "Stack adapter framework: $A_FW"; fi
  [ -z "$FW" ] && FW="$A_FW"
  PH=$(grep -c '{{' CLAUDE.md)
  if [ "$PH" -gt 0 ]; then warn "CLAUDE.md still has $PH line(s) with {{placeholders}} (items the owner has not supplied)"; else ok "CLAUDE.md has no leftover placeholders"; fi
else
  bad "CLAUDE.md is missing"
fi
case "$FW" in nextjs|astro) ;; *) [ -n "$FW" ] && warn "Unknown framework '$FW' (expected nextjs or astro); framework-specific checks skipped" ;; esac

OUT_DIR="$(adapter output_dir)"; is_placeholder "$OUT_DIR" && OUT_DIR=""
[ -z "$OUT_DIR" ] && case "$FW" in nextjs) OUT_DIR="out" ;; astro) OUT_DIR="dist" ;; esac
IMG_DIR="$(adapter local_images_dir)"; is_placeholder "$IMG_DIR" && IMG_DIR="images"
BLOG_DIR="$(adapter blog_collection)"; is_placeholder "$BLOG_DIR" && BLOG_DIR=""
LOG_FILE="$(adapter published_log)"; is_placeholder "$LOG_FILE" && LOG_FILE=""
case "$FW" in nextjs) CACHE_DIR=".next" ;; astro) CACHE_DIR=".astro" ;; *) CACHE_DIR="" ;; esac

# ---- files ----
for f in .gitignore .env.example; do
  if [ -f "$f" ]; then ok "$f exists"; else bad "$f is missing"; fi
done
[ -f .env ] && ok ".env exists" || warn ".env is missing (create it with empty values; the owner types the keys)"
[ -f README.md ] && ok "README.md exists" || warn "README.md is missing (placeholder is fine at this stage)"
[ -f keywords.csv ] && ok "keywords.csv exists" || warn "keywords.csv is missing (header only is fine)"
[ -f docs/on-page-seo-checklist.md ] && ok "docs/on-page-seo-checklist.md exists" || warn "docs/on-page-seo-checklist.md is missing (copy it from a skill's references folder)"

# ---- folders ----
for d in docs references public scripts "$IMG_DIR"; do
  if [ -d "$d" ]; then ok "folder $d/ exists"; else bad "folder $d/ is missing"; fi
done
if [ -n "$BLOG_DIR" ]; then
  [ -d "$BLOG_DIR" ] && ok "blog folder $BLOG_DIR/ exists" || warn "blog folder $BLOG_DIR/ is missing (create it before the first post)"
fi
if [ -n "$LOG_FILE" ]; then
  LOG_PARENT="$(dirname "$LOG_FILE")"
  [ -d "$LOG_PARENT" ] && ok "published log folder $LOG_PARENT/ exists" || warn "published log folder $LOG_PARENT/ is missing"
fi

# ---- reference files ----
for f in voice tone humor opinions stats stories; do
  p="references/$f.md"
  if [ -f "$p" ]; then
    n=$(grep -c '{{' "$p")
    if [ "$n" -gt 0 ]; then warn "$p has $n line(s) with {{placeholders}} still to fill"; else ok "$p filled"; fi
  else
    bad "$p is missing"
  fi
done

# ---- .env: report status only, never values ----
if [ -f .env ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|\#*) continue ;; esac
    key="${line%%=*}"; val="${line#*=}"
    key="${key//[[:space:]]/}"
    [ -z "$key" ] && continue
    if [ -n "$val" ]; then st="SET (value hidden)"; else st="empty"; fi
    echo "INFO  .env $key: $st"
    case "$key" in
      NEXT_PUBLIC_*|PUBLIC_*)
        if echo "$key" | grep -Eq '(^|_)(KEY|SECRET|TOKEN|PASSWORD|PASSWD)(_|$)'; then
          bad ".env: '$key' looks like a secret behind a public prefix (visible to every visitor). Rename it without the prefix."
        fi ;;
    esac
  done < .env
fi

# ---- git ignore checks ----
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ok "folder is a git repository"
  chk() { # label path
    if git check-ignore -q "$2" 2>/dev/null; then ok "$1 is git-ignored"; else bad "$1 is NOT git-ignored ($2)"; fi
  }
  chk ".env" ".env"
  chk "node_modules" "node_modules/x"
  [ -n "$OUT_DIR" ] && chk "build output ($OUT_DIR/)" "$OUT_DIR/index.html"
  [ -n "$CACHE_DIR" ] && chk "framework cache ($CACHE_DIR/)" "$CACHE_DIR/x"
  chk "images folder contents ($IMG_DIR/)" "$IMG_DIR/test.jpg"
  if git check-ignore -q "$IMG_DIR/.gitkeep" 2>/dev/null; then
    warn "$IMG_DIR/.gitkeep is ignored, so the empty folder will not be kept. Add a line '!$IMG_DIR/.gitkeep' to .gitignore"
  else
    ok "$IMG_DIR/.gitkeep can be tracked"
  fi
  if git ls-files --error-unmatch .env >/dev/null 2>&1; then
    bad ".env is TRACKED by git. Remove it from git (git rm --cached .env) and rotate any key that was in it."
  else
    ok ".env is not tracked by git"
  fi
else
  warn "not a git repository, so ignore rules could not be tested. Checking .gitignore text instead"
  for pat in ".env" "node_modules"; do
    grep -Eq "^/?${pat}/?$" .gitignore 2>/dev/null && ok ".gitignore lists $pat" || bad ".gitignore does not list $pat"
  done
fi

# ---- stray video files ----
VIDS=$(find . \( -path ./node_modules -o -path ./.git -o -path "./$OUT_DIR" \) -prune -o -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.avi' -o -iname '*.mkv' -o -iname '*.webm' \) -print 2>/dev/null)
if [ -n "$VIDS" ]; then
  warn "video files found (videos should be embedded from YouTube or Vimeo, not committed):"
  echo "$VIDS" | sed 's/^/        /'
else
  ok "no video files in the project"
fi

echo "------------------------------------------------------------"
echo "Summary: $PASS passed, $WARN warning(s), $FAIL failed"
[ "$FAIL" -gt 0 ] && exit 1
exit 0
