"""General utility functions/globals for python."""

import os
import sys
import logging
import argparse
import subprocess

class RootNotFoundException(Exception):
    """Exception class for if unable to determine worktree root."""

def parser_setup(name: str, desc: str, usage: str=None) -> argparse.ArgumentParser:
    """Create parser with basic functionality.

    Args:
        name: Name of the program to create the parser for.
        desc: Description of the program to create the parser for.
        usage: Command-line invocation example.

    Returns:
        parser: Parser with basic functionality (like debugging).
    """
    parser = argparse.ArgumentParser(prog=name, description=desc)
    if usage is not None:
        parser.usage = usage
    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument(
        '-v',
        '--verbose',
        help='Print out more information.',
        action='store_true',
        dest='verbose',
        default=False
    )
    logging_group.add_argument(
        '-d',
        '--debug',
        help='Print out debugging information.',
        action='store_true',
        dest='debug',
        default=False
    )
    return parser

def logger_setup(logger_name: str, logger_level: int=logging.WARNING) -> logging.Logger:
    """Create and return a logger formatted to print to stdout."""
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(logger_level)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    return logger

def run_command(cmd_str: str, time_out=None) -> int:
    """Run cmd_str with optional timeout."""
    return subprocess.check_call(cmd_str, timeout=time_out)

def get_root_dir(entry_path: str=None, max_steps: int=10, except_on_fail: bool=True) -> str:
    """Determine the root dir of the worktree.

    Args:
        entry_path: Path to start searching in (pending, this arg does nothing right now).
        max_steps: Maximum number of dirs to back up while searching.
        except_on_fail: If true, raise an exception if the root dir cannot be found.

    Returns:
        root_dir: The root dir of the worktree on a success (or an empty string on a failure with except_on_fail=False)
    """
    if entry_path is not None:
        # TODO allow for other entry_paths besides the current
        return None

    start_dir = os.getcwd()
    root_dir = ''
    for _ in range(max_steps):
        os.chdir('../')
        if os.path.exists('.root'):
            root_dir = os.getcwd()
            break
    os.chdir(start_dir)

    if except_on_fail and not root_dir:
        raise RootNotFoundException(f'Unable to determine root of worktree! Start dir: {start_dir}')

    return root_dir
