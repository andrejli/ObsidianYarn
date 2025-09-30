# API Reference

## Core Module (`write_md.py`)

### Functions

#### `add_link(link: str) -> str`
Converts a string to either a Markdown wiki-link or processes it as a tag.

**Parameters:**
- `link` (str): String representation of a link or tag

**Returns:**
- `str`: Formatted Markdown link `[[link]]` or empty string for tags

**Behavior:**
- If link starts with `#`, it's treated as a tag and added to global TAGS variable
- Otherwise, creates a wiki-style link format for Obsidian

**Example:**
```python
add_link("HomePage")     # Returns: "[[HomePage]]"
add_link("#python")      # Returns: "" (adds to TAGS)
```

---

#### `prepare_multiple_links(links: list) -> str`
Processes a list of links and returns a formatted string for Markdown.

**Parameters:**
- `links` (list): List of link strings

**Returns:**
- `str`: Space-separated string of formatted links

**Example:**
```python
links = ["Home", "About", "#tag"]
prepare_multiple_links(links)  # Returns: "[[Home]] [[About]]"
```

---

#### `read_template(filename: str) -> dict`
Reads a template file and returns its processed content.

**Parameters:**
- `filename` (str): Template filename in the templates folder

**Returns:**
- `dict`: Dictionary containing template rows and placeholder positions

**Example:**
```python
template_data = read_template("template")
```

---

#### `prepare_data(name: str, links: str, tags: str) -> str`
Generates Markdown content using the default template format.

**Parameters:**
- `name` (str): Note title
- `links` (str): Formatted links string
- `tags` (str): Formatted tags string

**Returns:**
- `str`: Complete Markdown content

---

#### `prepare_data_custom(name: str, links: str, tags: str) -> str`
Generates Markdown content using a custom template.

**Parameters:**
- `name` (str): Note title
- `links` (str): Formatted links string  
- `tags` (str): Formatted tags string

**Returns:**
- `str`: Complete Markdown content formatted according to custom template

---

#### `write_md(filename: str, data: str) -> bool`
Writes Markdown content to a file.

**Parameters:**
- `filename` (str): Target filename with path
- `data` (str): Markdown content to write

**Returns:**
- `bool`: True if successful, False otherwise

**Error Handling:**
- Catches and logs exceptions during file writing
- Returns False on any error

---

#### `prepare_data_2_save(plan: list, index_of_files: list) -> bool`
Main processing function that generates Markdown files from plan data.

**Parameters:**
- `plan` (list): List of plan rows from plan file
- `index_of_files` (list): List of existing Markdown files

**Returns:**
- `bool`: True when processing is complete

**Behavior:**
- Splits each plan row by separator
- Generates Markdown content for each note
- Skips files that already exist

## IO Module (`IO/io_plan.py`)

### Functions

#### `read_plan(filename: str) -> list`
Reads and parses a plan file into a list of rows.

**Parameters:**
- `filename` (str): Path to the plan file

**Returns:**
- `list`: List of strings, each representing a row in the plan

**Error Handling:**
- Returns empty list if file not found
- Prints error messages for file access issues

**File Format:**
- Reads until `<>\n` end symbol is encountered
- Each row represents one note and its connections

---

#### `get_index(path: str = None) -> list`
Scans a directory for Markdown files and returns their filenames.

**Parameters:**
- `path` (str, optional): Directory path to scan. Defaults to current working directory

**Returns:**
- `list`: List of Markdown filenames (ending in `.md`)

**Error Handling:**
- Returns empty list on directory access errors
- Prints error messages for permission or path issues

---

#### `file_is_markdown(path: str) -> bool`
Checks if a file path represents a Markdown file.

**Parameters:**
- `path` (str): File path to check

**Returns:**
- `bool`: True if file ends with `.md`, False otherwise

---

#### `filename_exists(filename: str, index: list) -> bool`
Checks if a filename exists in a provided list.

**Parameters:**
- `filename` (str): Filename to search for
- `index` (list): List of filenames to search in

**Returns:**
- `bool`: True if filename found in list, False otherwise

---

#### `duplicity_check_plan(plan: list) -> bool`
Analyzes a plan for duplicate note names.

**Parameters:**
- `plan` (list): List of plan rows

**Returns:**
- `bool`: True if duplicates found, False otherwise

**Algorithm:**
- Extracts first column (note name) from each row
- Uses set comparison to detect duplicates
- Prints diagnostic information

## Template Module (`IO/template_reader.py`)

### Class: `TemplateReader`

Template file parser that processes custom templates with placeholder detection.

#### `__init__(filename: str)`
Initializes the template reader.

**Parameters:**
- `filename` (str): Path to template file

**Attributes:**
- `template_file` (str): Path to template file
- `rows` (dict): Dictionary of template rows
- `tags` (list): List of detected tags

---

#### `read_template() -> None`
Reads the template file line by line into memory.

**Behavior:**
- Stops reading after 30 consecutive blank lines
- Stores each line with a numeric index
- Handles file access errors gracefully

**Error Handling:**
- Sets empty dictionary on file not found
- Prints error messages for access issues

---

#### `purge_last30blankrows() -> bool`
Removes trailing blank rows from the template.

**Returns:**
- `bool`: True when operation completes

**Purpose:**
- Cleans up template by removing excess whitespace
- Prevents blank content in generated files

---

#### `seek_tags_and_links() -> dict`
Scans template rows for placeholder tags.

**Returns:**
- `dict`: Dictionary of found placeholders with positions

**Placeholders Detected:**
- `<Tags>`: Tag insertion point
- `<Links>`: Link insertion point
- `<Name>`: Note name insertion point
- `<Author>`: Author insertion point
- `<Date>`: Date insertion point

**Return Format:**
```python
{
    row_index: (row_content, (start_pos, end_pos)),
    # ... more matches
}
```

## Configuration (`configs/config.py`)

### Constants

#### `SEPARATOR`
**Type:** `str`  
**Default:** `"\t"`  
**Purpose:** Character used to separate columns in plan files

#### `END_SYMBOL`
**Type:** `str`  
**Default:** `"<>\n"`  
**Purpose:** Symbol marking the end of plan file content

#### `TAGS`
**Type:** `str`  
**Default:** `""`  
**Purpose:** Global tags to be added to all generated notes

#### `PLANFILE`
**Type:** `str`  
**Default:** `"plan.txt"`  
**Purpose:** Default filename for plan files

#### `AUTHOR`
**Type:** `str`  
**Default:** `"ANDREW"`  
**Purpose:** Author name for generated file attribution

## Error Handling

### Common Exceptions

1. **FileNotFoundError**: Plan file or template file missing
2. **PermissionError**: Insufficient permissions for file operations
3. **UnicodeDecodeError**: File encoding issues
4. **IndexError**: Malformed plan file rows

### Error Recovery

- Functions return safe defaults (empty lists/dicts) on errors
- Error messages are printed to console for debugging
- Program continues execution when possible
- Existing files are never overwritten

## Type Hints

All functions include comprehensive type hints for:
- Parameter types
- Return types  
- Optional parameters
- Collection types (list, dict)

This enables better IDE support and static type checking with tools like mypy.