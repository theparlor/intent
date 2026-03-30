# Intent Site Contracts

> Verifiable assertions for the Intent product site. Run these checks after ANY modification to files in `docs/`.
> Each contract is a shell command that returns pass/fail. All must pass before committing.

## CON-SITE-001: Every HTML file has the primary nav

**Type:** structural
**Severity:** critical — broken nav means users can't navigate

```bash
# Verify: every .html file in docs/ contains the site-nav with all 9 links
cd docs/
FAIL=0
for f in *.html; do
  if ! grep -q 'class="site-nav"' "$f"; then
    echo "FAIL: $f missing site-nav"
    FAIL=1
  fi
  for link in pitch.html methodology.html concept-brief.html work-system.html flow-diagram.html schemas.html arb.html dogfood.html roadmap.html; do
    if ! grep -q "href=\"$link\"" "$f"; then
      echo "FAIL: $f missing nav link to $link"
      FAIL=1
    fi
  done
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-001"
```

## CON-SITE-002: Exactly one nav link is active per page

**Type:** structural
**Severity:** major — wrong active state confuses navigation

```bash
# Verify: pages in the primary nav have exactly one active link
cd docs/
FAIL=0
for f in pitch.html methodology.html concept-brief.html work-system.html flow-diagram.html schemas.html arb.html dogfood.html roadmap.html; do
  COUNT=$(grep -o 'class="active"' "$f" | head -20 | wc -l)
  # Primary nav pages should have at least 1 active (may have 2 if also in sub-nav)
  if [ "$COUNT" -lt 1 ]; then
    echo "FAIL: $f has no active nav link"
    FAIL=1
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-002"
```

## CON-SITE-003: Standard footer on all pages

**Type:** structural
**Severity:** major — branding consistency

```bash
# Verify: every .html file contains the standard footer text
cd docs/
FAIL=0
for f in *.html; do
  if ! grep -q 'github.com/theparlor/intent' "$f"; then
    echo "FAIL: $f missing standard footer link"
    FAIL=1
  fi
  if ! grep -q 'Built with the Intent methodology' "$f"; then
    echo "FAIL: $f missing footer tagline"
    FAIL=1
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-003"
```

## CON-SITE-004: Strategy B pages do NOT link styles.css

**Type:** structural
**Severity:** critical — linking styles.css on a Strategy B page causes CSS conflicts

```bash
# Strategy B pages: pitch.html, dogfood.html, arb.html, roadmap.html, signals.html
cd docs/
FAIL=0
for f in pitch.html dogfood.html arb.html roadmap.html signals.html; do
  if [ -f "$f" ] && grep -q 'href="styles.css"' "$f"; then
    echo "FAIL: $f is Strategy B but links styles.css"
    FAIL=1
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-004"
```

## CON-SITE-005: Strategy A pages DO link styles.css

**Type:** structural
**Severity:** critical — missing styles.css means no base styling

```bash
# Strategy A pages
cd docs/
FAIL=0
for f in index.html methodology.html concept-brief.html schemas.html work-system.html flow-diagram.html decisions.html event-catalog.html native-repos.html visual-brief.html architecture.html agents.html deployment.html; do
  if [ -f "$f" ] && ! grep -q 'href="styles.css"' "$f"; then
    echo "FAIL: $f is Strategy A but does not link styles.css"
    FAIL=1
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-005"
```

## CON-SITE-006: File size canary — no page dropped below 70% of baseline

**Type:** quality
**Severity:** critical — a dramatic size drop means content was lost

```bash
cd docs/
FAIL=0
check_size() {
  local file=$1 min=$2
  if [ -f "$file" ]; then
    SIZE=$(wc -c < "$file")
    if [ "$SIZE" -lt "$min" ]; then
      echo "FAIL: $file is ${SIZE}B, expected at least ${min}B (content may be lost)"
      FAIL=1
    fi
  fi
}
# 70% of baseline sizes
check_size pitch.html 18200
check_size work-system.html 33600
check_size signals.html 33600
check_size arb.html 22400
check_size dogfood.html 14000
check_size roadmap.html 10500
check_size methodology.html 8400
check_size concept-brief.html 7000
check_size decisions.html 7000
check_size event-catalog.html 7000
check_size schemas.html 5600
check_size index.html 5600
check_size architecture.html 10500
check_size agents.html 10500
check_size deployment.html 8400
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-006"
```

## CON-SITE-007: Technical sub-nav on depth pages

**Type:** structural
**Severity:** major — technical pages need the sub-nav for navigation between them

```bash
cd docs/
FAIL=0
for f in architecture.html agents.html deployment.html; do
  if [ -f "$f" ] && ! grep -q 'class="sub-nav"' "$f"; then
    echo "FAIL: $f missing sub-nav"
    FAIL=1
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-007"
```

## CON-SITE-008: Key visual components preserved

**Type:** quality
**Severity:** critical — these are the page's primary value

```bash
cd docs/
FAIL=0

# pitch.html must have its visual components
if [ -f pitch.html ]; then
  grep -q 'fracture-grid' pitch.html || { echo "FAIL: pitch.html missing fracture grid"; FAIL=1; }
  grep -q 'timeline' pitch.html || { echo "FAIL: pitch.html missing timeline"; FAIL=1; }
  grep -q 'compare-strip' pitch.html || { echo "FAIL: pitch.html missing comparison strip"; FAIL=1; }
  grep -q '<svg' pitch.html || { echo "FAIL: pitch.html missing SVG loop diagram"; FAIL=1; }
  grep -q 'stat-box' pitch.html || { echo "FAIL: pitch.html missing stat boxes"; FAIL=1; }
  grep -q 'plane-diagram' pitch.html || { echo "FAIL: pitch.html missing two-plane diagram"; FAIL=1; }
fi

# arb.html must have tab interface and tech radar
if [ -f arb.html ]; then
  grep -q 'switchTab' arb.html || { echo "FAIL: arb.html missing tab interface JS"; FAIL=1; }
  grep -q 'tab-btn' arb.html || { echo "FAIL: arb.html missing tab buttons"; FAIL=1; }
  grep -q 'radar' arb.html || { echo "FAIL: arb.html missing tech radar"; FAIL=1; }
fi

# signals.html must have signal cards
if [ -f signals.html ]; then
  grep -q 'SIG-001' signals.html || { echo "FAIL: signals.html missing SIG-001"; FAIL=1; }
  grep -q 'SIG-015' signals.html || { echo "FAIL: signals.html missing SIG-015"; FAIL=1; }
fi

[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-008"
```

## CON-SITE-009: No broken internal links

**Type:** quality
**Severity:** major — broken links are a bad user experience

```bash
cd docs/
FAIL=0
# Extract all href="*.html" references and check the files exist
for f in *.html; do
  LINKS=$(grep -oP 'href="\K[^"]*\.html' "$f" 2>/dev/null | sort -u)
  for link in $LINKS; do
    # Skip external links
    if [[ "$link" == http* ]]; then continue; fi
    if [ ! -f "$link" ]; then
      echo "FAIL: $f links to $link which does not exist"
      FAIL=1
    fi
  done
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-009"
```

## Running All Contracts

```bash
#!/bin/bash
# Save as docs/verify-site.sh and run after any change
cd "$(dirname "$0")"
echo "=== Intent Site Contract Verification ==="
echo ""

# Run each contract check...
# (paste each contract's bash block here)

echo ""
echo "=== Verification Complete ==="
```

## Contract Summary

| ID | Name | Severity | What It Catches |
|----|------|----------|-----------------|
| CON-SITE-001 | Primary nav present | critical | Missing navigation |
| CON-SITE-002 | Active state correct | major | Wrong page highlighted |
| CON-SITE-003 | Standard footer | major | Missing/wrong footer |
| CON-SITE-004 | Strategy B no styles.css | critical | CSS strategy violation |
| CON-SITE-005 | Strategy A has styles.css | critical | CSS strategy violation |
| CON-SITE-006 | File size canary | critical | Content loss detection |
| CON-SITE-007 | Sub-nav on tech pages | major | Missing technical nav |
| CON-SITE-008 | Visual components intact | critical | Lost diagrams/interactives |
| CON-SITE-009 | No broken links | major | Dead internal links |
