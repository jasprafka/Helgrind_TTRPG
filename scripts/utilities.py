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


def run_command(cmd_str: str, time_out=None, cwd=None) -> int:
    """Run cmd_str with optional timeout and working dir."""
    return subprocess.check_call(cmd_str, timeout=time_out, cwd=cwd)


def run_command_return_output(cmd_str: str, time_out=None, cwd=None) -> str:
    """Run cmd_str with optional timeout and working dir, return output.

    NOTE: Whitespace in the output is preserved and must be dealt with by the caller.
    """
    return subprocess.check_output(cmd_str, timeout=time_out, cwd=cwd, encoding='UTF-8')


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


def _run_git_ls_files_cmd(options: list=None, root: str=None) -> list:
    """Run git ls-files with the specified options, return the output as a list."""
    if options is not None:
        option_str = ' '.join(options)
    if root is None:
        root = get_root_dir()
    git_cmd = f'git ls-files {option_str}'
    output = run_command_return_output(git_cmd, cwd=root)
    output_files = []
    output_lines = output.split()
    if output_lines:
        output_files = [out_file for out_file in output_lines if os.path.isfile(os.path.join(root, out_file))]
    return output_files


def get_modified_files(root: str=None) -> list:
    """Get the list of modified files from worktree specified by root.

    Args:
        root: Root of the worktree to get files for; defaults to current source tree root.

    Returns:
        List of modified files, or an empty list if no modified files.
    """
    if root is None:
        root = get_root_dir()
    modified_files_options = ['-m', root]
    return _run_git_ls_files_cmd(modified_files_options, root=root)


def get_untracked_files(root: str=None) -> list:
    """Get the list of untracked files from worktree specified by root.

    Args:
        root: Root of the worktree to get files for; defaults to current source tree root.

    Returns:
        List of untracked files, or an empty list if no untracked files.
    """
    if root is None:
        root = get_root_dir()
    untracked_files_options = ['-o', '--exclude-standard', root]
    return _run_git_ls_files_cmd(untracked_files_options, root=root)


def get_staged_files(root: str=None) -> list:
    """Get the list of staged files from worktree specified by root.

    Args:
        root: Root of the worktree to get files for; defaults to current source tree root.

    Returns:
        List of staged files, or an empty list if no staged files.
    """
    if root is None:
        root = get_root_dir()
    diff_str = f'git diff --cached --name-only {root}'
    output = run_command_return_output(diff_str, cwd=root)
    output_files = []
    output_lines = output.split()
    if output_lines:
        output_files = [out_file for out_file in output_lines if os.path.isfile(os.path.join(root, out_file))]
    return output_files


def get_current_branch(root: str=None) -> str:
    """Return the name of the current git branch."""
    if root is None:
        root = get_root_dir()
    return run_command_return_output(f'git branch --show-current {root}').strip()


def git_push_to_remote(branch: str) -> None:
    """Push current commit to origin/<branch>."""
    push_cmd = f'git push origin {branch}'
    run_command(push_cmd)