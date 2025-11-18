import json
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SymbolData:
    title: str       # From the <head>/<title> tag (or JSON entry title)
    char: str        # From the <head>/<char> tag
    content: str     # From the <body>/<pre> tag (raw text with newlines)
    conditions: str = ""   # The value from the html tag's "conditions" attribute, if any
    is_blank: bool = False  # True if the JSON entry has title "blank" and no link

def process_toc(toc_filename: str) -> list[SymbolData]:
    """Reads the toc.json file and processes each XML file specified by the 'link' attribute.
       For each file, it extracts title, char, content and, if present, conditions.
    """
    with open(toc_filename, 'r', encoding='utf-8') as f:
        toc_entries = json.load(f)
    
    symbols = []
    for entry in toc_entries:
        # For entries without a link:
        if "link" not in entry:
            if entry.get("title", "").strip().lower() == "blank":
                symbols.append(SymbolData(title="blank", char="", content="", is_blank=True))
            else:
                symbols.append(SymbolData(title=entry.get("title", ""), char="", content=""))
            continue
        
        xml_path = entry["link"]
        if not os.path.exists(xml_path):
            print(f"File not found: {xml_path}")
            continue
        
        try:
            with open(xml_path, 'r', encoding='utf-8') as xf:
                content = xf.read()
            tree = ET.ElementTree(ET.fromstring(content))
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing {xml_path}: {e}")
            continue

        head = root.find("head")
        xml_title = head.find("title").text if head is not None and head.find("title") is not None else ""
        xml_char = head.find("char").text if head is not None and head.find("char") is not None else ""
        
        body = root.find("body")
        pre_content = body.find("pre").text if body is not None and body.find("pre") is not None else ""
        
        # Record the conditions attribute from the root (if present)
        conditions = root.attrib.get("conditions", "")
        
        symbols.append(SymbolData(title=xml_title, char=xml_char, content=pre_content, conditions=conditions))
    
    return symbols

def escape_text(text: str) -> str:
    """
    Escapes backslashes and double quotes in the provided text.
    """
    # First escape backslashes, then escape double quotes.
    return text.replace('\\', '\\\\').replace('"', '\\"')

def format_symbol(symbol: SymbolData) -> str:
    """
    Formats a SymbolData instance in the required format.
    
    For non-blank entries, the output is:
    
    #if <conditions>    <-- only if conditions is non-empty
    NAME("<title>"),CHAR("<char>"),TIP(
                            _("<line 1>")
                            _("<line 2>")
                            ...
                            _("<last line>")
                            _("")
                            )
    #endif             <-- only if conditions is non-empty
    
    For blank entries, returns "BLANK".
    
    Each line in the content is processed:
      - Double quotes and backslashes are escaped.
      - If a line contains only whitespace, it is output as _("").
    
    Note that an extra empty TIP line is always appended at the end.
    """
    if symbol.is_blank:
        return "BLANK"
    
    lines = []
    # Output the preprocessor condition if applicable.
    if symbol.conditions:
        lines.append(f"#if {symbol.conditions}")
    
    # Escape special characters in the symbol.char.
    escaped_char = escape_text(symbol.char)
    header_line = f'NAME("{symbol.title}"),CHAR("{escaped_char}"),TIP('
    indent = " " * 24
    tip_lines = []
    
    # Process each line of the pre content.
    for line in symbol.content.splitlines():
        escaped_line = escape_text(line)
        if escaped_line.strip() == "":
            escaped_line = ""
        tip_lines.append(f'{indent}_("{escaped_line}")')
    
    # Always ensure the TIP block ends with an empty line.
    tip_lines.append(f'{indent}_("")')
    
    closing_line = f"{indent})"
    lines.append(header_line)
    lines.extend(tip_lines)
    lines.append(closing_line)
    
    if symbol.conditions:
        lines.append("#endif")
    
    return "\n".join(lines)

if __name__ == "__main__":
    toc_file = "toc.json"
    symbol_data_list = process_toc(toc_file)
    
    # Write the complete formatted output to elements.h
    with open("elements.h", "w", encoding="utf-8") as out_file:
        for symbol in symbol_data_list:
            out_file.write(format_symbol(symbol))
            out_file.write("\n")
            