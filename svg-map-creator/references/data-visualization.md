# Data Visualization for SVG Maps

Sources: ColorBrewer 2.0 (Cynthia Brewer), cartographic visualization best practices, SVG specification

Scope: Covers: choropleth design principles, color scale types and selection, ColorBrewer palettes with hex codes, legend SVG construction, label placement, title/annotation patterns, responsive SVG, accessibility, common mistakes.

## Choropleth Map Design Principles

A choropleth map is a thematic map in which areas are shaded or patterned in proportion to the measurement of the statistical variable being displayed on the map, such as population density or per-capita income.

### Data Classification Methods

Choosing the right classification method is critical for accurately representing the underlying data distribution.

1. Equal Interval:
   - Method: Divides the range of data values into equal-sized sub-ranges.
   - Best for: Data that is uniformly distributed. It is easy for users to understand the steps (e.g., 0-10, 10-20, 20-30).
   - Drawback: Can result in many empty classes if data is skewed.

2. Quantile (Equal Count):
   - Method: Places an equal number of observations into each class.
   - Best for: Data that is skewed or where relative ranking is more important than absolute value.
   - Drawback: Can group very different values together or separate very similar values if they fall on either side of a breakpoint.

3. Natural Breaks (Jenks):
   - Method: Uses an algorithm to group values that are similar and maximize the difference between classes.
   - Best for: Most data distributions, as it identifies real clusters in the data.
   - Drawback: Breakpoints can be non-intuitive (e.g., 3.4 to 12.1) and vary between different maps, making comparison difficult.

4. Manual/Defined Interval:
   - Method: User specifies exact thresholds based on domain knowledge or standard benchmarks.
   - Best for: Policy-driven maps (e.g., poverty lines) or standard comparative scales.

### Decision Table for Classification

| Distribution | Goal | Recommended Method |
|--------------|------|-------------------|
| Uniform | Simple progression | Equal Interval |
| Heavily Skewed | Show relative rank | Quantile |
| Clustered | Show natural groups | Jenks (Natural Breaks) |
| Standardized | Meet specific criteria | Manual |

### Number of Classes

- 3 classes: Best for very simple "Low/Medium/High" distinctions.
- 5 classes: The default "sweet spot" for human perception and map clarity.
- 7 classes: Maximum recommended for general audiences.
- 8+ classes: Often results in colors that are too similar for the eye to distinguish accurately.

## Color Scale Types

### Sequential Scales
Used for data that goes from low to high magnitude (all values are positive or zero).
- Examples: Population, GDP, Literacy Rate.
- Logic: Light colors represent low values; dark colors represent high values.

### Diverging Scales
Used for data where there is a meaningful midpoint or "neutral" value (often zero or an average), and data deviates in two directions.
- Examples: Population growth (Positive/Negative), Election results (Margin of Victory), Temperature deviation.
- Logic: Two distinct hues meet at a neutral light center.

### Categorical (Qualitative) Scales
Used for data that is nominal or categorical, where there is no inherent order.
- Examples: Country names, Continents, Political Parties, Biomes.
- Logic: Distinct hues with similar lightness and saturation to avoid implying hierarchy.

### Binary Scales
A subset of categorical scales used for "Yes/No" or "Present/Absent" data.
- Logic: Two highly contrasting colors.

| Data Type | Scale Type | Pattern |
|-----------|------------|---------|
| Quantitative (Positive) | Sequential | Single hue, light to dark |
| Quantitative (Deviating) | Diverging | Two hues, light center |
| Qualitative (Groups) | Categorical | Multiple distinct hues |
| Boolean (True/False) | Binary | Two contrasting hues |

## ColorBrewer Palettes (Exact Hex Codes)

Use these hex codes directly in the `fill` attribute of SVG path elements. For "no data" or missing regions, always use #d1d5db (Light Gray).

### Sequential Palettes

**Blues**
- 3-class: #deebf7, #9ecae1, #3182bd
- 5-class: #eff3ff, #bdd7e7, #6baed6, #3182bd, #08519c
- 7-class: #eff3ff, #c6dbef, #9ecae1, #6baed6, #4292c6, #2171b5, #084594

**Greens**
- 3-class: #e5f5e0, #a1d99b, #31a354
- 5-class: #edf8e9, #bae4b3, #74c476, #31a354, #006d2c
- 7-class: #edf8e9, #c7e9c0, #a1d99b, #74c476, #41ab5d, #238b45, #005a32

**Oranges**
- 3-class: #fee6ce, #fdae6b, #e6550d
- 5-class: #feedde, #fdbe85, #fd8d3c, #e6550d, #a63603
- 7-class: #feedde, #fdd0a2, #fdae6b, #fd8d3c, #f16913, #d94801, #8c2d04

**Reds**
- 3-class: #fee0d2, #fc9272, #de2d26
- 5-class: #fee5d9, #fcae91, #fb6a4a, #de2d26, #a50f15
- 7-class: #fee5d9, #fcbba1, #fc9272, #fb6a4a, #ef3b2c, #cb181d, #99000d

**Purples**
- 3-class: #efedf5, #bcbddc, #756bb1
- 5-class: #f2f0f7, #cbc9e2, #9e9ac8, #756bb1, #54278f
- 7-class: #f2f0f7, #dadaeb, #bcbddc, #9e9ac8, #807dba, #6a51a3, #4a1486

### Diverging Palettes (5-class)

**RdYlGn (Red-Yellow-Green)**
- 5-class: #d73027, #fc8d59, #ffffbf, #91cf60, #1a9850

**RdBu (Red-Blue)**
- 5-class: #ca0020, #f4a582, #f7f7f7, #92c5de, #0571b0

**BrBG (Brown-BlueGreen)**
- 5-class: #a6611a, #dfc27d, #f5f5f5, #80cdc1, #018571

### Categorical Palettes (8-class)

**Set2**
- #66c2a5, #fc8d62, #8da0cb, #e78ac3, #a6d854, #ffd92f, #e5c494, #b3b3b3

**Dark2**
- #1b9e77, #d95f02, #7570b3, #e7298a, #66a61e, #e6ab02, #a6761d, #666666

## Legend Construction in SVG

Legends should be grouped in a `<g>` element to allow for easy positioning and styling.

### Horizontal Legend Implementation
Position this at the bottom-left or bottom-center of the map view.

```xml
<g class="legend horizontal" transform="translate(50, 750)">
  <!-- Legend Title -->
  <text x="0" y="-15" font-family="Arial, sans-serif" font-size="14" font-weight="bold">GDP per Capita (USD)</text>
  
  <!-- Class 1 -->
  <rect x="0" y="0" width="40" height="20" fill="#eff3ff" stroke="#666" stroke-width="0.5" />
  <text x="0" y="35" font-family="Arial, sans-serif" font-size="10" text-anchor="start">0 - 10k</text>
  
  <!-- Class 2 -->
  <rect x="40" y="0" width="40" height="20" fill="#bdd7e7" stroke="#666" stroke-width="0.5" />
  <text x="40" y="35" font-family="Arial, sans-serif" font-size="10" text-anchor="start">10k - 25k</text>
  
  <!-- Class 3 -->
  <rect x="80" y="0" width="40" height="20" fill="#6baed6" stroke="#666" stroke-width="0.5" />
  <text x="80" y="35" font-family="Arial, sans-serif" font-size="10" text-anchor="start">25k - 50k</text>
  
  <!-- Class 4 -->
  <rect x="120" y="0" width="40" height="20" fill="#3182bd" stroke="#666" stroke-width="0.5" />
  <text x="120" y="35" font-family="Arial, sans-serif" font-size="10" text-anchor="start">50k - 75k</text>
  
  <!-- Class 5 -->
  <rect x="160" y="0" width="40" height="20" fill="#08519c" stroke="#666" stroke-width="0.5" />
  <text x="160" y="35" font-family="Arial, sans-serif" font-size="10" text-anchor="start">75k+</text>
</g>
```

### Vertical Legend Implementation
Useful for sidebars or maps with specific empty corners.

```xml
<g class="legend vertical" transform="translate(900, 100)">
  <text x="0" y="-15" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Legend</text>
  
  <g transform="translate(0, 0)">
    <rect width="20" height="20" fill="#edf8e9" />
    <text x="30" y="15" font-family="Arial, sans-serif" font-size="12">Very Low</text>
  </g>
  <g transform="translate(0, 25)">
    <rect width="20" height="20" fill="#bae4b3" />
    <text x="30" y="15" font-family="Arial, sans-serif" font-size="12">Low</text>
  </g>
  <g transform="translate(0, 50)">
    <rect width="20" height="20" fill="#74c476" />
    <text x="30" y="15" font-family="Arial, sans-serif" font-size="12">Medium</text>
  </g>
  <g transform="translate(0, 75)">
    <rect width="20" height="20" fill="#31a354" />
    <text x="30" y="15" font-family="Arial, sans-serif" font-size="12">High</text>
  </g>
</g>
```

### Python Programmatic Legend Generation

```python
def generate_legend_svg(classes, colors, title, x=50, y=750):
    svg_elements = [f'<g transform="translate({x}, {y})">']
    svg_elements.append(f'<text x="0" y="-10" font-family="Arial" font-size="14" font-weight="bold">{title}</text>')
    
    for i, (label, color) in enumerate(zip(classes, colors)):
        offset = i * 60
        rect = f'<rect x="{offset}" y="0" width="60" height="20" fill="{color}" stroke="#fff" />'
        text = f'<text x="{offset}" y="35" font-family="Arial" font-size="10">{label}</text>'
        svg_elements.extend([rect, text])
        
    svg_elements.append('</g>')
    return "\n".join(svg_elements)
```

## Title and Annotation

### Title Placement
The title should be the most prominent text element, usually centered at the top.
- Position: x="50%", y="40" (inside a 1000x800 viewBox)
- Styling: `font-size="24"`, `font-weight="bold"`, `text-anchor="middle"`

### Source Attribution
Always include the data source to establish credibility.
- Position: x="10", y="790"
- Styling: `font-size="10"`, `fill="#666"`

### Recommended Fonts
SVG maps benefit from clean sans-serif fonts that remain readable when scaled.
- "Segoe UI", Tahoma, Arial, Helvetica, sans-serif
- Avoid serif fonts like Times New Roman as they can appear cluttered at small sizes on screens.

## Label Placement

Labeling regions (countries/states) provides immediate context without requiring tooltips.

### Centroid Positioning
Labels should be centered on the largest visual part of a region's path.
- Rule: Do not attempt to calculate centroids dynamically in the frontend if performance is a concern.
- Strategy: Use a lookup table of precalculated label coordinates (ISO-Code -> {x, y}).
- Skip Small Territories: If a region's bounding box is smaller than the label text, do not render the label or use an abbreviation.

### Leader Lines for Small Regions
For small territories where a label won't fit (e.g., European microstates, Caribbean islands), use a leader line.
- Draw a path from the centroid to an empty space in the ocean.
- Place the text label at the end of the line.

## Responsive SVG

To ensure maps look good on all screen sizes, avoid hardcoded pixel dimensions.

### ViewBox and Aspect Ratio
The `viewBox` attribute defines the coordinate system. The `preserveAspectRatio` attribute defines how it scales.
- Correct: `<svg viewBox="0 0 1000 800" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">`
- Incorrect: `<svg width="1000" height="800">`

### CSS Integration
Set the SVG width to 100% and height to auto in CSS to make it fluid.
```css
svg {
  width: 100%;
  height: auto;
  max-width: 1200px;
}
```

## Accessibility

Maps are inherently visual, so extra effort is required for screen readers and color-blind users.

### Meta Elements
Include `<title>` and `<desc>` as the first children of the `<svg>` tag.
```xml
<svg ...>
  <title>Map of Global Literacy Rates 2024</title>
  <desc>A choropleth map showing literacy rates by country, with darker blues indicating higher rates.</desc>
</svg>
```

### Aria Labels
Apply `role="img"` to the SVG and `aria-label` to individual path elements.
```xml
<path d="..." fill="#08519c" role="img" aria-label="Norway: 99% Literacy" />
```

### Color Contrast
Ensure a minimum contrast ratio of 3:1 between adjacent regions if they represent different data classes. Use a white or light-gray stroke (#ffffff or #e5e7eb) to separate regions.

## Common Choropleth Mistakes

| Mistake | Why It's Bad | Fix |
|:---|:---|:---|
| Rainbow Color Scales | Perceptually non-uniform. Humans perceive yellow as brighter than blue even if values are equal. | Use sequential or diverging scales. |
| Too Many Classes | Human eye cannot distinguish between 10 shades of the same color accurately. | Limit classes to 3-7. |
| Using Raw Counts | Misleading. Larger regions often have higher counts naturally (e.g., total deaths vs. deaths per 100k). | Normalize data (per capita, per sq km, or percentage). |
| Missing Legend | Map becomes abstract art. Users cannot interpret the relationship between color and value. | Always include a clear legend with labels. |
| No "No Data" Color | Users might assume white or gray represents zero. | Use a specific "No Data" color (#d1d5db) and list it in the legend. |
| Overlapping Labels | Makes the map unreadable and unprofessional. | Use leader lines or skip labels for small regions. |
| Fixed Pixel Widths | Map breaks on mobile or overflows container. | Use viewBox and percentage widths. |
