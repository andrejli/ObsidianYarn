import time
import os
import sys
from IO.template_reader import TemplateReader
from IO.io_plan import read_plan, get_index, filename_exists, duplicity_check_plan
from IO.exceptions import PlanFileError, TemplateError, FileWriteError
from configs.config import SEPARATOR, TAGS, END_SYMBOL, AUTHOR, PLANFILE

def add_link(link: str, tags: str = "") -> tuple:
    """
    Adds a Zettelkasten link to Markdown format. Tags (#) are accumulated in tags parameter.
    Args:
        link: String representation of a Zettelkasten link.
        tags: Current accumulated tags string.
    Returns:
        Tuple of (Markdown link string or empty if tag, updated tags string).
    """
    if link.startswith("#"):
        tags += link + " "
        return ("", tags)
    return (f"[[{link}]]", tags)

def prepare_multiple_links(links: list, tags: str = "") -> tuple:
    """
    Prepares a string of Markdown links from a list.
    Args:
        links: List of link strings.
        tags: Current accumulated tags string.
    Returns:
        Tuple of (String of Markdown links, updated tags string).
    """
    result = ""
    for i in links:
        i = i.rstrip("\n")
        link_str, tags = add_link(i, tags)
        if link_str:
            result += " " + link_str
    return (result.strip(), tags)

def read_template(filename: str) -> dict:
    """
    Reads a template file and returns its rows and tag/link positions.
    Args:
        filename: Template filename in templates folder.
    Returns:
        Dictionary of template rows and tag/link positions.
    Raises:
        TemplateError: If template cannot be read or processed.
    """
    if not filename:
        raise TemplateError("Template filename cannot be empty")
    
    file = os.path.join(os.getcwd(), "templates", filename)
    obj = TemplateReader(filename=file)
    obj.read_template()
    obj.purge_last30blankrows()
    result = obj.seek_tags_and_links()
    
    if not result:
        raise TemplateError(f"Template {filename} is empty or invalid")
    
    return result

def prepare_data_custom(name: str, links: str, tags: str, template: dict) -> str:
    """
    Prepares Markdown content for a custom template.
    Args:
        name: Note name.
        links: Markdown links string.
        tags: Accumulated tags string.
        template: Dictionary of template rows and tag/link positions.
    Returns:
        Markdown content string.
    """
    result = ""
    for i in template:
        row = template[i][0] if isinstance(template[i], tuple) else template[i]
        row = row.replace("<Name>", name)
        row = row.replace("<Tags>", tags)
        row = row.replace("<Links>", links)
        row = row.replace("<Author>", AUTHOR)
        if "<Date>" in row:
            date = time.strftime("%d.%m.%Y %H:%M")
            row = row.replace("<Date>", date)
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
    Raises:
        FileWriteError: If file cannot be written.
    """
    if not filename:
        raise FileWriteError("Filename cannot be empty")
    
    if not data:
        raise FileWriteError(f"Cannot write empty data to {filename}")
    
    try:
        with open(filename, mode="w", encoding="utf8") as f:
            f.write(data)
        print(f"SAVED: {filename}")
        return True
    except PermissionError:
        raise FileWriteError(f"Permission denied writing to {filename}")
    except OSError as e:
        raise FileWriteError(f"OS error writing to {filename}: {e}")
    except Exception as e:
        raise FileWriteError(f"Error saving {filename}: {e}")

def prepare_data_2_save(plan: list, index_of_files: list, template: dict) -> bool:
    """
    Iterates through the plan and writes Markdown files for each entry.
    Args:
        plan: List of plan rows.
        index_of_files: List of existing Markdown files.
        template: Dictionary of template rows and tag/link positions.
    Returns:
        True when done.
    Raises:
        PlanFileError: If plan data is invalid.
    """
    if not plan:
        raise PlanFileError("Plan is empty")
    
    if template is None:
        raise TemplateError("Template cannot be None")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "GENERATED_MARKDOWN")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for row in plan:
        tags = ""  # Local tags for each file
        splitted_row = row.split(SEPARATOR)
        
        if not splitted_row[0].strip():
            print(f"WARNING: Skipping empty note name in row: {row.strip()}")
            continue
        
        links = splitted_row[1:]
        if len(splitted_row) > 1:
            links_str, tags = prepare_multiple_links(links, tags)
            data = prepare_data_custom(splitted_row[0], links_str, tags, template)
            filename = splitted_row[0] + '.md'
            filepath = os.path.join(output_dir, filename)
            if filename_exists(filename, index_of_files):
                print(f"FILE ALREADY EXISTS: {filename}")
            else:
                write_md(filename=filepath, data=data)
    return True

if __name__ == "__main__":
    try:
        print(SEPARATOR, TAGS, END_SYMBOL, AUTHOR)
        filename = PLANFILE
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        
        # Read plan file
        try:
            plan = read_plan(filename=filename)
            if not plan:
                print("WARNING: Plan file is empty")
                sys.exit(0)
        except PlanFileError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        
        # Get index of existing files
        try:
            index_of_files = get_index()
            print(f"Found {len(index_of_files)} existing Markdown files")
        except PlanFileError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        
        # Read template
        try:
            template = read_template(filename="template")
        except TemplateError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        
        # Check for duplicates
        duplicity_check_plan(plan)
        
        # Generate files
        try:
            prepare_data_2_save(plan, index_of_files, template)
            print("\nMarkdown generation completed successfully")
        except (PlanFileError, TemplateError, FileWriteError) as e:
            print(f"ERROR during generation: {e}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
