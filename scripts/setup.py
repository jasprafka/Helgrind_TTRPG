"""Script to ensure environment is setup for this project."""

import os
import sys
import logging
import argparse
import utilities

LOGGER = logging.getLogger(os.path.basename(__file__))
"""Logger for this module."""

_ROOT = utilities.get_root_dir()
"""Root dir of the worktree."""


def _process_args(argv):
    """Parse and process arguments; convert to argparse.Namespace object.

    Args:
        argv: List of input arguments.

    Returns:
        args: Parsed args with args as properties on the object.
    """
    parser = argparse.ArgumentParser(os.path.basename(__file__), description='Ensure environment is setup for this project.')
    parser.add_argument(
        '-r',
        '--requirements',
        help='Path to requirements.txt',
        dest='requirements_file',
        default=None
    )
    args = utilities.parser_setup(parser, argv, LOGGER)
    return args


def _validate_python_packages(req_file: str=None):
    """Ensure required python packages are installed. Optionally specify path to requirements.txt.

    Args:
        req_file: Optional path to requirements.txt file.

    Raises:
        FileNotFoundError: Raises if no requirements.txt file can be found.
    """
    LOGGER.info('Checking python package requirements...')
    if req_file is None:
        req_file = os.path.join(_ROOT, 'scripts', 'requirements.txt')
    if not os.path.isfile(req_file):
        raise FileNotFoundError(f'Requirements file {req_file} does not exist!')
    req_cmd = f'python -m pip install -r {req_file}'
    utilities.run_command(req_cmd)


def main(argv):
    """Setup environment for Helgrind."""
    LOGGER.debug('Root = %s', _ROOT)
    args = _process_args(argv)
    _validate_python_packages(args.requirements_file)


if __name__ == '__main__':
    main(sys.argv[1:])