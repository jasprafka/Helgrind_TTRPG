"""Script to validate JSON files using the schemas under <ROOT>/library/schemas/"""

import os
import sys
import json
import jsmin
import logging
import argparse
import utilities
import jsonschema

LOGGER = logging.getLogger(os.path.basename(__file__))
"""Logger for this module."""

class ValidatorException(Exception):
    """Exception for JSON validation error."""

def _process_args(argv: list) -> argparse.Namespace:
    """Parse and process arguments; convert to argparse.Namespace object.

    Args:
        argv: List of input arguments.

    Returns:
        args: Parsed args with args as properties on the object.
    """
    parser = argparse.ArgumentParser(os.path.basename(__file__), description='Validate the structure of a JSON file using an associated schema.')
    parser.add_argument(
        '-i',
        '--input_file',
        help='Path to input JSON file to be validated.',
        dest='json_path',
        default=None
    )
    parser.add_argument(
        '-s',
        '--schema_file',
        help='Path to JSON schame file to use for validation.',
        dest='schema_path',
        default=None
    )
    args = utilities.parser_setup(parser, argv, LOGGER)

    if args.json_path is None:
        # TODO allow for user to validate ALL json files at once
        raise ValidatorException('Pending functionality; For now you must specify an input file!')
    elif not os.path.exists(args.json_path):
        raise FileNotFoundError(f'Input file {args.json_path} does not exist!')

    if args.schema_path is None:
        # TODO allow for user to validate ALL json files at once
        raise ValidatorException('Pending functionality; For now you must specify a schema file!')
    elif not os.path.exists(args.schema_path):
        raise FileNotFoundError(f'Schema file {args.json_path} does not exist!')


    return args

def _object_is_valid(in_obj, schema, file_path: str='unknown') -> bool:
    """Validate in_obj against schema."""
    # Try and get the object's name to help with debugging
    if isinstance(in_obj, dict):
        in_obj_name = in_obj.get('name', None)

    try:
        jsonschema.validate(in_obj, schema)
        if in_obj_name is not None:
            LOGGER.info('-- Object "%s" from file %s is valid!', in_obj_name, file_path)
        else:
            LOGGER.info('-- Object from file %s is valid!', file_path)
        return True
    except jsonschema.exceptions.ValidationError as excpt:
        if in_obj_name is not None:
            LOGGER.info('-- Object "%s" from file %s is not valid!', in_obj_name, file_path)
        else:
            LOGGER.info('-- Object from file %s is not valid!', file_path)
        LOGGER.debug(excpt)
        return False

def _validate_json_file(json_path: str, schema_path: str) -> bool:
    """Validate json_path using schema at schema_path.

    Args:
        json_path: Path to input JSON file.
        schema_path: Path to schema file.

    Returns:
        True if JSON is valid, false if not.

    NOTE: Input JSON files are expected to contain a list of objects,
        each of which get validated one at a time by the schema.
    """
    LOGGER.info('Validating %s with %s', json_path, schema_path)
    with open(schema_path, 'r') as schema_fp:
        my_schema = json.loads(jsmin.jsmin(schema_fp.read()))
    
    # NOTE JSON files are expected to be lists of objects, each of which will be validated one at a time.
    with open(json_path, 'r') as json_fp:
        json_list = json.loads(jsmin.jsmin(json_fp.read()))

    validity = []
    for my_obj in json_list:
        validity.append(_object_is_valid(my_obj, my_schema, json_path))
    if not all(validity):
        return False
    return True

def _sanity_check():
    """TODO pending. Sanity check an object. This is meant to be a general use
    function that can sanity check any object, dispatching the correct sanity
    checker function as required. You will likely want a separate module with
    all of the sanity checker functions.

    Sanity checking examples:
        - Ensure talent level prerequisite > 0.
        - Ensure talent ancestry prerequisite is an existing ancestry.
        - Ensure prerequisites are met for all talents on a character sheet.
    """

def main(argv: list) -> None:
    """Process args and sequence through actions.

    Args:
        argv: List of input arguments.
    """
    args = _process_args(argv)

    # Validate the contents of a single JSON file
    if args.json_path and args.schema_path:
        if _validate_json_file(args.json_path, args.schema_path):
            print(f'{args.json_path} is valid!')
        else:
            print(f'{args.json_path} is not valid! Use -d option for more information.')
    else:
        LOGGER.info('Unsupported functionality; you must specify both an input JSON file and a schema with which to validate it.')


if __name__ == '__main__':
    main(sys.argv[1:])