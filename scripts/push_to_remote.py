"""Helper script to do all the things required before pushing to github, then pushes if status is green."""

import os
import sys
import logging
import argparse
import utilities
import run_test

_ROOT = utilities.get_root_dir()
"""Root dir of the worktree."""

LOGGER = logging.getLogger(os.path.basename(__file__))
"""Logger for this module."""


class DirtyWorktreeError(Exception):
    """Exception class for a dirty git worktree."""


def _process_args(argv):
    """Parse and process arguments; convert to argparse.Namespace object.

    Args:
        argv: List of input arguments.

    Returns:
        args: Parsed args with args as properties on the object.
    """
    branch = utilities.get_current_branch(_ROOT)
    parser = argparse.ArgumentParser(os.path.basename(__file__),
                                     description='Perform all actions required for a successful push, '
                                     'then push if status is good.')
    parser.add_argument(
        '-b',
        '--branch',
        help=f'Name of remote branch to push to (default={branch}).',
        dest='branch',
        default=branch
    )
    parser.add_argument(
        '-D',
        '--dry_run',
        help=f"Don't actually perform any actions, just print what would be done.",
        dest='dry_run',
        action='store_true',
        default=False
    )
    args = utilities.parser_setup(parser, argv, LOGGER)
    return args


def _run_unittests():
    """Run all unittests."""
    run_test.main(['-t', 'all'])


def _print_list(my_list: list, tabs: int=0):
    """Print a list with specified left padding."""
    for item in my_list:
        print(''.ljust(tabs * 4, ' ') + item)


def main(argv):
    """Perform all actions required for a successful push, then push if status is green."""
    modified_files = utilities.get_modified_files(_ROOT)
    untracked_files = utilities.get_untracked_files(_ROOT)
    staged_files = utilities.get_staged_files(_ROOT)
    args = _process_args(argv)

    if args.branch == 'main':
        print('You cannot push directly to main! Exiting.')
        return -1

    LOGGER.info('Checking for dirty worktree...')
    if modified_files or untracked_files or staged_files:
        print( f'Modified files:')
        _print_list(modified_files, tabs=1)
        print(f'Untracked files:')
        _print_list(untracked_files, tabs=1)
        print(f'Staged files:')
        _print_list(staged_files, tabs=1)
        if args.dry_run:
            print('Would raise DirtyWorktreeError!')
            return -1
        else:
            raise DirtyWorktreeError(f'Cannot push to origin/{args.branch}, your worktree is dirty! '
                                    'Clean/commit your changes and try again.')

    LOGGER.info('Worktree clean. Running unittests...')
    if not args.dry_run:
        _run_unittests()

    print(f'Worktree clean and unittests passed, pushing to origin/{args.branch}...')
    push_cmd = f'git push origin {args.branch}'
    if args.dry_run:
        print(f'Would run {push_cmd}')
    else:
        pass
        utilities.run_command(push_cmd)


if __name__ == '__main__':
    main(sys.argv[1:])