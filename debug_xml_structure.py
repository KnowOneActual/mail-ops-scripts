#!/usr/bin/env python3
"""Diagnostic script to inspect DMARC XML structure and locate envelope_to field"""

import glob
import gzip
import sys
import xml.etree.ElementTree as ET
import zipfile


def inspect_xml(file_path):
    """Inspect the XML structure and print all elements"""
    tree = None

    try:
        if file_path.endswith(".gz"):
            with gzip.open(file_path, "rb") as f:
                tree = ET.parse(f)
        elif file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as z:
                xml_files = [n for n in z.namelist() if n.lower().endswith(".xml")]
                if not xml_files:
                    return
                with z.open(xml_files[0]) as f:
                    tree = ET.parse(f)
        else:
            tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    print(f"\n{'=' * 80}")
    print(f"File: {file_path}")
    print(f"{'=' * 80}")

    # Print all unique element paths
    def get_all_paths(element, prefix=""):
        paths = set()
        paths.add(f"{prefix}{element.tag}")
        for child in element:
            child_paths = get_all_paths(child, f"{prefix}{element.tag}/")
            paths.update(child_paths)
        return paths

    all_paths = get_all_paths(root)
    for path in sorted(all_paths):
        print(f"  {path}")

    # Specifically look for envelope_to
    print("\n🔍 Searching for 'envelope_to'...")
    found = False

    # Try different possible locations
    searches = [
        ".//envelope_to",
        ".//envelope/to",
        ".//policy_published/envelope_to",
        ".//row/envelope_to",
        ".//identifiers/envelope_to",
    ]

    for search_path in searches:
        result = root.findtext(search_path)
        if result:
            print(f"  ✅ Found at '{search_path}': {result}")
            found = True

    if not found:
        print("  ❌ 'envelope_to' not found in any expected location")
        print("\n📋 First record structure sample:")
        first_record = root.find(".//record")
        if first_record is not None:
            print(ET.tostring(first_record, encoding="unicode")[:500])


if __name__ == "__main__":
    xml_files = (
        glob.glob("*.xml")
        + glob.glob("reports/*.xml")
        + glob.glob("*.gz")
        + glob.glob("reports/*.gz")
        + glob.glob("*.zip")
        + glob.glob("reports/*.zip")
    )

    if not xml_files:
        print("❌ No XML files found. Run 'mailops fetch' first!")
        sys.exit(1)

    print(f"\n📊 Found {len(xml_files)} XML files. Inspecting first 3...\n")

    for xml_file in xml_files[:3]:
        inspect_xml(xml_file)
