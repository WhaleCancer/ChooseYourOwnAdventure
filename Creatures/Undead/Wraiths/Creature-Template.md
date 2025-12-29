# Creature Entry Template

## Structure

1. **Title** - Creature name in title case

2. **Statistics Block** - Bullet list with all stats:
   - SKILL
   - STAMINA
   - ATTACKS
   - WEAPON (link to weapon file if applicable)
   - ARMOR (American spelling)
   - DAMAGE MODIFIER
   - HABITAT
   - NUMBER ENCOUNTERED
   - TYPE
   - REACTION
   - INTELLIGENCE

3. **Offense** (if creature has a weapon)
   - Table format with roll values (1, 2, 3, 4, 5, 6, 7+) as column headers
   - Weapon name as row label (plain text, not linked)
   - Only include if creature has a weapon
   - Look up weapon damage track in `RULES/Combat/Weapons/Weapons-Fighting-Fantasy.md`
   - Link weapon name in WEAPON stat line, not in the table
   - Add any special attack abilities (like Life Drain, Paralysis) as riders below the table
   - **Note on similar abilities:** If multiple creatures share a similar ability but with different mechanics (e.g., Paralysis that takes 3 hits vs 4 hits), use a different ability name to distinguish them (e.g., "Paralysis" for the standard version, "Greater Paralysis" for the more powerful version)

4. **Defense** (if creature has special defensive properties)
   - Bullet list of defensive properties
   - Merge related abilities into single entries where appropriate (e.g., "Incorporeal: Normal weapons pass through, causing no damage; can only be harmed by magic or silver weapons")
   - Only include if creature has special defensive properties (not just standard armor)

5. **Description** - Full original text from source

6. **Creating [Creature Name]** (only if there is a way to create the creature)
   - Include if the creature can be created through spells, rituals, or other means
   - Link to the relevant spell or method
   - Include key details: magic point cost, casting time, requirements, limitations
   - Place after Description section

7. **Footer** - Single line with:
   - Source: Book code, book name, Pages [X](link), [Y](link) (comma-separated, each page number links to its page image)
   - Attribution: Creature name from Book Name by Author. [Illustration](link) by Illustrator Name. (if illustration exists)
   - Separated by pipes (|)

## Notes

- Use American spelling for "ARMOR"
- Weapon links go in the WEAPON stat line, not in the Offense table
- Offense section only if creature has a weapon
- Defense section only if creature has special defensive properties (incorporeal, vulnerabilities, etc.)
- Merge related defense abilities into single entries for clarity
- Creating section only if there is a documented way to create the creature
- Page numbers should be comma-separated with each page number linking to its respective page image
- Illustration link should be in the attribution section, not separate
- Source and attribution should be on one line separated by pipes
