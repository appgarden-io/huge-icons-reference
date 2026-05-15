---
name: hugeicons-icon-reference
description: Searches the local HugeIcons reference for exact icon names and semantically related candidates using icon names, generated descriptions, categories, and normalized tags. Use when a user asks to find HugeIcons icons, choose an icon for UI work, search icon names/tags/descriptions, compare icon candidates, or needs exact HugeIcons icon identifiers for code, design systems, or MCP/tool usage.
---

# HugeIcons Icon Reference

Use this skill to find exact HugeIcons icon identifiers from the bundled local reference. The repository contains 5,130 icons with generated descriptions, categories, and normalized search tags.

## Fast Search Workflow

Icon search progress:
- [ ] Run the bundled search script for the user's concept.
- [ ] Inspect the top candidates and matching reasons.
- [ ] Re-run with category or tag filters when the first pass is broad.
- [ ] Return exact icon names in backticks with a short rationale.

Start with the script instead of manually reading the large markdown tables:

```bash
python3 scripts/search_icons.py "secure checkout" --limit 8
```

Useful variants:

```bash
python3 scripts/search_icons.py "terminal command line" --category programming --limit 10
python3 scripts/search_icons.py "zoom out" --tag search --limit 8
python3 scripts/search_icons.py "ai search" --require-all-terms --limit 8
python3 scripts/search_icons.py "profile settings" --format json --limit 5
python3 scripts/search_icons.py "database sync" --format names --limit 6
```

The script scores exact name matches highest, then phrase matches in tags/name and token matches in name/tags/category/description. Use `--require-all-terms` when a broad term is causing noisy partial matches. Add `--fuzzy` only when the user's query appears misspelled; normal searches are faster without it.

## Reference Files

Load these only when the script output is not enough:

| File | Read when |
| --- | --- |
| `all-icons.md` | You need the complete row for an icon or want to audit the source data. |
| `tag-index.md` | You need to explore a tag directly and see every icon under it. |
| `categories/<category>.md` | The user already knows the category and wants to browse nearby alternatives. |

## Response Guidance

Prefer concise recommendations:

```markdown
Best fit: `shopping-basket-secure-01`

Other good candidates:
- `shopping-basket-secure-02` - alternate basket variant, tagged with secure shopping/cart terms.
- `credit-card-accept` - better if the UI is about payment approval.
```

When using the icon in code, preserve the exact identifier returned by the script. Do not rename, camel-case, or remove numeric suffixes unless the target HugeIcons package explicitly requires a different import format.

## Gotchas

- Descriptions are generated from the official icon name, category, and tags because the HugeIcons MCP index did not include prose descriptions.
- Tags include synonyms and related concepts; a tag hit is a candidate, not proof that the icon visually matches the product need.
- Numeric suffixes such as `-01` and `-02` are separate icons. Show multiple variants when the visual distinction may matter.
- Some official names include unusual spelling or punctuation. Prefer exact script results over inferred names.
- For broad concepts like `user`, `add`, or `arrow`, filter by category or combine terms to avoid noisy results.
