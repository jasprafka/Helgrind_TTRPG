"""General utility functions/globals for python."""

import os
import sys
import logging
import argparse
import subprocess

class RootNotFoundException(Exception):
    """Exception class for if unable to determine worktree root."""


def parser_setup(parser: argparse.ArgumentParser, argv: list, logger: logging.Logger=None) -> argparse.Namespace:
    """Create parser with basic functionality.

    Args:
        parser: Argument parser to setup.
        argv: list of args to parse.
        logger: Logger to configure.

    Returns:
        args: Parsed args with values as properties on the object.
    """
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

    argv = parser.parse_args()

    if logger is not None:
        _logger_config(logger, argv)
        logger.debug('args: %s', argv)

    return argv


def _logger_config(logger: logging.Logger, args: argparse.Namespace) -> None:
    """Configure an existing logger based on the verbosity of the parsed args.

    Args:
        logger: Logger to configure.
        args: Parsed args as configured in parser_setup(). 

    NOTE: This function should never be called directly and only used from inside parser_setup().
    """
    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)


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
        if os.path.exists('.root'):
            root_dir = os.getcwd()
            break
        os.chdir('../')
    os.chdir(start_dir)

    if except_on_fail and not root_dir:
        raise RootNotFoundException(f'Unable to determine root of worktree! Start dir: {start_dir}')

    return os.path.abspath(root_dir)  # Ensure root path is absolute path
