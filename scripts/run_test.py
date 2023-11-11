
import os
import sys
import glob
import logging
import unittest
import argparse
import utilities

LOGGER = logging.getLogger(os.path.basename(__file__))
"""Logger for this module."""

_ROOT = utilities.get_root_dir()
"""Root of the worktree."""

_TEST_DIR = os.path.join(_ROOT, 'scripts', 'testing')
"""Path to testing directory."""

_TEST_RE = os.path.join('scripts', 'testing', 'test_*.py')
"""Glob pattern to match python unittests."""


class TestFailedException(Exception):
    """Exception class for failed unittest."""

def _process_args(argv: list) -> argparse.Namespace:
    """Parse and process arguments; convert to argparse.Namespace object.

    Args:
        argv: List of input arguments.

    Returns:
        args: Parsed args with args as properties on the object.
    """
    # Get the basename (sans extension) of each python unittest file
    parser = argparse.ArgumentParser(os.path.basename(__file__),
                                     description='Run a python unittest. Unittests should not be '
                                     'run directly! They must be run using this script.')
    test_files = glob.glob(_TEST_RE, root_dir=_ROOT)
    test_options = [os.path.basename(file).split('.')[0] for file in test_files]
    test_files.append('test_*.py')
    test_options.append('all')
    parser.add_argument(
        '-t',
        '--test_name',
        help='Name of the test to run.',
        dest='test',
        choices=test_options,
        default='all'
    )
    args = utilities.parser_setup(parser, argv, LOGGER)

    test_map = {basename: os.path.basename(path) for basename, path in zip(test_options, test_files)}
    setattr(args, 'test_map', test_map)

    return args


def _run_test(test_pattern: str) -> unittest.TestResult:
    """Run the python unittest specified by test_pattern."""
    test_suite = unittest.defaultTestLoader.discover(_TEST_DIR, test_pattern)
    result = unittest.TextTestRunner().run(test_suite)
    return result


def main(argv):
    """Run a unittest."""
    args = _process_args(argv)
    result = _run_test(args.test_map[args.test])
    if result.failures or result.errors:
        raise TestFailedException(f'Unittests failed for "{args.test}" suite!')


if __name__ == '__main__':
    main(sys.argv[1:])
