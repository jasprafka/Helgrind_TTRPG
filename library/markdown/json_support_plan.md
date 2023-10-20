# JSON Support Plan

Rough outline of the different JSON structures I'll need to support.

## Outline

### What do I need to support?

Support in this context means there is a game rule/datatype that needs to be stored in a human-readable/writable way, and there must be a schema for the JSON structure defining that rule/datatype.

#### Ancestries

- Flavor text
- List of ancestry talents
- Traits
    - Tags
    - Age
    - Size
    - Speed
    - Languages
    - Special Senses
- Base HP increase
- Heritage

#### Character Advancement

- Level up table, basically

#### Character sheets

- Name
- Level
    - Current XP
    - XP to next level
- Attributes
    - Score
    - Skill
    - Defense
- Talents
- Ancestry
    - Heritage
- Equipment
    - Weapons
    - Armor
    - Attacks
    - Inventory slots
    - Currency
    - Free Carry Items
- Resources
    - HP
    - FP
    - Stress
    - Toxicity
    - Adrenaline
- Speed
- Size
- Tags
- Magic
    - Sorcery
    - Incantations
- Abilities
    - Spells
    - Techniques
- Reputation
- Senses
- Languages

#### Talents

- Description
- Prerequisites
    - Stat requirements
    - Ancestry
    - Other talents
    - Level (this is also the level of the talent - no need to duplicate data!)
- Mechanical Effects
    - Does the talent increase your speed, HP, armor, etc?
    - Format this in a way that can easily modify your character sheet

#### Abilities (sorceries, incantations, techniques, template for future ability types)

- FP cost
- Description
- Activation
- Range
- Target
- Duration
- Implement
- Attack VS.
    - Effect on hit
    - Effect on miss

#### Equipment

- Description
- Slots
- Value
- How to handle weapons/armor?
    - This'll be a future issue
    - List of equipment types to handle:
        - Weapons
        - Armor
        - Alchemy Items
        - Mechanical Items
        - Magic Items

#### NPC statblocks (monsters, mostly, but stuff like friendly NPCs too)

- Name
- Optional description
- Stats
    - Size
    - Level
    - role
    - XP value
    - speed
    - HP
    - armor
    - Senses
    - Languages
- Traits
- Major Actions
- Minor Actions
- Reactions
- Items
- Attribute Scores

#### NPC Statblock suggestions

- Not sure exactly what to do here, but some ideas:
    - HP/Armor/Dmg by level
    - Expected HP based on level/creature type
- If a statblock falls outside the expected range, offer a warning/suggestion

Each of the above items needs a JSON schema supporting it. The schemas and associated JSON files will each get their own issue for the [initial population project](https://github.com/users/jasprafka/projects/1/views/1). They should all count towards the [initial population milestone](https://github.com/jasprafka/Helgrind_TTRPG/milestone/1).
