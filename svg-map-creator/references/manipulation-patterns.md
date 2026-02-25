# SVG Map Manipulation Patterns

Sources: Python xml.etree.ElementTree docs, SVG specification, simplemaps convention analysis, D3.js patterns

Covers: Python and JavaScript patterns for coloring regions, handling namespaces, multi-path targeting, adding elements, extracting sub-regions, modifying viewBox, CSS-based styling.

## 1. Python: ElementTree Approach

The `xml.etree.ElementTree` (ET) module is the standard for server-side SVG manipulation in Python. It provides a robust, tree-based API for navigating and modifying XML structures.

### CRITICAL: Namespace Management
SVG files use the XML namespace `http://www.w3.org/2000/svg`. If not handled correctly, ET will append a prefix like `ns0:` to every element (e.g., `<ns0:path>`), which breaks many SVG renderers.

```python
import xml.etree.ElementTree as ET

# ALWAYS register the SVG namespace before parsing or writing
ET.register_namespace('', 'http://www.w3.org/2000/svg')
```

### Style Parsing and Modification
Many SVG maps (like simplemaps) store colors inside a `style` attribute (e.g., `style="fill:#cccccc; stroke:#ffffff"`). Modifying this requires a parser to avoid overwriting other properties like stroke or opacity.

```python
def parse_style(style_str):
    """Converts style string to dictionary."""
    if not style_str:
        return {}
    pairs = [p.split(':') for p in style_str.split(';') if ':' in p]
    return {k.strip(): v.strip() for k, v in pairs}

def stringify_style(style_dict):
    """Converts dictionary back to style string."""
    return "; ".join([f"{k}:{v}" for k, v in style_dict.items()])

def set_style_fill(element, color):
    """Sets fill color handling both style attribute and direct fill attribute."""
    # 1. Check style attribute first
    style_attr = element.get('style')
    if style_attr:
        style_dict = parse_style(style_attr)
        style_dict['fill'] = color
        element.set('style', stringify_style(style_dict))
    
    # 2. Also set/update direct fill attribute for compatibility
    element.set('fill', color)
```

### Finding and Coloring Paths
Paths are typically targeted by their `id` (standard ISO codes) or `class` (for grouping multi-part regions).

```python
def color_region(root, target_id, color):
    # Namespace handling for search
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Target by ID
    for path in root.findall('.//svg:path', ns):
        if path.get('id') == target_id:
            set_style_fill(path, color)
        
        # Target by class (useful for multi-part regions)
        cls = path.get('class', '')
        if target_id in cls.split():
            set_style_fill(path, color)
```

### Complete Working Example
```python
import xml.etree.ElementTree as ET

def process_map(input_file, output_file, coloring_data):
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    tree = ET.parse(input_file)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    for path in root.findall('.//svg:path', ns):
        path_id = path.get('id')
        path_class = path.get('class', '')
        
        # Check if this path should be colored
        for target, color in coloring_data.items():
            if path_id == target or target in path_class.split():
                set_style_fill(path, color)

    # Use xml_declaration=True to ensure proper file headers
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

# Usage
data = {'US': '#3b82f6', 'CA': '#ef4444', 'MX': '#10b981'}
process_map('world.svg', 'colored_world.svg', data)
```

## 2. Python: Batch Coloring from Data

Processing large datasets (JSON/CSV) requires an efficient lookup strategy. Instead of iterating the tree for every data point, iterate the tree once and check against the data.

```python
import json

def color_map_from_json(svg_path, json_data_path, output_path):
    with open(json_data_path, 'r') as f:
        data = json.load(f) # Format: {"US": "#ff0000", ...}

    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    for path in root.findall('.//svg:path', ns):
        p_id = path.get('id')
        p_classes = path.get('class', '').split()
        
        # Check ID match
        if p_id in data:
            set_style_fill(path, data[p_id])
            continue
            
        # Check Class match (for multi-path countries)
        for cls in p_classes:
            if cls in data:
                set_style_fill(path, data[cls])
                break

    tree.write(output_path, encoding='utf-8', xml_declaration=True)
```

## 3. Python: Adding SVG Elements

Adding annotations, legends, or labels requires creating new elements with proper namespaces.

### Creating a Legend
```python
def add_legend_item(root, x, y, color, label):
    ns_prefix = '{http://www.w3.org/2000/svg}'
    
    # Create group for the legend item
    g = ET.SubElement(root, f'{ns_prefix}g', attrib={'class': 'legend-item'})
    
    # Add colored rectangle
    ET.SubElement(g, f'{ns_prefix}rect', attrib={
        'x': str(x),
        'y': str(y),
        'width': '20',
        'height': '20',
        'fill': color,
        'stroke': '#000000',
        'stroke-width': '0.5'
    })
    
    # Add text label
    text = ET.SubElement(g, f'{ns_prefix}text', attrib={
        'x': str(x + 30),
        'y': str(y + 15),
        'font-family': 'Arial, sans-serif',
        'font-size': '12',
        'fill': '#333333'
    })
    text.text = label
```

### Adding Data Labels
```python
def add_label(root, x, y, text_content):
    ns_prefix = '{http://www.w3.org/2000/svg}'
    label = ET.SubElement(root, f'{ns_prefix}text', attrib={
        'x': str(x),
        'y': str(y),
        'font-size': '14',
        'font-weight': 'bold',
        'text-anchor': 'middle', # Horizontal centering
        'dominant-baseline': 'middle' # Vertical centering
    })
    label.text = text_content

### Creating Connector Lines
Useful for linking labels to small regions or islands.

```python
def add_connector(root, x1, y1, x2, y2, color='#666666'):
    ns_prefix = '{http://www.w3.org/2000/svg}'
    line = ET.SubElement(root, f'{ns_prefix}line', attrib={
        'x1': str(x1),
        'y1': str(y1),
        'x2': str(x2),
        'y2': str(y2),
        'stroke': color,
        'stroke-width': '1',
        'stroke-dasharray': '2,2' # Optional dashed line
    })
```

## 4. Python: Grouping Elements


Grouping elements with the `<g>` tag is useful for applying transformations (scale, rotate, translate) to multiple paths at once or for logical organization.

```python
def group_paths_by_region(root, region_name, path_ids):
    """Wraps specific paths in a new <g> element."""
    ns_prefix = '{http://www.w3.org/2000/svg}'
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Create the group
    group = ET.Element(f'{ns_prefix}g', attrib={'id': region_name, 'class': 'region-group'})
    
    # Find parents of paths to handle removal correctly
    parent_map = {c: p for p in root.iter() for c in p}
    
    paths_found = []
    for path in root.findall('.//svg:path', ns):
        if path.get('id') in path_ids:
            paths_found.append(path)
            
    for path in paths_found:
        parent = parent_map.get(path)
        if parent is not None:
            parent.remove(path)
            group.append(path)
            
    root.append(group)

# Usage: Group Scandinavia
# group_paths_by_region(root, 'Scandinavia', ['NO', 'SE', 'DK', 'FI'])
```

## 5. Python: Extracting Sub-Region

To create a map of just "Western Europe" from a world map, you must isolate specific paths and ideally adjust the coordinate system.

### Isolation Strategy (The "Hide" Approach)
The simplest way to extract a region without recalculating complex path data is to set non-target paths to `display:none` or `fill:none; stroke:none`.

```python
def isolate_regions(svg_path, keep_ids, output_path):
    # CRITICAL for output formatting
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Find all paths first
    all_paths = root.findall('.//svg:path', ns)
    
    # Track paths to remove
    to_remove = []
    for path in all_paths:
        p_id = path.get('id')
        p_classes = path.get('class', '').split()
        
        should_keep = (p_id in keep_ids) or any(cls in keep_ids for cls in p_classes)
        
        if not should_keep:
            to_remove.append(path)
                
    # Use parent map for safe removal
    parent_map = {c: p for p in root.iter() for c in p}
    for path in to_remove:
        parent = parent_map.get(path)
        if parent is not None:
            parent.remove(path)
                
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
```

### Bounding Box Calculation (Conceptual)
While calculating an exact bounding box from complex path strings (`d` attribute) requires a parser like `svgpath2mpl` or `svgelements`, you can often approximate by checking the `id` and `viewBox` of regional maps provided by sources like simplemaps.

```python
def calculate_approx_viewbox(root, target_ids):
    """
    In a real implementation, you would parse the 'd' attribute 
    of all target_ids to find min_x, min_y, max_x, max_y.
    """
    # Placeholder for logic using 'svgelements' library
    # import svgelements
    # paths = [svgelements.Path(p.get('d')) for p in target_paths]
    # bbox = svgelements.Group(paths).bbox()
    pass
```

## 6. Python: Modifying ViewBox

The `viewBox` attribute defines the visible area of the SVG canvas. It takes four values: `min-x min-y width height`.

### Zooming and Cropping
By modifying these values, you can "zoom in" on a specific region.

```python
def set_viewbox(root, x, y, w, h):
    root.set('viewBox', f"{x} {y} {w} {h}")
    # Ensure width and height attributes don't conflict
    if 'width' in root.attrib: del root.attrib['width']
    if 'height' in root.attrib: del root.attrib['height']
```

### Common Region Ranges (Simplemaps World Map)
The standard simplemaps `world.svg` (2000x857 units) uses these approximate ranges:

| Region | min-x | min-y | width | height |
| :--- | :--- | :--- | :--- | :--- |
| World (Full) | 0 | 0 | 2000 | 857 |
| North America | 100 | 100 | 550 | 350 |
| South America | 450 | 450 | 350 | 400 |
| Europe | 850 | 100 | 450 | 350 |
| Africa | 900 | 300 | 350 | 400 |
| Asia | 1200 | 150 | 600 | 400 |
| Oceania | 1500 | 550 | 450 | 300 |

## 6. JavaScript: DOM Approach

In a browser or Node.js (with `jsdom`), you can manipulate the SVG using standard DOM methods.

### Inline Manipulation
```javascript
// Target by ID
const usPath = document.querySelector('path#US');
if (usPath) {
    usPath.style.fill = '#3b82f6';
}

// Target all parts of a country by class
document.querySelectorAll('path.Canada').forEach(path => {
    path.setAttribute('fill', '#ef4444');
});
```

### Server-Side with JSDOM
```javascript
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const fs = require('fs');

const svgContent = fs.readFileSync('map.svg', 'utf8');
const dom = new JSDOM(svgContent, { contentType: "image/svg+xml" });
const document = dom.window.document;

// Manipulate
const path = document.getElementById('FR');
path.setAttribute('fill', 'blue');

// Export
const result = document.documentElement.outerHTML;
fs.writeFileSync('output.svg', result);
```

## 7. CSS-Based Styling Alternative

Instead of modifying every path's attributes, you can inject a `<style>` block. This is highly efficient for dynamic maps.

```python
def inject_css_styles(root, style_dict):
    """
    style_dict example: {"#US": "fill: blue", ".Europe": "fill: green"}
    """
    ns_prefix = '{http://www.w3.org/2000/svg}'
    style_el = ET.SubElement(root, f'{ns_prefix}style')
    
    css_lines = []
    for selector, rules in style_dict.items():
        css_lines.append(f"{selector} {{ {rules} }}")
    
    # Add hover effects
    css_lines.append("path:hover { fill-opacity: 0.7; cursor: pointer; transition: 0.2s; }")
    
    style_el.text = "\n".join(css_lines)
```

### Advantage of CSS
- **Performance**: Browser handles the coloring logic.
- **Interactivity**: Easy to add transitions and hover states.
- **Cleanliness**: The SVG path data remains untouched.

## 8. Common Pitfalls Table

| Pitfall | Cause | Fix |
| :--- | :--- | :--- |
| Namespace prefix `ns0:` | Failed to register SVG namespace before ET operations. | Call `ET.register_namespace('', 'http://www.w3.org/2000/svg')`. |
| Colors not applying | Conflicting `style` and `fill` attributes. | Use the `set_style_fill` helper to update both or prioritize one. |
| Multi-path regions partially colored | Only matched the `id` (e.g. "US") and missed islands (class "US"). | Always check both `id` and `class` attributes when coloring. |
| SVG not rendering | Malformed XML (e.g. missing closing tags after text manipulation). | Use a proper XML parser (ET/JSDOM) instead of regex/string replace. |
| File size bloated | Keeping hidden paths or high-precision coordinates. | Use `parent.remove(element)` to physically delete unwanted regions. |
| Labels misaligned | Wrong `text-anchor` or `dominant-baseline` settings. | Use `text-anchor="middle"` for horizontal and `dominant-baseline="middle"` for vertical. |
| Coordinates off | Not accounting for SVG coordinate system (y increases downward). | Remember 0,0 is top-left. South America has higher Y values than North America. |
