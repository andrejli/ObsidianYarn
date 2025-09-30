# ObsidianYarn

A Python tool for generating interconnected Obsidian Markdown files from structured plan files. Create knowledge graphs, documentation systems, and note networks with ease.

## Features

- 📝 **Structured Note Generation**: Create interconnected Markdown files from simple plan files
- 🔗 **Automatic Linking**: Generate proper Obsidian wiki-style links (`[[Note Name]]`)
- 🏷️ **Tag Support**: Automatic tag processing and organization
- 📋 **Custom Templates**: Use customizable templates with placeholders
- 🛡️ **Safe Operation**: Never overwrites existing files
- ⚙️ **Configurable**: Flexible configuration for different workflows
- 🧪 **Well Tested**: Comprehensive test suite with pytest

## Quick Start

1. **Install**:
   ```bash
   git clone https://github.com/andrejli/ObsidianYarn.git
   cd ObsidianYarn
   pip install -r requirements.txt
   ```

2. **Configure** (`configs/config.py`):
   ```python
   AUTHOR = "Your Name"
   PLANFILE = "plan.txt"
   ```

3. **Create a plan file** (`plan.txt`):
   ```
   HomePage	About	Projects	Contact
   About	HomePage	Skills	Experience
   Projects	HomePage	Project1	Project2
   <>
   ```

4. **Generate notes**:
   ```bash
   python write_md.py
   ```

## Documentation

- 📖 **[Complete Documentation](DOCUMENTATION.md)** - Installation, configuration, and usage guide
- 🔧 **[API Reference](API.md)** - Detailed function and class documentation  
- 💡 **[Examples](EXAMPLES.md)** - Real-world use cases and templates
- 🧪 **[Tests](tests.py)** - Run with `python -m pytest tests.py`

## Requirements

- Python 3.7+
- Obsidian (for viewing generated files)
- pytest (for testing)

## Usage Examples

### Basic Command Line
```bash
# Use default plan file
python write_md.py

# Use custom plan file  
python write_md.py my_notes.txt
```

### Plan File Format
```
NoteName[TAB]Link1[TAB]Link2[TAB]#tag1
AnotherNote[TAB]NoteName[TAB]#tag2
<>
```

### Custom Templates
Create `templates/template` with placeholders:
```markdown
# <Name>
Created: <Date>
Author: <Author>

<Links>
<Tags>
```

## Project Structure

```
ObsidianYarn/
├── configs/           # Configuration files
├── IO/               # Input/output modules  
├── templates/        # Template files
├── tests/           # Test files and data
├── write_md.py      # Main application
├── plan.txt         # Example plan file
└── requirements.txt # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_obsidian_yarn.py::test_read_plan -v
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

- 📚 Check the [documentation](DOCUMENTATION.md) for detailed guidance
- 💡 See [examples](EXAMPLES.md) for real-world use cases
- 🐛 Report issues on GitHub
- 💬 Discussions and questions welcome in GitHub Issues

---

**Happy Knowledge Building! 🧠✨**


