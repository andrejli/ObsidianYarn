"""
Custom exceptions for ObsidianYarn.
"""

class ObsidianYarnError(Exception):
    """Base exception for ObsidianYarn."""
    pass

class PlanFileError(ObsidianYarnError):
    """Exception raised for plan file related errors."""
    pass

class TemplateError(ObsidianYarnError):
    """Exception raised for template related errors."""
    pass

class FileWriteError(ObsidianYarnError):
    """Exception raised when writing Markdown files fails."""
    pass
