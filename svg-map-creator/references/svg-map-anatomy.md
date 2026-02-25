# SVG Map Anatomy

Sources: SVG specification (W3C), SimpleMaps.com SVG library analysis, production SVG map inspection

This document details the structural conventions, element relationships, and identification schemas required for programmatic manipulation of geographic SVG maps. Understanding this anatomy is essential for correctly targeting regions, applying styles, and extending maps with dynamic data layers. This reference focuses on the standard established by SimpleMaps, which is the industry benchmark for interactive map development.

## 1. SVG Root Element
The `<svg>` element serves as the container and coordinate system definition for the entire map. It must include specific attributes to ensure correct rendering and cross-platform compatibility across browsers and GIS (Geographic Information System) software.

### 1.1 Required Attributes
| Attribute | Description | Typical Value |
|-----------|-------------|---------------|
| `xmlns` | The XML namespace for SVG. Required for XML parsers to identify the schema. | `http://www.w3.org/2000/svg` |
| `viewBox` | Defines the internal coordinate system of the map. Essential for scaling. | `0 0 [width] [height]` |
| `width` | Recommended display width. Often set to 100% for responsiveness. | `100%` or `2000` |
| `height` | Recommended display height. Usually calculated to maintain aspect ratio. | `857` |
| `version` | Specifies the SVG version. | `1.1` |
| `preserveAspectRatio` | How the map fits the container. | `xMidYMid meet` |

### 1.2 The viewBox Coordinate System
The `viewBox` attribute is the most critical component of map anatomy. It consists of four numbers: `min-x`, `min-y`, `width`, and `height`. 

Example: `viewBox="0 0 2000 857"`
- **Coordinate Space**: The map is drawn on a virtual canvas that is 2000 units wide and 857 units high.
- **Independence**: All path coordinates within the file are relative to this 2000x857 grid, regardless of the physical size of the SVG on the screen.
- **Scaling**: Scaling the map (e.g., to 500px wide) does not change these internal coordinates; the browser handles the translation.
- **Negative Coordinates**: In some maps, the `min-x` or `min-y` may be negative (e.g., `-100 -100 2000 857`). This shift is common when the map is centered on a specific meridian or if the projection creates a centered origin.

Maintain the aspect ratio defined by the `viewBox` to prevent geographic distortion. If the `viewBox` ratio differs from the CSS `width/height` ratio, the `preserveAspectRatio` attribute determines how the map fits the container.

## 2. Path Elements
In geographic SVGs, the `<path>` element is the primary unit of representation. Each territory, island, or administrative region is defined as a path.

### 2.1 The d Attribute Commands
The `d` attribute (path data) contains a series of commands that trace the outline of the region.

| Command | Name | Description |
|---------|------|-------------|
| `M x,y` | MoveTo | Starts a new sub-path at (x,y). |
| `L x,y` | LineTo | Draws a straight line to (x,y). |
| `H x` | Horizontal LineTo | Draws a horizontal line to x. |
| `V y` | Vertical LineTo | Draws a vertical line to y. |
| `C x1,y1, x2,y2, x,y` | CurveTo | Draws a cubic Bézier curve. |
| `S x2,y2, x,y` | Smooth CurveTo | Draws a smooth cubic Bézier curve. |
| `Q x1,y1, x,y` | Quadratic CurveTo | Draws a quadratic Bézier curve. |
| `T x,y` | Smooth Quadratic | Draws a smooth quadratic Bézier curve. |
| `A rx,ry...x,y` | Elliptical Arc | Draws an elliptical arc. |
| `Z` | ClosePath | Closes the current sub-path. |

### 2.2 Curve Command Details
Cubic Bézier curves (`C`) are used for complex natural coastlines. They require two control points. Quadratic curves (`Q`) are simpler and used for smoother, less detailed borders. When programmatic scripts simplify paths, they often convert `C` commands to `L` or `Q` to reduce file size.

## 3. Identification Conventions
Targeting countries for data visualization requires a consistent identification schema. SimpleMaps utilizes a hybrid approach using `id`, `class`, and custom `name` attributes.

### 3.1 Targeting Framework
| Attribute | Scope | Consistency | Use Case |
|-----------|-------|-------------|----------|
| `id` | Element | High (Unique) | Direct CSS selection or specific territory targeting. |
| `class` | Document | Medium (Shared) | Grouping multiple paths (islands) into one country. |
| `name` | Human | Medium (Label) | Displaying text in tooltips or legend keys. |
| `data-id` | Metadata | High (Standard) | Cross-referencing with external datasets. |

### 3.2 ID vs. Class Distinction
- **ID Attribute**: Use for 1-to-1 mapping. An ID must be unique within the SVG document. If a country like France is represented by one path, `id="FR"` is applied to that single path.
- **Class Attribute**: Use for 1-to-many mapping. If a country like Japan consists of several separate island paths, each path receives `class="Japan"`. IDs cannot be reused for multiple elements.

## 4. Multi-Path Countries
Automated scripts must check for both `id` and `class` when searching for a country. The following table identifies major countries in the `world.svg` standard that utilize multi-path class grouping.

| Country Name | Primary Attribute | Reason for Multiple Paths |
|--------------|-------------------|--------------------------|
| Canada | `class` | Extensive Arctic archipelago and coastal islands. |
| United Kingdom | `class` | Separation of Great Britain, Northern Ireland, and Hebrides. |
| United States | `class` | Non-contiguous territories including Alaska and Hawaii. |
| Australia | `class` | Mainland Australia plus Tasmania and coastal islands. |
| Greece | `class` | Fragmented geography across the Aegean and Ionian seas. |
| Denmark | `class` | The Jutland peninsula plus Zealand, Funen, and Lolland. |
| Argentina | `class` | Inclusion of Tierra del Fuego and southern island chains. |
| China | `class` | Mainland China plus Hainan Island and coastal territories. |
| Japan | `class` | Primary archipelago structure (Honshu, Hokkaido, etc.). |
| Indonesia | `class` | Thousands of islands forming a fragmented state. |
| Philippines | `class` | Archipelagic structure with 7,000+ islands. |
| Angola | `class` | Inclusion of the Cabinda exclave separated by DR Congo. |
| Azerbaijan | `class` | Inclusion of the Nakhchivan exclave separated by Armenia. |
| Spain | `class` | Mainland plus Balearic Islands and Canary Islands. |
| Italy | `class` | Mainland plus Sicily, Sardinia, and Elba. |
| Norway | `class` | Extensive fjord system and coastal islands. |
| Russia | `class` | Massive coastline and various exclaves/islands. |
| France | `class` | Mainland plus Corsica and overseas departments. |
| Mexico | `class` | Mainland plus Cozumel and coastal islands. |
| New Zealand | `class` | North Island, South Island, and Stewart Island. |

## 5. Style Conventions
SVG styles can be applied via inline attributes or CSS-like strings. SimpleMaps defaults to a clean, minimalist style.

### 5.1 Default Visual Properties
- **Fill**: Default is often `#ececec` (light gray).
- **Stroke**: Default is `#ffffff` (white) or `#000000` (black).
- **Stroke Width**: Usually `0.75` to `1.5` in internal units.

### 5.2 Implementation Methods
**Direct Attributes:**
```xml
<path id="DE" fill="#ff0000" stroke="#000000" stroke-width="1" ... />
```

**Inline Style String:**
```xml
<path id="DE" style="fill:#ff0000;stroke:#000000;stroke-width:1" ... />
```

## 6. Namespace Handling
SVG is a dialect of XML. When using strict XML parsers, the namespace must be explicitly handled.

### 6.1 Python ElementTree Pattern
```python
import xml.etree.ElementTree as ET

namespaces = {
    'svg': 'http://www.w3.org/2000/svg',
    'xlink': 'http://www.w3.org/1999/xlink'
}

for prefix, uri in namespaces.items():
    ET.register_namespace(prefix, uri)

tree = ET.parse('map.svg')
root = tree.getroot()
paths = root.findall('.//svg:path', namespaces)
```

## 7. Country-Level vs. Province-Level SVGs
The hierarchy determines the identification standard used for sub-regions.

### 7.1 Identification Standards Table
| Map Level | Common Unit | Primary ID Schema | Example |
|-----------|-------------|-------------------|---------|
| World | Sovereign State | ISO 3166-1 alpha-2 | `id="US"` |
| USA | State | 2-Letter Postal | `id="TX"` |
| Canada | Province | 2-Letter Code | `id="ON"` |
| Germany | Land (State) | ISO 3166-2:DE | `id="DE-BY"` |
| UK | County/Region | ISO 3166-2:GB | `id="GB-KEN"` |
| France | Department | FIPS / INSEE | `id="FR-75"` |

## 8. Adding Elements
Maps often require additional layers for labels, markers, or legends.

### 8.1 Primitive Elements
- `<circle>`: Ideal for city markers (`cx`, `cy`, `r`).
- `<text>`: Essential for labels (`x`, `y`).
- `<rect>`: Used for legends or scale bars.
- `<line>`: Used for connectors or leader lines.

### 8.2 Grouping with <g>
```xml
<g id="capitals" fill="red">
    <circle cx="1200" cy="450" r="3" />
    <circle cx="1050" cy="510" r="3" />
</g>
```

## 9. Z-Index and Layering
SVG layering is strictly determined by the order of elements in the DOM.
- **Bottom Layer**: Backgrounds and oceans (first children).
- **Middle Layer**: Land masses and country paths.
- **Top Layer**: Labels, markers, and tooltips (last children).

## 10. Handling Tiny Territories
City-states (Singapore, Monaco) are often replaced with a `<circle>` or a small, standardized square path.
```xml
<circle id="SG" name="Singapore" cx="1500.5" cy="600.2" r="2" fill="#ececec" />
```

## 11. Projection and Distortion
- **Equirectangular**: Lat/long mapped directly to x/y.
- **Mercator**: Preserves angles but distorts area at high latitudes.

## 12. Dynamic Styling with CSS Variables
```xml
<svg style="--highlight-color: #ff0000;">
    <path id="FR" style="fill: var(--highlight-color);" />
</svg>
```

## 13. Zooming and Viewport Calculations
To implement a "zoom to country" feature, you must update the `viewBox` attribute.
- **Target**: A country path with bounding box `(minX, minY, width, height)`.
- **Padding**: Add 10-20% padding to the bounding box to prevent the country from touching the edges.
- **Aspect Ratio**: Adjust the calculated bounding box to match the original aspect ratio of the SVG container to prevent stretching.
- **Transformation**: Calculate the new `viewBox` as `[minX - pad, minY - pad, width + 2*pad, height + 2*pad]`.

## 14. Color Theory for Map Structure
When applying colors to the SVG structure, follow these cartographic standards:
- **Qualitative**: Distinct colors for distinct entities (e.g., political maps).
- **Sequential**: Gradient of a single hue for intensity (e.g., population density).
- **Diverging**: Two hues with a neutral center (e.g., election results or temperature anomalies).

## 15. Advanced CSS-in-SVG Patterns
You can embed complex CSS within the `<defs>` or `<style>` block of an SVG for advanced interactivity.

### 15.1 State-Based Styling
```xml
<style>
    path { transition: fill 0.3s, stroke 0.3s; }
    path.active { fill: #2ecc71; stroke: #27ae60; stroke-width: 2; }
    path.inactive { fill: #ecf0f1; pointer-events: none; }
    path:hover { filter: brightness(90%); }
</style>
```

### 15.2 SVG Filters for Visual Polish
Use filters for shadow or glow effects without increasing path complexity.
```xml
<defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="3" />
        <feOffset dx="2" dy="2" result="offsetblur" />
        <feComponentTransfer>
            <feFuncA type="linear" slope="0.5" />
        </feComponentTransfer>
        <feMerge>
            <feMergeNode />
            <feMergeNode in="SourceGraphic" />
        </feMerge>
    </filter>
</defs>
<path id="US" filter="url(#shadow)" ... />
```

## 16. Coordinate Math Implementation
When calculating a centroid from path data, follow this pseudo-algorithm:
1. Initialize `minX, minY` to Infinity and `maxX, maxY` to -Infinity.
2. Tokenize the `d` attribute string into commands and coordinates.
3. For each coordinate pair `(x, y)`:
   - Update `minX = min(minX, x)`, `maxX = max(maxX, x)`.
   - Update `minY = min(minY, y)`, `maxY = max(maxY, y)`.
4. Calculate `centerX = (minX + maxX) / 2`.
5. Calculate `centerY = (minY + maxY) / 2`.
6. Return `(centerX, centerY)` for marker placement.

## 17. Structural Anti-Patterns
- **Nested SVGs**: complicates coordinate math.
- **Individual Path Transforms**: makes centroid calculation difficult.
- **Empty Paths**: clutters the DOM and slows down queries.
- **Duplicate IDs**: causes selector collisions in CSS and JS.
- **Hardcoded Pixels**: Use relative units or viewBox units instead of absolute `px` values.

## 18. Metadata and Accessibility
```xml
<svg role="img" aria-label="World Map" ...>
    <title>World Map</title>
    <desc>SimpleMaps standard world map with ISO alpha-2 codes.</desc>
    <!-- Map Content -->
</svg>
```

## 19. Summary of Geographic ID Standards
The following table summarizes the ID naming conventions used for internal territories in major countries supported by SimpleMaps.

| Country | Internal Unit | Standard Used | Example ID |
|---------|---------------|---------------|------------|
| USA | States | US Postal | `AL`, `CA`, `NY` |
| Canada | Provinces | CA Postal | `AB`, `BC`, `ON` |
| UK | Regions | ISO 3166-2:GB | `GB-LND` (London) |
| Germany | States (Länder) | ISO 3166-2:DE | `DE-BE` (Berlin) |
| France | Departments | INSEE Codes | `75`, `92`, `13` |
| Australia | States/Territories | AU Standard | `NSW`, `QLD`, `VIC` |
| Brazil | States | ISO 3166-2:BR | `BR-SP`, `BR-RJ` |
| India | States/UTs | ISO 3166-2:IN | `IN-MH`, `IN-DL` |
| China | Provinces | ISO 3166-2:CN | `CN-BJ`, `CN-SH` |
| Mexico | States | ISO 3166-2:MX | `MX-CMX`, `MX-JAL` |
