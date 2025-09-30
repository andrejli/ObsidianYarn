import time
import os
import sys
from IO.template_reader import TemplateReader
from IO.io_plan import read_plan, get_index, filename_exists, duplicity_check_plan
from configs.config import SEPARATOR, TAGS, END_SYMBOL, AUTHOR, PLANFILE

def add_link(link: str) -> str:
    """
    Adds a Zettelkasten link to Markdown format. Tags (#) are added to TAGS global.
    Args:
        link: String representation of a Zettelkasten link.
    Returns:
        Markdown link string or empty if tag.
    """
    global TAGS
    if link.startswith("#"):
        TAGS += link + " "
        return ""
    return f"[[{link}]]"

def prepare_multiple_links(links: list) -> str:
    """
    Prepares a string of Markdown links from a list.
    Args:
        links: List of link strings.
    Returns:
        String of Markdown links.
    """
    result = ""
    for i in links:
        i = i.rstrip("\n")
        result += " " + add_link(i)
    return result.strip()

def read_template(filename: str) -> dict:
    """
    Reads a template file and returns its rows and tag/link positions.
    Args:
        filename: Template filename in templates folder.
    Returns:
        Dictionary of template rows and tag/link positions.
    """
    file = os.path.join(os.getcwd(), "templates", filename)
    obj = TemplateReader(filename=file)
    obj.read_template()
    obj.purge_last30blankrows()
    return obj.seek_tags_and_links()

def prepare_data(name: str, links: str, tags: str) -> str:
    """
    Prepares Markdown content for the default template.
    Args:
        name: Note name.
        links: Markdown links string.
        tags: Markdown tags string.
    Returns:
        Markdown content string.
    """
    global TAGS
    tags = TAGS
    result = f"# {name}\n\n"
    result += f"## Links {links}\n"
    result += f"## Tags {tags}\n\n"
    result += "Created by SCRIPT"
    return result

def prepare_data_custom(name: str, links: str, tags: str) -> str:
    """
    Prepares Markdown content for a custom template.
    Args:
        name: Note name.
        links: Markdown links string.
        tags: Markdown tags string.
    Returns:
        Markdown content string.
    """
    global TAGS, AUTHOR
    tags = TAGS
    result = ""
    loaded_template = read_template(filename="template")
    for i in loaded_template:
        row = loaded_template[i][0] if isinstance(loaded_template[i], tuple) else loaded_template[i]
        if "<Name>" in row:
            result += f"# {name}\n"
        elif "<Tags>" in row:
            result += f"## TAGS :{tags}\n"
        elif "Links" in row:
            result += f"## LINKS : {links}\n"
        elif "<Author>" in row:
            result += f"### Was Created By : {AUTHOR}\n"
        elif "<Date>" in row:
            date = time.strftime("%d.%m.%Y %H:%M")
            result += f"### Date : {date}\n"
        else:
            result += row
    return result

def write_md(filename: str, data: str) -> bool:
    """
    Writes prepared Markdown data to a file.
    Args:
        filename: Path and filename.
        data: Markdown content string.
    Returns:
        True if saved successfully.
    """
    try:
        with open(filename, mode="w", encoding="utf8") as f:
            f.write(data)
        print(f"SAVED: {filename}")
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def prepare_data_2_save(plan: list, index_of_files: list) -> bool:
    """
    Iterates through the plan and writes Markdown files for each entry.
    Args:
        plan: List of plan rows.
        index_of_files: List of existing Markdown files.
    Returns:
        True when done.
    """
    global TAGS, SEPARATOR
    for row in plan:
        splitted_row = row.split(SEPARATOR)
        links = splitted_row[1:]
        if len(splitted_row) > 1:
            data = prepare_data_custom(splitted_row[0], prepare_multiple_links(links), TAGS)
            filename = splitted_row[0] + '.md'
            if filename_exists(filename, index_of_files):
                print(f"FILE ALREADY EXISTS: {filename}")
            else:
                write_md(filename=filename, data=data)
    return True

if __name__ == "__main__":
    print(SEPARATOR, TAGS, END_SYMBOL, AUTHOR)
    filename = PLANFILE
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    try:
        plan = read_plan(filename=filename)
    except FileNotFoundError:
        plan = []
        print("PLAN FILE DOESN'T EXIST")
    index_of_files = get_index()
    print(index_of_files)
    a = duplicity_check_plan(plan)
    print(a)
    prepare_data_2_save(plan, index_of_files)

