import time
import os
import sys
import re
from configs.config import SEPARATOR, PLANFILE

def read_plan_simple(filename: str) -> list:
    """Read plan file with simple format: NAME[TAB]LINK"""
    result = []
    try:
        with open(filename, mode="r", encoding="utf8") as f:
            for row in f:
                if row.strip() == "<>":
                    break
                if row.strip():  # Skip empty lines
                    result.append(row.strip())
    except FileNotFoundError:
        print(f"Plan file not found: {filename}")
    return result

def file_exists(filename: str) -> bool:
    """Check if markdown file exists"""
    return os.path.exists(filename)

def read_existing_file(filename: str) -> str:
    """Read existing markdown file content"""
    try:
        with open(filename, 'r', encoding='utf8') as f:
            return f.read()
    except:
        return ""

def write_or_append_md(filename: str, link: str):
    """Write new file or append link to existing file with counter"""
    md_filename = filename + '.md'
    
    if file_exists(md_filename):
        # File exists - update counter for link
        existing_content = read_existing_file(md_filename)
        lines = existing_content.split('\n')
        
        # Find the links line (line with [[]])
        links_line_index = -1
        for i, line in enumerate(lines):
            if '[[' in line and ']]' in line:
                links_line_index = i
                break
        
        if links_line_index != -1:
            # Parse existing links and counters
            links_line = lines[links_line_index]
            link_counts = {}
            
            # Extract existing links with counters
            pattern = r'(\d+)\s*\[\[([^\]]+)\]\]'
            matches = re.findall(pattern, links_line)
            
            for count, link_name in matches:
                link_counts[link_name] = int(count)
            
            # Update counter for the new link
            if link in link_counts:
                link_counts[link] += 1
            else:
                link_counts[link] = 1
            
            # Rebuild the links line
            new_links = []
            for link_name, count in link_counts.items():
                new_links.append(f"{count} [[{link_name}]]")
            
            lines[links_line_index] = "    ".join(new_links)
            
            # Write back the modified content
            with open(md_filename, 'w', encoding='utf8') as f:
                f.write('\n'.join(lines))
            print(f"UPDATED: {md_filename} - {link} count is now {link_counts[link]}")
        else:
            # No links line found, add new one
            lines.append(f"1 [[{link}]]")
            with open(md_filename, 'w', encoding='utf8') as f:
                f.write('\n'.join(lines))
            print(f"UPDATED: {md_filename} - added first link to {link}")
    else:
        # File doesn't exist - create new file
        content = f"{filename}\n\n1 [[{link}]]"
        with open(md_filename, 'w', encoding='utf8') as f:
            f.write(content)
        print(f"CREATED: {md_filename} with link to {link}")

def process_simple_plan(plan: list):
    """Process plan with simple format"""
    for row in plan:
        parts = row.split(SEPARATOR)
        if len(parts) >= 2:
            note_name = parts[0].strip()
            link_name = parts[1].strip()
            write_or_append_md(note_name, link_name)

if __name__ == "__main__":
    filename = PLANFILE
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    print(f"Processing plan file: {filename}")
    plan = read_plan_simple(filename)
    print(f"Found {len(plan)} entries")
    
    process_simple_plan(plan)
    print("Done!")