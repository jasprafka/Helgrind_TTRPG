# Talent JSON Support Plan

An outline for how to structure and validate the JSON for Helgrind Talents.

## Outline

Structure and support plan.

### Talent Contents

The parts of a Helgrind Talent:
- Description (string, required)
- Prerequisites (dict, required)
    - attribute requirements (dict, not required)
    - Ancestry (string, not required)
    - Other talents (list of str, not required)
    - Level (int, required)
        - this is also the level of the talent - no need to duplicate data!
- Mechanical Effects (pending, probably dict, not required)
    - Does the talent increase your speed, HP, armor, etc?
    - Format this in a way that can easily modify your character sheet

#### Name (string, required)

The name of the talent.

#### Description (string, required)

The descriptive/flavor text of a talent.

#### Prerequisites (dict, required)

A dictionary containing:
- Level (int, required)
    - Level of the talent (typically \[1-10\], but values greater than 10 are technically allowed).
- attribute requirements (dict, not required)
    - Dict with keys:
        - str
        - dex
        - bod
        - int
        - mnd
        - cha
    - The value of each key must be a positive or negative integer
- Ancestry (string, not required)
    - String value associated with an ancestry
    - Emit a warning if the string is not a supported ancestry?
- Other talents (list of str, not required)
    - List with the names of other talents as strings

#### Mechanical Effects
Somehow I want the talent to be able to modify your character sheet during character creation (e.g. talents that increase your HP actually do it on your char sheet, etc). This will be a dict, but formatting is pending.

### Sanity Checking

JSON Schemas are great for validating JSON, but they are strict. Either the JSON is valid, or it isn't. Flexibility and extensibility are desirable - Helgrind only supports levels 1-10 as of 10/21/2023, but it would be nice to allow for future modifications without too much trouble. Instead of hard-coding a level range limit in the JSON, there will be sanity checking functions that ensure a valid json file still follows the expected rules of the RPG.

For example, there may be a valid reason someone wants to create a talent with a prerequisite for an ancestry that doesn't exist, or for a level higher than 10. Instead of making the schema invalidate such JSON, the sanity checking functions will emit a warning to let them know something is awry.

### Talent Storage

Talents will be stored in a JSON file called `talents.json`. This file will contain an unordered list of dictionaries, each defining a single talent.

There is a future script planned (planned in issue #4) that will compile the list of talents into a file called `talents_list.md` which will contain a list of talents organized alphabetically by level. `talents_list.md` will contain only the names, level, and prerequisites of each talent.


### JSON Example

#### Single Talent Object

```json
{
    "name": "my_talent_name",
    "description": "My talent description.",
    "prerequisites": {
        "level": 1,
        "attributes": {
            "str": 0,
            "dex": 0,
            "bod": 0,
            "int": 0,
            "cha": 0,
            "mnd": 0
        },
        "ancestry": "some_ancestry",
        "other_talents": ["other_talent_1", "other_talent_2"]
    },
    "mechanical_effects": {
        "pending": "pending"
    }
}
```

#### The `talents.json` File
```json
[
    {
        "name": "talent_1",
        "description": "talent_1 detailed description.",
        "prerequisites": {
            "level": 1
        }
    },
    {
        "name": "talent_2",
        "description": "talent_2 detailed description.",
        "prerequisites": {
            "level": 2,
            "attributes": {
                "str": 3
            },
            "ancestry": "some_ancestry",
            "other_talents": ["talent_1"]
        }
    }
]
```
