---
name: svg-map-creator
description: |
  Create, customize, and generate SVG maps programmatically using
  simplemaps.com free SVG library and similar open-source map projects.
  Covers the full SVG map workflow: source selection, downloading base maps,
  coloring countries/regions/states by data, building choropleth
  visualizations, adding legends and labels, extracting sub-regions,
  and producing publication-ready SVG output. Synthesizes SVG specification
  knowledge, simplemaps conventions, D3/GeoJSON ecosystem patterns, and
  cartographic data visualization best practices.

  Trigger phrases: "SVG map", "color countries", "choropleth map",
  "world map SVG", "color regions on map", "highlight countries",
  "map visualization", "simplemaps", "country map SVG",
  "color states on map", "SVG world map", "map by data",
  "create a map", "generate map SVG", "data map visualization",
  "shade countries", "heat map countries"
---

# SVG Map Creator

## Core Philosophy

1. **Start from existing maps, never draw from scratch.** Free, optimized
   SVG maps exist for every country. Download, modify, output.
2. **SVG is just XML — parse it, don't render it.** Use XML/text
   manipulation to change colors, add elements, extract regions. No browser
   or rendering library needed for most tasks.
3. **ISO codes are the bridge between data and geometry.** Every region in a
   well-structured SVG map has an ISO code as `id` or `class`. Match your
   data's country/state codes to these identifiers.
4. **Color encodes data — choose scales deliberately.** Sequential for
   magnitude, diverging for above/below threshold, categorical for groups.
   Never use rainbow.
5. **Output self-contained SVG.** Inline all styles, fonts, legends. The SVG
   file should render correctly anywhere without external dependencies.

## Quick-Start: Map Creation Workflow

### Step 1: Choose a Base Map

| Need | Source | Action |
|------|--------|--------|
| World map | SimpleMaps | Download `world.svg` (140KB, Robinson projection) |
| Single country with provinces | SimpleMaps | Download `{iso2}.svg` (e.g., `us.svg`, `de.svg`) |
| Continent | SimpleMaps | Download `europe.svg`, `africa.svg`, etc. |
| Custom projection or GeoJSON | Natural Earth + MapShaper | Convert shapefile → SVG |

→ See `references/map-sources.md` for all URLs and download patterns

### Step 2: Understand the SVG Structure

SimpleMaps SVGs use this convention:
- **Single-territory countries**: `<path id="US" name="United States" ...>`
- **Multi-territory countries**: `<path class="Canada" ...>` (multiple paths)
- Colors in `style="fill:#ececec"` or `fill` attribute
- `viewBox="0 0 2000 857"` defines coordinate system

→ See `references/svg-map-anatomy.md` for full structure reference

### Step 3: Apply Colors

**Python (recommended for batch operations):**
```python
import xml.etree.ElementTree as ET
tree = ET.parse('world.svg')
root = tree.getroot()
ns = {'svg': 'http://www.w3.org/2000/svg'}
# Color by id
for path in root.iter('{http://www.w3.org/2000/svg}path'):
    if path.get('id') == 'US':
        path.set('style', 'fill:#3b82f6')
tree.write('output.svg', xml_declaration=True)
```

**For batch coloring from data, use the script:**
```bash
python3 {this_skill_directory}/scripts/color-svg-map.py \
  --input world.svg --data colors.json --output colored-map.svg
```

→ See `references/manipulation-patterns.md` for all coloring approaches

### Step 4: Add Legend and Labels (Optional)

Insert SVG elements for legend rectangles, text labels, title. Position
using the map's viewBox coordinate system.

→ See `references/data-visualization.md` for legend construction patterns

### Step 5: Output

Save as `.svg` for web/vector use. Convert to PNG via Inkscape CLI if
raster needed: `inkscape input.svg --export-type=png --export-dpi=300`

## Decision Trees

### Map Source Selection

| Criteria | Best Source |
|----------|------------|
| Need it fast, standard projection | SimpleMaps free SVG library |
| Need province/state level | SimpleMaps country-specific SVGs |
| Need custom projection | Natural Earth → MapShaper → SVG |
| Need interactive web map | D3.js + TopoJSON |
| Need React component | react-simple-maps or react-svg-worldmap |

### Color Approach Selection

| Data Type | Color Scale | Example |
|-----------|-------------|---------|
| Continuous (GDP, population) | Sequential (light→dark single hue) | `#eff3ff → #08519c` |
| Above/below center (growth rate) | Diverging (two hues from center) | `#d73027 → #f7f7f7 → #1a9850` |
| Categories (continent, party) | Categorical (distinct hues) | `#e41a1c, #377eb8, #4daf4a` |
| Binary (yes/no, member/not) | Two contrasting colors | `#3b82f6` vs `#e5e7eb` |
| No data / not applicable | Neutral gray | `#d1d5db` |

### Multi-Path Country Handling

| SVG Convention | How to Target | Example |
|----------------|---------------|---------|
| `id="XX"` attribute | `path.get('id') == 'XX'` | Most countries |
| `class="CountryName"` | `'CountryName' in path.get('class','')` | Canada, Russia, Indonesia, etc. |
| Multiple `<path>` elements | Color ALL matching paths | Islands + mainland |

→ See `references/iso-country-codes.md` for complete code lookup

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/color-svg-map.py` | Apply colors to SVG map regions from JSON/CSV data. Handles id and class targeting, multi-path countries, optional legend generation. |

## Reference Files

| File | Contents |
|------|----------|
| `references/svg-map-anatomy.md` | SVG map structure (viewBox, path, id/class/name conventions), SimpleMaps format, multi-path countries, namespace handling, coordinate systems |
| `references/map-sources.md` | SimpleMaps free library (world, US, 200+ countries with exact URLs), Natural Earth + MapShaper pipeline, other open sources, license terms, comparison |
| `references/manipulation-patterns.md` | Python ElementTree, JavaScript DOM, raw text patterns for: coloring regions, adding/removing elements, extracting sub-regions, modifying viewBox, CSS class approach |
| `references/data-visualization.md` | Choropleth design, ColorBrewer scales, legend SVG construction, label placement, tooltip patterns, responsive SVG, accessibility, common pitfalls |
| `references/iso-country-codes.md` | Complete ISO 3166-1 alpha-2 code table, SimpleMaps id vs class mapping, multi-path country list, US state FIPS codes, disputed territory handling |
