# Scripts Plans
Plans for the various scripts I want to make.

## Strictly Necessary Functionality
This list includes all of the 'must-haves' for [initial population project](https://github.com/users/jasprafka/projects/1/views/1). They all need their own issue under the project.
- Schema validator (_This is one of the first things you have to do!_)
    - Functionality to validate a single JSON file with a single schema (preferably auto-detect the schema!) as well as to validate all JSON files under data
        - If a JSON doesn't have a schema associated with it, let the user know that it hasn't been validated
- database compiler
    - You will need a script to create lists on your behalf
    - You don't want to have to manually maintain the lists of talents, spells, etc.
    - Instead, just have those things be in their JSON and create a script that tallies up the total number/name of everything in several long lists
        - These lists will get updated very frequently
- Python package requirements
    - Basically a `requirements.txt` file and an updater script to ensure it's up-to-date, as well as ensure any other requirements are up-to-date.

## Long-Term Script Ideas
Ideas for scripts that I want to make eventually.
- Character generator
    - Allows you to easily and quickly create a character of any level
    - Also allows you to update any part of an existing character (level, talents, equipment, etc.)
- NPC Statblock generator

## How to create codeblocks in markdown
Here is an example of a code block (in python):
```python
def function():
    return
```
Using the syntax above, you can create blocks of any supported language (including JSON)!

```json
{
    "key": "value",
    "other_key": ["list", "of", "vals"],
    "third_key": {
        "val_dict": 8,
        "pretty_cool": true
    }
}
```