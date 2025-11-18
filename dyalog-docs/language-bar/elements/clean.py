import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def remove_attributes(element):
    """Recursively remove all attributes from XML elements,
       except on the html tag: if a MadCap:conditions attribute is present,
       preserve it (without the namespace) and strip a leading "default.".
    """
    if element.tag == "html":
        new_attrib = {}
        for attr, value in element.attrib.items():
            # Determine the local name (i.e. without namespace or prefix)
            if attr.startswith('{'):
                # e.g. "{http://...}conditions"
                local = attr.split('}', 1)[1]
            elif ':' in attr:
                # e.g. "MadCap:conditions"
                local = attr.split(':', 1)[1]
            else:
                local = attr
            # If this attribute is "conditions", preserve it
            if local == "conditions":
                # Remove the "default." prefix if present.
                if value.startswith("default."):
                    value = value[len("default."):]
                new_attrib["conditions"] = value
        element.attrib = new_attrib
    else:
        # For non-html elements, remove all attributes.
        element.attrib.clear()
    
    # Process child elements recursively.
    for child in element:
        remove_attributes(child)

def process_file(file_path):
    """Process a single HTM file to remove XML attributes as specified."""
    try:
        # Read the original file content.
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove any existing XML declaration.
        content = re.sub(r'<\?xml[^>]*\?>\s*', '', content)
        
        # Parse the XML content.
        tree = ET.ElementTree(ET.fromstring(content))
        root = tree.getroot()
        
        # Remove attributes (with special handling for html tag).
        remove_attributes(root)
        
        # Convert back to string.
        processed_content = ET.tostring(root, encoding='unicode', method='xml')
        
        # Add the standard XML declaration.
        processed_content = '<?xml version="1.0" encoding="utf-8"?>\n' + processed_content
        
        # Create backup of original file.
        backup_path = file_path.with_suffix(file_path.suffix + '.backup')
        Path(file_path).rename(backup_path)
        
        # Write new content.
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
            
        print(f"Processed {file_path}")
        print(f"Original file backed up to {backup_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def main():
    """Process all .htm files in the current directory."""
    current_dir = Path('.')
    htm_files = list(current_dir.glob('*.htm'))
    
    if not htm_files:
        print("No .htm files found in the current directory.")
        return
    
    print(f"Found {len(htm_files)} .htm files to process.")
    
    for file_path in htm_files:
        process_file(file_path)
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()