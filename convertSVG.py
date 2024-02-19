import xml.etree.ElementTree as ET
import json
import sys

import xml.etree.ElementTree as ET

def load_svg(path):
    try:
        # Parse the SVG file using ElementTree
        tree = ET.parse(path)
        # Get the root element of the XML tree
        root = tree.getroot()
        # Return the root element
        return root
    except ET.ParseError as e:
        # Handle any parse errors that might occur
        print(f"Error while loading SVG file: {e}")
        return None

def svg_to_json(root_svg):
    svg_data = {
        "height": int(float(root_svg.get("height", ""))),
        "width": int(float(root_svg.get("width", ""))),
        "shapes": []
    }

    id_counter = 0

    # Process polygon elements in SVG
    for polygon in root_svg.findall(".//{http://www.w3.org/2000/svg}polygon"):
        fill_color = polygon.get("fill", "")
        stroke_color = polygon.get("stroke", "none")

        # Change stroke to "grey" for objects with fill "#727171"
        if fill_color == "#727171":
            stroke_color = "grey"

        # Parse points and save as tuples
        points = polygon.get("points", "").split()
        points = [tuple(map(lambda x: int(float(x)), point.split(","))) for point in points]

        # Create an object representing a room
        room = {
            "id": id_counter,
            "fill": fill_color,
            "stroke": stroke_color,
            "points": points
        }

        # Add the room object to the list of shapes in SVG data
        svg_data["shapes"].append(room)
        id_counter += 1

    return svg_data

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_svg_path> <output_json_path>")
        sys.exit(1)

    svg_path = sys.argv[1]
    json_path = sys.argv[2]

    svg_root = load_svg(svg_path)

    if svg_root:
        json_data = svg_to_json(svg_root)

        # Save to JSON file
        with open(json_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)

        print(f"SVG data saved to JSON file: {json_path}")
    else:
        print("Error while loading SVG file.")

if __name__ == "__main__":
    main()
