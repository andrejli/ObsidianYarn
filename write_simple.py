import time
import os
import sys
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

def write_or_append_md(filename: str, link: str, pair_counts: dict):
    """Write new file or append link to existing file with counter for duplicates"""
    md_filename = filename + '.md'
    pair_key = f"{filename}-{link}"
    
    # Get count for this specific pair
    if pair_key in pair_counts:
        pair_counts[pair_key] += 1
        counter = pair_counts[pair_key]
        link_formatted = f"{counter} [[{link}]]"
    else:
        pair_counts[pair_key] = 1
        link_formatted = f"[[{link}]]"
    
    if file_exists(md_filename):
        # File exists - append new link
        existing_content = read_existing_file(md_filename)
        
        # Find the links line and add new link
        lines = existing_content.split('\n')
        new_content = []
        for line in lines:
            if line.strip().startswith('[[') or (line.strip() and line.strip()[0].isdigit() and '[[' in line):
                # This is a links line, append new link
                new_content.append(line + f"    {link_formatted}")
            else:
                new_content.append(line)
        
        # Write back the modified content
        with open(md_filename, 'w', encoding='utf8') as f:
            f.write('\n'.join(new_content))
        print(f"UPDATED: {md_filename} - added {link_formatted}")
    else:
        # File doesn't exist - create new file
        content = f"{filename}\n\n{link_formatted}"
        with open(md_filename, 'w', encoding='utf8') as f:
            f.write(content)
        print(f"CREATED: {md_filename} with {link_formatted}")

def process_simple_plan(plan: list):
    """Process plan with simple format and track pair occurrences"""
    pair_counts = {}
    
    # First pass: count all pairs
    for row in plan:
        parts = row.split(SEPARATOR)
        if len(parts) >= 2:
            note_name = parts[0].strip()
            link_name = parts[1].strip()
            pair_key = f"{note_name}-{link_name}"
            pair_counts[pair_key] = 0
    
    # Second pass: process with counters
    for row in plan:
        parts = row.split(SEPARATOR)
        if len(parts) >= 2:
            note_name = parts[0].strip()
            link_name = parts[1].strip()
            write_or_append_md(note_name, link_name, pair_counts)

if __name__ == "__main__":
    filename = PLANFILE
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    print(f"Processing plan file: {filename}")
    plan = read_plan_simple(filename)
    print(f"Found {len(plan)} entries")
    
    process_simple_plan(plan)
    print("Done!")