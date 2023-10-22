"""Script to compile all of the json files into organized markdown files showing various aspects of the data."""

import os
import sys
import json
import jsmin
import logging
import argparse
import utilities
import markdown_utils


LOGGER = logging.getLogger(os.path.basename(__file__))
"""Logger for this module."""

_ROOT = utilities.get_root_dir()
"""Root dir of the worktree."""

_JSON_DIR = os.path.join(_ROOT, 'library', 'json')
"""Path to JSON directory in the worktree."""

_GEN_MD_DIR = os.path.join(_ROOT, 'generated', 'markdown')
"""Path to generated markdown directory in the worktree."""


# ======== Database compilation functions ========
"""Database compilation handler functions; each function must have the signature 'func_name(input_path, args):'."""
def _compile_talents(talents_path: str, args: argparse.Namespace):
    """Generate markdown file for talents.

    Args:
        talents_path: Path to talents.json.
        args: Unused args namespace.

    Post:
        library/markdown/generated/talents_list.md is generated.
    """
    LOGGER.info('Generating markdown for talents...')
    with open(talents_path, 'r') as json_fp:
        talents_list = json.loads(jsmin.jsmin(json_fp.read()))

    LOGGER.debug('-- Sorting talents list...')
    talents_list.sort(key=lambda my_dict: my_dict.get('name', ''))
    talents_list.sort(key=lambda my_dict: my_dict.get('prerequisites', {}).get('level', 0))

    main_heading = markdown_utils.write_heading('Talents', level=1)
    level_heading = markdown_utils.write_heading('Level {} Talents', level=3)
    talent_separator = '  \n'

    md_string = f'{main_heading}\nTalents presented alphabetically by level.\n\n'
    for index in range(1, 11):
        md_string += level_heading.format(str(index))
        md_string += '\n'
        name_list = [talent.get('name', '').replace('_', ' ') for talent in talents_list if talent.get('prerequisites', {}).get('level', 0) == index]
        md_string += talent_separator.join(name_list)
        md_string += '\n\n'

    LOGGER.debug('-- Writing talents file...')
    md_path = os.path.join(_GEN_MD_DIR, 'talents_list.md')
    with open(md_path, 'w') as md_fp:
        md_fp.write(md_string)


def _bad_key(bad_path: str, unused_args: argparse.Namespace):
    """Default return function if a bad key is passed to _FILE_FUNC_MAP."""
    LOGGER.error('Input file %s is not mapped to a handler function! Skipping.', bad_path)

_FILE_FUNC_MAP = {
    os.path.join(_JSON_DIR, 'talents.json'): _compile_talents
}
"""Dict mapping input file name to function for parsing it."""

_SUPPORTED_FILES = list(_FILE_FUNC_MAP.keys())
"""List of supported files."""
# ======== End database compilation functions ========


class DatabaseCompilerError(Exception):
    """Exception class for database compilation errors."""


def _process_args(argv: list) -> argparse.Namespace:
    """Parse and process arguments; convert to argparse.Namespace object.

    Args:
        argv: List of input arguments.

    Returns:
        args: Parsed args with args as properties on the object.
    """
    parser = argparse.ArgumentParser(
        os.path.basename(__file__),
        description='Compile all of the json files into organized markdown files showing various aspects of the data.'
    )
    parser.add_argument(
        '-i',
        '--input_file',
        help='Input JSON file to generate markdown for. If not specified, all supported files will be used.',
        dest='input_json',
        default=None
    )

    args = utilities.parser_setup(parser, argv, LOGGER)

    if args.input_json is None:
        setattr(args, 'input_files', _SUPPORTED_FILES)
    else:
        # Turn file into absolute path to match the paths in _SUPPORTED_FILES
        args.input_json = os.path.abspath(args.input_json)
        if not os.path.isfile(args.input_json):
            raise FileNotFoundError(f'Input file {args.input_json} is not a file or does not exist!')
        elif args.input_json not in _SUPPORTED_FILES:
            raise DatabaseCompilerError(f'Input file {args.input_json} is not a supported file! Supported files = {_SUPPORTED_FILES}')
        setattr(args, 'input_files', [args.input_json])
    LOGGER.debug('Input files = %s', args.input_files)

    return args


def _generate_markdown(args: argparse.Namespace):
    """Dispatch the correct handler function for each file in args.input_files.

    Raises:
        FileNotFoundError: Error if expected input file (i.e. a file in _SUPPORTED_FILES) could not be found.
    """
    os.makedirs(_GEN_MD_DIR, exist_ok=True)
    for in_file in args.input_files:
        if not os.path.isfile(in_file):
            raise FileNotFoundError(f'Supported file {in_file} does not exist, did you delete it?')
        _FILE_FUNC_MAP.get(in_file, _bad_key)(in_file, args)  # Execute function mapped to this file


def main(argv: list) -> None:
    """Process args and generate markdown.

    Args:
        argv: List of input arguments.
    """
    args = _process_args(argv)
    _generate_markdown(args)


if __name__ == '__main__':
    main(sys.argv[1:])