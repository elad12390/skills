#!/usr/bin/env python3
"""
Color SVG Map Regions

Applies colors to SVG map regions based on JSON or CSV data files.
Supports both id-based and class-based path targeting for multi-path countries.

Usage:
    python3 color-svg-map.py -i world.svg -d data.json -o colored.svg
    python3 color-svg-map.py -i world.svg -d data.csv -o colored.svg --legend
    python3 color-svg-map.py -i world.svg -d data.json -o colored.svg --title "World Map"

Data Format (JSON):
    Simple: {"US": "#3b82f6", "CA": "#ef4444"}
    Extended: {"US": {"color": "#3b82f6", "label": "United States"}}

Data Format (CSV):
    code,color
    US,#3b82f6

    Or with labels:
    code,color,label
    US,#3b82f6,United States
"""

import xml.etree.ElementTree as ET
import json
import csv
import argparse
import sys
import os
import re

# Multi-path countries that use class attribute instead of id
MULTI_PATH_CLASSES = {
    "AO": "Angola",
    "AR": "Argentina",
    "AU": "Australia",
    "AZ": "Azerbaijan",
    "CA": "Canada",
    "CN": "China",
    "DK": "Denmark",
    "GR": "Greece",
    "GB": "United Kingdom",
}


def parse_data(data_path):
    """
    Parse JSON or CSV data file into a dictionary.

    Returns:
        dict: {code: {"color": hex, "label": str}}
    """
    ext = os.path.splitext(data_path)[1].lower()
    result = {}

    if ext == ".json":
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for code, value in data.items():
                if isinstance(value, str):
                    # Simple format: {"US": "#3b82f6"}
                    result[code] = {"color": value, "label": code}
                elif isinstance(value, dict):
                    # Extended format: {"US": {"color": "#3b82f6", "label": "..."}}
                    result[code] = {
                        "color": value.get("color", "#ececec"),
                        "label": value.get("label", code),
                    }

    elif ext == ".csv":
        with open(data_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row.get("code", "").strip()
                color = row.get("color", "#ececec").strip()
                label = row.get("label", code).strip()
                if code:
                    result[code] = {"color": color, "label": label}

    else:
        raise ValueError(f"Unsupported data format: {ext}. Use .json or .csv")

    return result


def parse_style(style_str):
    """
    Parse CSS style string into a dictionary.

    Args:
        style_str: CSS style string like "fill:#fff;stroke:#000"

    Returns:
        dict: {property: value}
    """
    styles = {}
    if not style_str:
        return styles

    for declaration in style_str.split(";"):
        declaration = declaration.strip()
        if ":" in declaration:
            prop, value = declaration.split(":", 1)
            styles[prop.strip()] = value.strip()

    return styles


def style_to_string(styles):
    """Convert style dictionary back to CSS string."""
    return ";".join(f"{k}:{v}" for k, v in styles.items())


def set_fill_color(element, color):
    """
    Set fill color on an SVG element.
    Handles both style attribute and fill attribute.

    Args:
        element: XML element
        color: Hex color string
    """
    style_attr = element.get("style")

    if style_attr:
        # Parse existing style and update fill
        styles = parse_style(style_attr)
        styles["fill"] = color
        element.set("style", style_to_string(styles))
    else:
        # Set fill attribute directly
        element.set("fill", color)


def add_legend(root, data, legend_x, legend_y, viewbox):
    """
    Add a legend to the SVG.

    Args:
        root: SVG root element
        data: Color data dictionary
        legend_x: X position
        legend_y: Y position (or None for auto)
        viewbox: Viewbox tuple (x, y, width, height)
    """
    # Get unique colors and their labels
    color_labels = {}
    for code, info in data.items():
        color = info["color"]
        label = info["label"]
        if color not in color_labels:
            color_labels[color] = label

    # Auto-calculate Y position if not provided
    if legend_y is None:
        _, _, _, vb_height = viewbox
        legend_y = vb_height - (len(color_labels) * 20 + 30)

    # Create legend group
    legend_group = ET.SubElement(root, "g")
    legend_group.set("id", "legend")

    # Add legend items
    y_offset = legend_y
    for color, label in sorted(color_labels.items(), key=lambda x: x[1]):
        # Color rectangle
        rect = ET.SubElement(legend_group, "rect")
        rect.set("x", str(legend_x))
        rect.set("y", str(y_offset))
        rect.set("width", "20")
        rect.set("height", "14")
        rect.set("fill", color)
        rect.set("stroke", "#333")
        rect.set("stroke-width", "0.5")

        # Label text
        text = ET.SubElement(legend_group, "text")
        text.set("x", str(legend_x + 25))
        text.set("y", str(y_offset + 11))
        text.set("font-family", "sans-serif")
        text.set("font-size", "12")
        text.set("fill", "#333")
        text.text = label

        y_offset += 20


def add_title(root, title_text, viewbox):
    """
    Add a title to the SVG.

    Args:
        root: SVG root element
        title_text: Title string
        viewbox: Viewbox tuple (x, y, width, height)
    """
    _, _, vb_width, _ = viewbox

    title = ET.SubElement(root, "text")
    title.set("x", str(vb_width / 2))
    title.set("y", "30")
    title.set("font-family", "sans-serif")
    title.set("font-size", "24")
    title.set("font-weight", "bold")
    title.set("fill", "#333")
    title.set("text-anchor", "middle")
    title.text = title_text


def get_viewbox(root):
    """
    Extract viewBox dimensions from SVG root.

    Returns:
        tuple: (x, y, width, height) or (0, 0, 800, 600) as default
    """
    viewbox_str = root.get("viewBox")
    if viewbox_str:
        parts = viewbox_str.split()
        if len(parts) == 4:
            return tuple(float(p) for p in parts)

    # Fallback to width/height attributes
    width = float(root.get("width", "800").replace("px", ""))
    height = float(root.get("height", "600").replace("px", ""))
    return (0, 0, width, height)


def color_map(
    input_path,
    data_path,
    output_path,
    default_color="#ececec",
    add_legend_flag=False,
    title_text=None,
    legend_x=50,
    legend_y=None,
):
    """
    Apply colors to SVG map regions based on data file.

    Args:
        input_path: Path to input SVG file
        data_path: Path to JSON or CSV data file
        output_path: Path to output SVG file
        default_color: Default fill color for unmatched regions
        add_legend_flag: Whether to add a legend
        title_text: Optional title text
        legend_x: X position for legend
        legend_y: Y position for legend (None for auto)

    Returns:
        dict: Statistics about the coloring operation
    """
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input SVG file not found: {input_path}")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")

    # Parse data
    data = parse_data(data_path)

    # Register SVG namespace to prevent ns0: prefix
    ET.register_namespace("", "http://www.w3.org/2000/svg")

    # Parse SVG
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Get viewbox for legend/title positioning
    viewbox = get_viewbox(root)

    # Track statistics
    colored_count = 0
    multi_path_count = 0
    matched_codes = set()

    # Build reverse lookup for multi-path countries
    class_to_code = {v: k for k, v in MULTI_PATH_CLASSES.items()}

    # Find all path elements (handle namespaced and non-namespaced)
    paths = root.findall(".//{http://www.w3.org/2000/svg}path")
    if not paths:
        paths = root.findall(".//path")

    # Color paths
    for path in paths:
        path_id = path.get("id", "").strip()
        path_class = path.get("class", "").strip()

        color = None
        matched_code = None

        # Check id attribute
        if path_id in data:
            color = data[path_id]["color"]
            matched_code = path_id

        # Check class attribute (for multi-path countries)
        elif path_class in class_to_code:
            code = class_to_code[path_class]
            if code in data:
                color = data[code]["color"]
                matched_code = code
                multi_path_count += 1

        # Apply color
        if color:
            set_fill_color(path, color)
            colored_count += 1
            matched_codes.add(matched_code)
        else:
            # Apply default color only if no fill is set
            current_fill = path.get("fill")
            current_style = path.get("style", "")

            # Check if path has no explicit fill
            if not current_fill and "fill:" not in current_style:
                set_fill_color(path, default_color)

    # Find unmatched codes
    unmatched_codes = set(data.keys()) - matched_codes

    # Add legend if requested
    if add_legend_flag:
        add_legend(root, data, legend_x, legend_y, viewbox)

    # Add title if provided
    if title_text:
        add_title(root, title_text, viewbox)

    # Write output
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    # Return statistics
    return {
        "colored": colored_count,
        "multi_path": multi_path_count,
        "unmatched": len(unmatched_codes),
        "unmatched_codes": sorted(unmatched_codes),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Apply colors to SVG map regions from JSON/CSV data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument("-i", "--input", required=True, help="Path to input SVG file")
    parser.add_argument(
        "-d", "--data", required=True, help="Path to data file (JSON or CSV)"
    )
    parser.add_argument("-o", "--output", required=True, help="Path to output SVG file")
    parser.add_argument(
        "--default-color",
        default="#ececec",
        help="Default fill color for unmatched regions (default: #ececec)",
    )
    parser.add_argument(
        "--legend", action="store_true", help="Include a legend in the output"
    )
    parser.add_argument("--title", help="Optional title text to add to the map")
    parser.add_argument(
        "--legend-x", type=float, default=50, help="X position for legend (default: 50)"
    )
    parser.add_argument(
        "--legend-y",
        type=float,
        help="Y position for legend (default: auto-calculated)",
    )

    args = parser.parse_args()

    try:
        stats = color_map(
            input_path=args.input,
            data_path=args.data,
            output_path=args.output,
            default_color=args.default_color,
            add_legend_flag=args.legend,
            title_text=args.title,
            legend_x=args.legend_x,
            legend_y=args.legend_y,
        )

        print(f"Success! Colored {stats['colored']} regions")
        if stats["multi_path"] > 0:
            print(f"  - {stats['multi_path']} multi-path regions")
        if stats["unmatched"] > 0:
            print(
                f"Warning: {stats['unmatched']} unmatched codes: {', '.join(stats['unmatched_codes'])}"
            )
        print(f"Output saved to: {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
