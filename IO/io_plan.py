
import os
from configs.config import SEPARATOR, END_SYMBOL
from IO.exceptions import PlanFileError

def read_plan(filename: str) -> list:
    """
    Reads a plan file and returns a list of rows until the end symbol is found.
    Args:
        filename: Path to the plan file.
    Returns:
        List of strings, each representing a row in the plan.
    """
    result = []
    if not filename:
        raise PlanFileError("Plan filename cannot be empty")
    
    try:
        with open(filename, mode="r", encoding="utf8") as f:
            for row in f:
                if row == END_SYMBOL:  # End symbol from config
                    break
                result.append(row)
    except FileNotFoundError:
        raise PlanFileError(f"Plan file not found: {filename}")
    except PermissionError:
        raise PlanFileError(f"Permission denied reading plan file: {filename}")
    except UnicodeDecodeError as e:
        raise PlanFileError(f"Invalid encoding in plan file {filename}: {e}")
    except Exception as e:
        raise PlanFileError(f"Error reading plan file {filename}: {e}")
    
    return result

def get_index(path: str = None) -> list:
    """
    Returns a list of all Markdown (.md) files in the given directory.
    Args:
        path: Directory to search for Markdown files. Defaults to current working directory.
    Returns:
        List of Markdown filenames.
    Raises:
        PlanFileError: If directory cannot be accessed.
    """
    if path is None:
        path = os.getcwd()
    
    if not os.path.exists(path):
        raise PlanFileError(f"Directory does not exist: {path}")
    
    if not os.path.isdir(path):
        raise PlanFileError(f"Path is not a directory: {path}")
    
    try:
        content = os.listdir(path)
        result = [i for i in content if i.endswith('.md')]
    except PermissionError:
        raise PlanFileError(f"Permission denied accessing directory: {path}")
    except Exception as e:
        raise PlanFileError(f"Error listing directory {path}: {e}")
    
    return result

def file_is_markdown(path: str) -> bool:
    """
    Checks if the given file path is a Markdown file.
    Args:
        path: File path to check.
    Returns:
        True if file is Markdown, False otherwise.
    """
    return path.endswith('.md')

def filename_exists(filename: str, index: list) -> bool:
    """
    Checks if the filename exists in the provided index list.
    Args:
        filename: Filename to check.
        index: List of filenames.
    Returns:
        True if filename exists, False otherwise.
    """
    return filename in index

def duplicity_check_plan(plan: list) -> bool:
    """
    Checks for duplicate node names in the plan.
    Args:
        plan: List of node names with links.
    Returns:
        True if duplicates exist, False otherwise.
    """
    nodes = [row.split(SEPARATOR)[0] for row in plan]
    nodes_set = set(nodes)
    if len(nodes) != len(nodes_set):
        print(f"DUPLICITY IN PLAN DETECTED: {len(nodes)} nodes, {len(nodes_set)} unique")
        return True
    else:
        print("DUPLICITY IN PLAN NOT DETECTED")
        return False