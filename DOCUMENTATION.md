# ObsidianYarn Documentation

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Configuration](#configuration)
4. [Plan File Format](#plan-file-format)
5. [Template System](#template-system)
6. [API Reference](#api-reference)
7. [Development](#development)
8. [Examples](#examples)

## Installation

### Prerequisites
- Python 3.7 or higher
- Obsidian (for viewing generated files)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/andrejli/ObsidianYarn.git
   cd ObsidianYarn
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the project to your Obsidian vault folder (optional but recommended)

## Quick Start

1. **Configure the tool** by editing `configs/config.py`:
   ```python
   AUTHOR = "Your Name"
   PLANFILE = "plan.txt"
   ```

2. **Create a plan file** (`plan.txt`) with your note structure:
   ```
   HomePage	About	Projects	Contact
   About	HomePage
   Projects	HomePage	Project1	Project2
   <> 
   ```

3. **Run the generator**:
   ```bash
   python write_md.py
   ```

4. **Check your vault** - Markdown files will be created for each note with proper Obsidian links.

## Configuration

### Config File (`configs/config.py`)

| Setting | Description | Default | Example |
|---------|-------------|---------|---------|
| `SEPARATOR` | Character separating columns in plan file | `"\t"` | `"\t"` (tab) |
| `END_SYMBOL` | Symbol marking end of plan file | `"<>\n"` | `"<>\n"` |
| `TAGS` | Global tags to add to all notes | `""` | `"#generated"` |
| `PLANFILE` | Default plan file name | `"plan.txt"` | `"my_notes.txt"` |
| `AUTHOR` | Author name for generated files | `"ANDREW"` | `"Your Name"` |

## Plan File Format

### Structure
Each line in the plan file represents one note and its connections:
```
NoteName[TAB]Link1[TAB]Link2[TAB]Tag1[TAB]Tag2
```

### Rules
- **First column**: Note name (becomes the filename with `.md` extension)
- **Subsequent columns**: Links to other notes or tags
- **Tags**: Prefix with `#` (e.g., `#python`, `#project`)
- **End marker**: Line containing only `<>` marks the end of the plan
- **Separator**: Use tabs by default (configurable)

### Example Plan File
```
HomePage	About	Projects	Contact	#main
About	HomePage	Skills	Experience	#personal
Projects	HomePage	Project1	Project2	#work
Skills	About	Python	JavaScript	#technical
Contact	HomePage	Email	LinkedIn	#contact
<>
```

This creates 5 Markdown files with interconnected links.

## Template System

### Default Template
If no custom template is found, uses a simple default format:
```markdown
# Note Name

## Links [[Link1]] [[Link2]]

## Tags #tag1 #tag2

Created by SCRIPT
```

### Custom Templates

Create a file at `templates/template` with placeholders:

```markdown
<Name>
<Date>

## Overview
Brief description here.

<Tags>

## Related Notes
<Links>

## Additional Info
Add your content here.

### Metadata
Created by <Author>
```

### Available Placeholders
- `<Name>` - Note title
- `<Date>` - Current date/time
- `<Tags>` - Formatted tags
- `<Links>` - Formatted links
- `<Author>` - Author from config

## API Reference

### Core Functions

#### `add_link(link: str) -> str`
Converts a link to Markdown format or processes as tag.
- **Args**: `link` - String representation of link or tag
- **Returns**: Markdown link string or empty string for tags
- **Example**: `add_link("HomePage")` → `"[[HomePage]]"`

#### `prepare_multiple_links(links: list) -> str`
Processes a list of links into a formatted string.
- **Args**: `links` - List of link strings
- **Returns**: Space-separated Markdown links
- **Example**: `prepare_multiple_links(["Home", "About"])` → `"[[Home]] [[About]]"`

#### `write_md(filename: str, data: str) -> bool`
Writes Markdown content to a file.
- **Args**: 
  - `filename` - Target filename
  - `data` - Markdown content
- **Returns**: True if successful, False otherwise

### IO Functions (`IO/io_plan.py`)

#### `read_plan(filename: str) -> list`
Reads and parses a plan file.
- **Args**: `filename` - Path to plan file
- **Returns**: List of plan rows
- **Raises**: Prints error message if file not found

#### `get_index(path: str = None) -> list`
Gets list of existing Markdown files in directory.
- **Args**: `path` - Directory path (defaults to current directory)
- **Returns**: List of `.md` filenames

#### `duplicity_check_plan(plan: list) -> bool`
Checks for duplicate note names in plan.
- **Args**: `plan` - List of plan rows
- **Returns**: True if duplicates found, False otherwise

### Template Functions (`IO/template_reader.py`)

#### `TemplateReader`
Class for reading and parsing template files.

**Methods:**
- `read_template()` - Reads template file into memory
- `purge_last30blankrows()` - Removes trailing blank lines
- `seek_tags_and_links()` - Finds placeholder positions

## Development

### Project Structure
```
ObsidianYarn/
├── configs/
│   └── config.py          # Configuration settings
├── IO/
│   ├── io_plan.py         # Plan file operations
│   └── template_reader.py # Template processing
├── templates/
│   └── template           # Custom template file
├── tests/
│   ├── test_plan          # Test plan file
│   └── test.md            # Test markdown file
├── tests.py               # Test suite
├── write_md.py            # Main application
├── plan.txt               # Example plan file
└── requirements.txt       # Dependencies
```

### Running Tests
```bash
python -m pytest tests/ -v
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Include docstrings for all public functions
- Handle errors gracefully with try/except blocks

## Examples

### Example 1: Simple Knowledge Base
**Plan file:**
```
Index	Concepts	Tools	Resources
Concepts	Index	Programming	Design	#learning
Programming	Concepts	Python	JavaScript	#code
Design	Concepts	UI	UX	#design
Tools	Index	VSCode	Git	#tools
<>
```

**Generated files:**
- `Index.md` - Main hub linking to all sections
- `Concepts.md` - Overview with links to specific topics
- `Programming.md` - Programming notes with language links
- `Design.md` - Design concepts
- `Tools.md` - Development tools

### Example 2: Project Documentation
**Plan file:**
```
ProjectOverview	Requirements	Architecture	Implementation	#project
Requirements	ProjectOverview	Functional	NonFunctional	#analysis
Architecture	ProjectOverview	Database	API	Frontend	#design
Implementation	ProjectOverview	Setup	Development	Testing	#code
<>
```

Creates a complete project documentation structure with cross-references.

### Example 3: Personal Knowledge Management
**Plan file:**
```
PersonalHub	Learning	Projects	Ideas	#personal
Learning	PersonalHub	Books	Courses	Articles	#knowledge
Projects	PersonalHub	Active	Completed	Planned	#work
Ideas	PersonalHub	Technical	Creative	Business	#inspiration
<>
```

Builds a personal knowledge management system with categorized notes.

## Troubleshooting

### Common Issues

1. **File not found errors**: Ensure `plan.txt` exists and path is correct
2. **Template not working**: Check `templates/template` file exists and has proper placeholders
3. **Files not generating**: Verify plan file ends with `<>` symbol
4. **Encoding issues**: Ensure plan file is saved with UTF-8 encoding

### Error Messages

- `PLAN FILE DOESN'T EXIST`: Plan file not found at specified path
- `FILE ALREADY EXISTS`: Markdown file already exists (safety feature)
- `DUPLICITY IN PLAN DETECTED`: Multiple entries with same note name
- `Template file not found`: Custom template file missing

### Getting Help

1. Check this documentation
2. Review example files in the repository
3. Run tests to verify installation: `python -m pytest tests.py`
4. Check issues on GitHub repository

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.