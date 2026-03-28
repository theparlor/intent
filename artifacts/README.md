# Intent Artifacts

Visual and interactive explorations of the Intent work system.

## Artifacts

1. **intent-visual-brief** (intent-visual-brief.html)
   - A one-page visual summary of Intent
   - Seven-unit work ontology (Signal → Intent → Spec → Contract → Capability → Feature → Product)
   - Three governance dimensions (Right Things, Right Time, Right Way)
   - Agent workflow model

2. **intent-native-repos** (native-repos.html)
   - A guide to structuring repositories for Intent
   - Signal capture (.intent/signals/)
   - Intent and Spec definitions
   - Capability atomization
   - Observable work (git log, CI/CD integration)

3. **intent-work-system** (work-system.html)
   - The full interactive work system explorer
   - Tabbed interface for exploring each dimension
   - Dashboard mockup showing team capability health
   - Side-by-side Agile ↔ Intent comparison
   - Click-to-expand detail cards for each work unit

## Viewing Options

### GitHub Pages
All artifacts are live at [theparlor/intent](https://github.com/theparlor/intent):
- [Visual Brief](https://theparlor.github.io/intent/visual-brief.html)
- [Native Repos](https://theparlor.github.io/intent/native-repos.html)
- [Work System](https://theparlor.github.io/intent/work-system.html)

### Local Development
```bash
cd docs
python3 -m http.server 8000
```
Then visit `http://localhost:8000`

### Claude / Cowork
- Paste `artifacts/intent-work-system.jsx` into a Claude canvas for interactive editing
- Use Cowork's artifact system for rapid iteration

## Navigation

All pages include a back-link to `index.html` for easy navigation between artifacts.