# Task: Convert index.html to pitch redirect

> Handoff spec for Claude Code terminal. Read this file, execute, verify contracts.

## Context

Per `site-ia.md`, the pitch IS the home page. `index.html` should be a simple meta redirect to `pitch.html`, not a standalone page.

## What to Do

Replace the entire contents of `docs/index.html` with:

```html
<!DOCTYPE html>
<html><head>
<meta http-equiv="refresh" content="0;url=pitch.html">
<title>Intent</title>
</head><body>
<p>Redirecting to <a href="pitch.html">Intent</a>...</p>
</body></html>
```

That's it. The file goes from ~7KB to ~170 bytes. This is intentional — it is NOT content loss.

## Verification

```bash
cd ~/Workspaces/Core/frameworks/intent/docs

# Must contain the redirect
grep -q 'url=pitch.html' index.html && echo "PASS: redirect present" || echo "FAIL: missing redirect"

# Must be small (redirect only)
SIZE=$(wc -c < index.html)
[ "$SIZE" -lt 300 ] && echo "PASS: redirect-only size ($SIZE bytes)" || echo "FAIL: still has old content ($SIZE bytes)"

# Logo link on all other pages still points to index.html
FAIL=0
for f in *.html; do
  [ "$f" = "index.html" ] && continue
  if grep -q 'class="site-nav"' "$f"; then
    if grep -q 'href="index.html"' "$f"; then
      : # good
    else
      echo "FAIL: $f logo doesn't link to index.html"
      FAIL=1
    fi
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: logo links intact"
```

**Note:** CON-SITE-006 will flag index.html as below its 5.6KB baseline. This is expected and correct — update the baseline in site-contracts.md to 100 bytes after this change.

## After Verification

```bash
cd ~/Workspaces/Core/frameworks/intent

# Update the size check in contracts
sed -i '' 's/check_size index.html 5600/# index.html is now a redirect — no size check needed/' docs/site-contracts.md

git add docs/index.html docs/site-contracts.md
git commit -m "Convert index.html to pitch.html redirect

The pitch IS the home page. index.html now contains a meta redirect
to pitch.html instead of standalone content. Per site-ia.md decision.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push origin main
```
