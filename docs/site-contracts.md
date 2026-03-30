# Intent Site Contracts

> Verifiable assertions for the Intent product site. Run these checks after ANY modification to files in `docs/`.
> Each contract is a shell command that returns pass/fail. All must pass before committing.
> **IA v2:** Three-pillar model — see `site-ia.md` for full specification.

## CON-SITE-001: Every HTML file has the 3-link primary nav

**Type:** structural
**Severity:** critical — broken nav means users can't navigate

```bash
# Verify: every .html file in docs/ contains the site-nav with 3 pillar links
cd docs/
FAIL=0
for f in *.html; do
  if grep -q 'class="site-nav"' "$f"; then
    : # has nav
  else
    echo "FAIL: $f missing site-nav"
    FAIL=1
  fi
  for link in pitch.html work-system.html architecture.html; do
    if grep -q "href=\"$link\"" "$f"; then
      : # has link
    else
      echo "FAIL: $f missing nav link to $link"
      FAIL=1
    fi
  done
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-001"
```

## CON-SITE-002: Correct active states per pillar

**Type:** structural
**Severity:** major — wrong active state confuses navigation

```bash
# Verify: every page has exactly the right active states
# Primary nav: one of The Story / The System / The Build
# Sub-nav: one link matching the current page
cd docs/
FAIL=0

# Pillar 1 pages should have "The Story" active in primary nav
for f in pitch.html concept-brief.html methodology.html roadmap.html; do
  if [ -f "$f" ]; then
    if grep -q 'class="active"' "$f"; then
      : # has at least one active
    else
      echo "FAIL: $f has no active nav link"
      FAIL=1
    fi
  fi
done

# Pillar 2 pages should have "The System" active in primary nav
for f in work-system.html flow-diagram.html schemas.html signals.html dogfood.html event-catalog.html; do
  if [ -f "$f" ]; then
    if grep -q 'class="active"' "$f"; then
      : # has at least one active
    else
      echo "FAIL: $f has no active nav link"
      FAIL=1
    fi
  fi
done

# Pillar 3 pages should have "The Build" active in primary nav
for f in architecture.html agents.html deployment.html arb.html decisions.html native-repos.html; do
  if [ -f "$f" ]; then
    if grep -q 'class="active"' "$f"; then
      : # has at least one active
    else
      echo "FAIL: $f has no active nav link"
      FAIL=1
    fi
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
  if grep -q 'github.com/theparlor/intent' "$f"; then
    : # has footer link
  else
    echo "FAIL: $f missing standard footer link"
    FAIL=1
  fi
  if grep -q 'Built with the Intent methodology' "$f"; then
    : # has tagline
  else
    echo "FAIL: $f missing footer tagline"
    FAIL=1
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-003"
```

## CON-SITE-004: All HTML pages link styles.css

**Type:** structural
**Severity:** critical — missing styles.css means no shared foundation (nav, palette, typography)

```bash
cd docs/
FAIL=0
for f in *.html; do
  if grep -q 'href="styles.css"' "$f"; then
    : # has styles.css
  else
    echo "FAIL: $f does not link styles.css"
    FAIL=1
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-004"
```

## CON-SITE-005: Rich pages retain page-specific CSS

**Type:** quality
**Severity:** critical — stripping inline styles from rich pages destroys their visual components

```bash
# Rich pages must have substantial inline <style> blocks
cd docs/
FAIL=0
check_inline_css() {
  local file=$1 min_lines=$2
  if [ -f "$file" ]; then
    CSS_LINES=$(sed -n '/<style>/,/<\/style>/p' "$file" | wc -l)
    if [ "$CSS_LINES" -lt "$min_lines" ]; then
      echo "FAIL: $file has only ${CSS_LINES} lines of inline CSS, expected at least ${min_lines} (page-specific CSS may have been stripped)"
      FAIL=1
    fi
  fi
}
check_inline_css pitch.html 50
check_inline_css arb.html 80
check_inline_css signals.html 50
check_inline_css roadmap.html 50
check_inline_css dogfood.html 30
check_inline_css architecture.html 30
check_inline_css agents.html 30
check_inline_css deployment.html 30
check_inline_css index.html 20
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
check_size arb.html 27300
check_size dogfood.html 14000
check_size roadmap.html 10500
check_size methodology.html 8400
check_size concept-brief.html 7000
check_size decisions.html 3500
check_size event-catalog.html 1800
check_size schemas.html 5600
check_size architecture.html 10500
check_size agents.html 10500
check_size deployment.html 8400
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-006"
```

## CON-SITE-007: Sub-nav on ALL pillar pages

**Type:** structural
**Severity:** critical — every page in a pillar needs sub-nav for within-pillar navigation

```bash
cd docs/
FAIL=0

# Pillar 1: The Story
for f in pitch.html concept-brief.html methodology.html roadmap.html; do
  if [ -f "$f" ]; then
    if grep -q 'class="sub-nav"' "$f"; then
      : # has sub-nav
    else
      echo "FAIL: $f missing sub-nav (Pillar 1 — The Story)"
      FAIL=1
    fi
  fi
done

# Pillar 2: The System
for f in work-system.html flow-diagram.html schemas.html signals.html dogfood.html event-catalog.html; do
  if [ -f "$f" ]; then
    if grep -q 'class="sub-nav"' "$f"; then
      : # has sub-nav
    else
      echo "FAIL: $f missing sub-nav (Pillar 2 — The System)"
      FAIL=1
    fi
  fi
done

# Pillar 3: The Build
for f in architecture.html agents.html deployment.html arb.html decisions.html native-repos.html; do
  if [ -f "$f" ]; then
    if grep -q 'class="sub-nav"' "$f"; then
      : # has sub-nav
    else
      echo "FAIL: $f missing sub-nav (Pillar 3 — The Build)"
      FAIL=1
    fi
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

# arb.html must have tab interface, SVG radar visual, and tech radar cards
if [ -f arb.html ]; then
  grep -q 'switchTab' arb.html || { echo "FAIL: arb.html missing tab interface JS"; FAIL=1; }
  grep -q 'tab-btn' arb.html || { echo "FAIL: arb.html missing tab buttons"; FAIL=1; }
  grep -q 'radar' arb.html || { echo "FAIL: arb.html missing tech radar"; FAIL=1; }
  grep -q '<svg' arb.html || { echo "FAIL: arb.html missing SVG radar visual"; FAIL=1; }
  grep -q 'class="blip"' arb.html || { echo "FAIL: arb.html missing radar blips"; FAIL=1; }
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

## CON-SITE-010: Primary nav has exactly 3 pillar links (no old 9-link nav)

**Type:** structural
**Severity:** critical — ensures the IA v2 migration is complete, no pages retain old nav

```bash
cd docs/
FAIL=0
for f in *.html; do
  # Old nav had direct links to methodology, concept-brief, schemas, etc. in primary nav
  # New nav only has pitch, work-system, architecture in primary nav
  # Check that old-style nav links are NOT in the site-nav block
  OLD_IN_NAV=$(sed -n '/<nav class="site-nav">/,/<\/nav>/p' "$f" | grep -c 'href="methodology.html"\|href="concept-brief.html"\|href="schemas.html"\|href="flow-diagram.html"\|href="arb.html"\|href="dogfood.html"\|href="roadmap.html"')
  if [ "$OLD_IN_NAV" -gt 0 ]; then
    echo "FAIL: $f still has old 9-link primary nav (found $OLD_IN_NAV old links in site-nav)"
    FAIL=1
  fi
done
[ $FAIL -eq 0 ] && echo "PASS: CON-SITE-010"
```

## Contract Summary

| ID | Name | Severity | What It Catches |
|----|------|----------|-----------------|
| CON-SITE-001 | 3-link primary nav present | critical | Missing pillar navigation |
| CON-SITE-002 | Active state correct per pillar | major | Wrong pillar/page highlighted |
| CON-SITE-003 | Standard footer | major | Missing/wrong footer |
| CON-SITE-004 | All pages link styles.css | critical | Missing shared foundation |
| CON-SITE-005 | Rich pages retain inline CSS | critical | Stripped page-specific visuals |
| CON-SITE-006 | File size canary | critical | Content loss detection |
| CON-SITE-007 | Sub-nav on ALL pillar pages | critical | Missing within-pillar navigation |
| CON-SITE-008 | Visual components intact | critical | Lost diagrams/interactives |
| CON-SITE-009 | No broken links | major | Dead internal links |
| CON-SITE-010 | No old 9-link nav remnants | critical | Incomplete IA migration |
