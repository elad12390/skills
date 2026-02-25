# SVG Map Sources

Sources: SimpleMaps.com resource library, Natural Earth Data project, D3.js community resources, 2024-2025 ecosystem analysis

Covers: SimpleMaps free SVG library (URLs, available maps, license), Natural Earth Data pipeline, D3/TopoJSON ecosystem, other open-source alternatives, source comparison.

## 1. SimpleMaps Free SVG Library

SimpleMaps is the primary recommendation for web-ready SVG maps due to their consistent formatting, small file sizes, and permissive licensing.

### License and Usage
The maps in the SimpleMaps SVG library are released under the MIT License.
- Free for personal use.
- Free for commercial use.
- Attribution is not strictly required but is appreciated.
- No registration or API keys are needed for direct file downloads.

### Primary Global and Regional Maps
These files are the most commonly used for high-level visualizations.

| Map Type | URL |
|----------|-----|
| World Map (Robinson) | https://simplemaps.com/static/demos/resources/svg-library/svgs/world.svg |
| United States Map | https://simplemaps.com/static/demos/resources/svg-library/svgs/us.svg |
| Europe Map | https://simplemaps.com/static/demos/resources/svg-library/svgs/europe.svg |
| Africa Map | https://simplemaps.com/static/demos/resources/svg-library/svgs/africa.svg |
| North America Map | https://simplemaps.com/static/demos/resources/svg-library/svgs/north_america.svg |
| South America Map | https://simplemaps.com/static/demos/resources/svg-library/svgs/south_america.svg |
| Asia Map | https://simplemaps.com/static/demos/resources/svg-library/svgs/asia.svg |
| Oceania Map | https://simplemaps.com/static/demos/resources/svg-library/svgs/oceania.svg |
| Pacific-Centered World | https://simplemaps.com/static/demos/resources/svg-library/svgs/world_pacific.svg |

### Country-Specific Maps
SimpleMaps provides SVG maps for over 200 countries. Each country map typically includes administrative level 1 boundaries (provinces, states, or regions).

The page URL pattern for discovering these maps is:
`https://simplemaps.com/resources/svg-{iso2_lowercase}`

For example:
- France: https://simplemaps.com/resources/svg-fr
- Brazil: https://simplemaps.com/resources/svg-br
- India: https://simplemaps.com/resources/svg-in

Note: The actual .svg file paths for country maps are often dynamic or nested within their demo structure. It is recommended to visit the resource page to find the specific download link or use the patterned access method described in the download section.

### Available Countries (ISO-2 Codes)
The following countries have dedicated SVG maps available in the SimpleMaps library:

| | | | | | | | |
|---|---|---|---|---|---|---|---|
| AF | AL | DZ | AD | AO | AI | AG | AR |
| AM | AW | AU | AT | AZ | BS | BH | BD |
| BB | BY | BE | BZ | BJ | BM | BT | BO |
| BA | BW | BR | VG | BN | BG | BF | BI |
| KH | CM | CA | CV | KY | CF | TD | CL |
| CN | CO | KM | CR | HR | CU | CW | CY |
| CZ | CI | CD | DK | DJ | DM | DO | EC |
| EG | SV | GQ | ER | EE | ET | FO | FK |
| FJ | FI | FR | PF | GA | GE | DE | GH |
| GR | GL | GD | GT | GN | GW | GY | HT |
| HN | HK | HU | IS | IN | ID | IR | IQ |
| IE | IL | IT | JM | JP | JO | KZ | KE |
| KW | KG | LA | LV | LB | LS | LR | LY |
| LI | LT | LU | MK | MG | MW | MY | MV |
| ML | MT | MR | MU | MX | MD | MN | ME |
| MS | MA | MZ | MM | NA | NR | NP | NL |
| NC | NZ | NI | NE | NG | KP | NO | OM |
| PK | PS | PA | PG | PY | PE | PH | PN |
| PL | PT | PR | QA | CG | RO | RU | RW |
| KN | LC | SX | MF | VC | SA | SN | RS |
| SC | SL | SG | SK | SI | SB | SO | ZA |
| KR | SS | ES | LK | SD | SR | SZ | SE |
| CH | SY | ST | TW | TJ | TZ | TH | GM |
| TL | TG | TO | TT | TN | TR | TM | TC |
| UG | UA | AE | GB | VI | UY | UZ | VU |
| VE | VN | EH | YE | ZM | ZW | | |

### Key Features of SimpleMaps SVGs
1. Optimized File Size: Paths are simplified to balance visual accuracy with fast web loading.
2. Robinson Projection: The world maps use the Robinson projection, which provides a more natural look for global data.
3. Clean Path IDs: Each `<path>` element is typically assigned an `id` corresponding to the ISO code of the region (e.g., `id="FR"` for France).
4. ViewBox Calibration: Maps are exported with consistent ViewBox settings, making them easy to scale in CSS.
5. Minimal Noise: Files do not contain excessive metadata, editor-specific tags, or hidden layers.
6. Consistent Nomenclature: Attributes like `name` or `title` are often included for basic accessibility and labeling.

### ViewBox and Scaling
SimpleMaps SVGs use the `viewBox` attribute rather than hardcoded `width` and `height` attributes in the root `<svg>` tag. This allows them to be responsive by default.
- Default behavior: Map fills the width of its parent container.
- CSS Control: Use `svg { width: 100%; height: auto; }` for fluid layouts.
- Aspect Ratio: The aspect ratio is preserved automatically by the browser's SVG renderer.

## 2. How to Download Programmatically

Automating the retrieval of these maps ensures consistency in build pipelines and data visualization projects.

### Using Command Line Tools
The `curl` command is the most direct way to fetch a map.

```bash
# Download the Robinson World Map
curl -o world.svg https://simplemaps.com/static/demos/resources/svg-library/svgs/world.svg

# Download the United States Map
curl -o usa.svg https://simplemaps.com/static/demos/resources/svg-library/svgs/us.svg

# Download the Europe Map
curl -o europe.svg https://simplemaps.com/static/demos/resources/svg-library/svgs/europe.svg
```

You can also use `wget` for similar results:
```bash
wget -O world.svg https://simplemaps.com/static/demos/resources/svg-library/svgs/world.svg
```

### Bulk Download Script (Bash)
To download all major continent maps at once:

```bash
#!/bin/bash
MAPS=("world" "us" "europe" "africa" "north_america" "south_america" "asia" "oceania")
BASE_URL="https://simplemaps.com/static/demos/resources/svg-library/svgs/"

for map in "${MAPS[@]}"; do
    echo "Downloading $map..."
    curl -s -o "$map.svg" "$BASE_URL$map.svg"
done
```

### Using Python Requests
For Python-based automation, the `requests` library is the standard choice.

```python
import requests

def download_simplemap(map_name, output_path):
    base_url = "https://simplemaps.com/static/demos/resources/svg-library/svgs/"
    url = f"{base_url}{map_name}.svg"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {map_name} to {output_path}")
    else:
        print(f"Failed to download {map_name}. Status code: {response.status_code}")

# Usage
download_simplemap("world", "global_map.svg")
download_simplemap("us", "united_states.svg")
```

### Note on Country Map URLs
Unlike the primary world and continent maps, country-specific province maps are often hosted at unique paths that do not follow a strict filename pattern on the static server.
- Step 1: Query the resource page: `https://simplemaps.com/resources/svg-{iso2}`.
- Step 2: Parse the page content to find the `href` ending in `.svg`.
- Step 3: Download the discovered URL.

## 3. Natural Earth Data + MapShaper Pipeline

Natural Earth is a public domain map dataset available at 1:10m, 1:50m, and 1:110m scales. It is the gold standard for cartographic accuracy.

### Source Data
Website: https://www.naturalearthdata.com/
- 1:110m: Small scale, best for global overviews and thumbnails.
- 1:50m: Medium scale, suitable for most web-based world maps.
- 1:10m: Large scale, extremely detailed, best for specific regions or countries.

### Common Datasets
- `ne_110m_admin_0_countries.shp`: Land boundaries for all countries.
- `ne_50m_admin_1_states_provinces.shp`: First-level administrative divisions.
- `ne_10m_populated_places.shp`: Major cities and towns.

### The MapShaper Workflow
Natural Earth provides Shapefiles (`.shp`), which are not natively supported by browsers. MapShaper (https://mapshaper.org/) is the tool used to convert these to SVG.

#### Installation
```bash
npm install -g mapshaper
```

#### Conversion Commands
To convert a shapefile to an SVG with simplification (to reduce file size):

```bash
# Basic conversion
mapshaper ne_110m_admin_0_countries.shp -o format=svg

# Conversion with 15% simplification and specific output filename
mapshaper ne_50m_admin_0_countries.shp -simplify dp 15% -o world_detailed.svg

# Filter and reproject before exporting
mapshaper ne_50m_admin_0_countries.shp \
    -filter "CONTINENT == 'Africa'" \
    -proj mercator \
    -o africa_mercator.svg
```

### When to Use This Pipeline
- Custom Projections: If you need a Mercator, Albers, or Winkel Tripel projection, MapShaper can reproject the data before exporting to SVG.
- High Resolution: When standard web maps are too blurry for high-zoom applications.
- Feature Selection: If you only want to export specific features (e.g., only countries with a population over 1 million).

### Drawbacks
- Complexity: Requires local tooling and knowledge of GIS concepts.
- Large Files: Natural Earth data is dense; without aggressive simplification, SVG files can easily exceed 5MB.
- Manual IDs: Unlike SimpleMaps, you may need to specify which attribute in the shapefile should be used as the SVG `id` or `class`.

## 4. D3.js + TopoJSON Ecosystem

D3.js is the most powerful framework for data visualization. It relies heavily on TopoJSON, an extension of GeoJSON that encodes topology.

### Key NPM Packages
- `world-atlas`: Contains TopoJSON files for world countries and land.
- `us-atlas`: Contains TopoJSON files for US states, counties, and districts.

### Implementation Logic
D3 generates the SVG DOM elements dynamically in the browser based on the TopoJSON data and a projection function.

```javascript
// Example of how D3 uses these sources
const projection = d3.geoRobinson();
const path = d3.geoPath().projection(projection);

d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(data => {
    svg.append("g")
       .selectAll("path")
       .data(topojson.feature(data, data.objects.countries).features)
       .enter().append("path")
       .attr("d", path)
       .attr("class", "country");
});
```

### When to Use
- Interactive Web Maps: When you need zooming, panning, and dynamic data binding.
- Data-Driven Applications: When the map content depends on a live API.
- Non-Standard Projections: D3 supports hundreds of mathematical projections.

### Coordinate Transformation
When using D3, you often need to convert Latitude/Longitude coordinates to SVG x/y coordinates.
- Projection Function: `const [x, y] = projection([longitude, latitude]);`
- Drawing: Use these coordinates to place circles or icons on top of the generated map paths.

## 5. Other Open Sources

Beyond the major players, several other resources provide reliable SVG map data.

### Wikipedia / Wikimedia Commons
Website: https://commons.wikimedia.org/wiki/Category:SVG_maps
- Type: Crowd-sourced repository.
- Quality: Highly varied. Some are professional-grade, others are simplified sketches.
- License: Usually Public Domain or Creative Commons Attribution-ShareAlike.
- Pros: Excellent for historical maps and obscure administrative divisions.

### SimpleMaps Location Database (Secondary)
Website: https://simplemaps.com/data/world-cities
- Use Case: If you need to overlay dots on your SVG map for specific cities, use the "Basic" free database to get the Lat/Long coordinates.

## 6. Source Comparison Table

Choosing the right source depends on your technical constraints and the required visual fidelity.

| Feature | SimpleMaps | Natural Earth | D3 / TopoJSON | Wikimedia Commons |
|---------|------------|---------------|---------------|-------------------|
| License | MIT (Free) | Public Domain | BSD-3-Clause | Public Domain / CC-BY-SA |
| Format | SVG | SHP / GeoJSON | TopoJSON | SVG |
| Ease of Use | Very High | Medium | Low | Variable |
| Resolution | Web-Optimized | Variable | Variable | Variable |
| File Size | Small | Large | Very Small | Variable |
| Projections | Fixed | Unlimited | Unlimited | Fixed |
| Country Cov. | 200+ | All | All | Partial |
| Admin Levels | Level 1 | Levels 0, 1 | Levels 0, 1 | Variable |
| Dynamic Data | Manual | Manual | Native | Manual |

All sources above are fully free for both personal and commercial use.

### Selection Logic
- Use SimpleMaps if: You need a standard, fast-loading map of a country or the world for a website.
- Use Natural Earth if: You need specific projections or high-detail printing.
- Use D3 / TopoJSON if: You are building a complex, interactive dashboard with many data points.
- Use Wikimedia if: You need historical maps, obscure regions, or very specific administrative divisions.

## 7. Common Issues and Troubleshooting

### CORS Policy Failures
When fetching maps via JavaScript (`fetch` or D3), you may encounter Cross-Origin Resource Sharing (CORS) errors.
- Solution: Host the SVG files locally on your own server or use a CDN that supports CORS (like JSDelivr for npm packages).
- SimpleMaps Note: SimpleMaps.com does not explicitly support cross-origin fetching for all assets; downloading and hosting locally is the safest approach.

### Path Misalignment
If overlaying data points (like cities) on a map, they might appear shifted.
- Cause: Incorrect projection or mismatched center point.
- Solution: Ensure the latitude/longitude data is converted using the exact same projection parameters as the map itself.

### Oversized SVG Files
Large SVGs can slow down page rendering.
- Optimization: Use MapShaper with the `-simplify` flag or tools like SVGO (SVG Optimizer).
- Recommendation: For web display, world maps should ideally be under 200KB.

### Broken Path IDs
Some automated conversion tools mangle the `id` attributes.
- Fix: Use MapShaper's `-info` command to see available attributes, then use `-each 'id = ADM0_A3'` to map a specific database field to the SVG ID.

### Technical Disclaimer
SVG maps sourced from different providers may not share the same coordinate system or projection. When combining maps (e.g., overlaying city points on a country map), ensure that the base map and the overlays are calibrated to the same projection or use a library like D3 to handle the transformation.

### Final Note
All sources listed in this file are free for personal and commercial use. SimpleMaps (MIT), Natural Earth (Public Domain), D3/TopoJSON (BSD-3-Clause), and Wikimedia Commons (Public Domain / CC-BY-SA) impose no usage fees.
