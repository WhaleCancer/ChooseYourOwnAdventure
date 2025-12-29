# Creatures

This directory contains creature entries extracted from various Fighting Fantasy sourcebooks, organized by creature type.

## Incorporated Sourcebooks

The following sourcebooks have been incorporated into this collection:

- **CB77002 - Out of the Pit** - 221 creatures
- **CB77008 - Beyond The Pit** - 213 creatures
- **CB77019 - Return to the Pit** - 214 creatures

**Total:** 648 creatures (649 files due to one duplicate handling)

## Directory Structure

Creatures are organized by type in the following folders:

```
Creatures/
├── Amphibians/          # Amphibious creatures
├── Animals/             # Natural animals and beasts
├── Demons/              # Demonic entities
├── Humanoids/           # Human-like creatures (with subfolders for subtypes)
│   ├── Elves/          # Various elf types
│   ├── Fairies/        # Fairy creatures
│   ├── Faeries/        # Alternative fairy spelling
│   ├── Forces of Evil/ # Evil-aligned humanoids
│   ├── Giants/         # Giant humanoids
│   ├── Halflings/      # Halfling creatures
│   ├── Humans/         # Human variants
│   ├── Ogres/          # Ogre types
│   ├── Orcs/           # Orc variants
│   └── Trolls/         # Troll types
├── Insects/             # Insectoid creatures
├── Magical Creatures/   # Magically created or enhanced beings
├── Molluscs/            # Mollusk-like creatures
├── Monsters/            # Large monstrous creatures
├── Plants/              # Plant-based creatures
└── Undead/              # Undead creatures
```

## Creature Article Format

Each creature article follows a standard format:

- **Title:** Creature name in title case
- **Source:** Sourcebook reference and page number (CB77002, CB77008, or CB77019)
- **Type:** Creature classification
- **Page Image:** Link to the original page image
- **Statistics:** Game statistics (SKILL, STAMINA, etc.)
- **Description:** Detailed description of the creature

## Notes

- All creature files are in Markdown format (.md)
- Filenames use title case with hyphens (e.g., `Wood-Elf.md`)
- If duplicate creature names exist across books, they are distinguished with a suffix (e.g., `Bear-Out-of-the-Pit.md`, `Bear-Beyond-the-Pit.md`)
- Internal links between related creatures are included where appropriate
- Page images are referenced using relative paths to the sourcebook page image directories
