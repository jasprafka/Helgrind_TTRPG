"""Script to validate JSON files using the schemas under <ROOT>/library/schemas/"""

import os
import sys
import json
import logging
import argparse
import utilities
import jsonschema

LOGGER = logging.getLogger(os.path.basename(__file__))
"""Logger for this module."""

def _process_args(argv: list) -> argparse.Namespace:
    """Parse and process arguments; convert to argparse.Namespace object.

    Args:
        argv: List of input arguments.

    Returns:
        args: Parsed args with args as properties on the object.
    """
    # TODO update description
    parser = argparse.ArgumentParser(os.path.basename(__file__), description='Pending description.')
    args = utilities.parser_setup(parser, argv, LOGGER)

    return args

def main(argv: list) -> None:
    """Process args and sequence through actions.

    Args:
        argv: List of input arguments.
    """
    args = _process_args(argv)
    # TODO:
        # Handle a case with a single input JSON file and a single input SCHEMA

if __name__ == '__main__':
    main(sys.argv[1:])