"""General utility functions for generating and working with markdown."""

class MarkdownError(Exception):
    """Exception class for working with markdown."""

def write_heading(heading: str, level: int=1) -> str:
    """Write a markdown heading.

    Args:
        heading: String to convert to markdown heading by appending '#' characters.
        level: Optional number of '#' chars to prepend (default 1).

    Returns:
        md_heading: Markdown heading with specified number of '#'.
    """
    if level < 1:
        raise MarkdownError(f'Invalid level ({level}) for heading {heading}')
    
    return ''.rjust(level, '#') + ' ' + heading
