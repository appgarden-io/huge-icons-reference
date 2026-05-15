---
title: "HugeIcons Markdown Reference"
generated_at: "2026-05-15T14:52:51.848Z"
source: "HugeIcons MCP list_icons via @hugeicons/mcp-server"
icon_count: 5130
category_count: 59
tag_count: 10781
tags:
  - "hugeicons"
  - "icon-reference"
  - "agent-search"
---

# HugeIcons Markdown Reference

[![skills.sh](https://skills.sh/b/appgarden-io/huge-icons-reference)](https://skills.sh/appgarden-io/huge-icons-reference)

Generated at: 2026-05-15T14:52:51.848Z

Source: HugeIcons MCP list_icons via @hugeicons/mcp-server

Total icons: 5130

Categories: 59

Search tags: 10781

## Files

- [SKILL.md](SKILL.md): agent skill entrypoint and search workflow.
- [scripts/search_icons.py](scripts/search_icons.py): dependency-free CLI for ranked name, description, category, and tag search.
- [all-icons.md](all-icons.md): complete icon list with descriptions and tags.
- [tag-index.md](tag-index.md): normalized search tags mapped back to icon names.
- [categories/](categories/): one markdown file per HugeIcons category.

## Install as an Agent Skill

Install from `skills.sh`:

```bash
npx skills add appgarden-io/huge-icons-reference
```

This repository is also a skill folder named `hugeicons-icon-reference`. Install it by copying or symlinking this directory into the agent's skills directory, then invoke it whenever an agent needs exact HugeIcons icon identifiers.

Fast local search:

```bash
python3 scripts/search_icons.py "secure checkout" --limit 8
python3 scripts/search_icons.py "terminal command line" --category programming --limit 10
python3 scripts/search_icons.py "ai search" --require-all-terms --limit 8
python3 scripts/search_icons.py "profile settings" --format json --limit 5
```

The search script reads `all-icons.md` as the source of truth and ranks matches across icon names, generated descriptions, categories, and normalized tags.

## Category Files

| Category | Count | File |
| --- | ---: | --- |
| Add Remove | 29 | [add-remove.md](categories/add-remove.md) |
| Ai | 93 | [ai.md](categories/ai.md) |
| Alert | 37 | [alert.md](categories/alert.md) |
| Animation | 35 | [animation.md](categories/animation.md) |
| Arrows | 182 | [arrows.md](categories/arrows.md) |
| Award | 38 | [award.md](categories/award.md) |
| Bookmark | 42 | [bookmark.md](categories/bookmark.md) |
| Buildings | 82 | [buildings.md](categories/buildings.md) |
| Business | 376 | [business.md](categories/business.md) |
| Check | 39 | [check.md](categories/check.md) |
| Clothing | 64 | [clothing.md](categories/clothing.md) |
| Communications | 246 | [communications.md](categories/communications.md) |
| Crypto | 75 | [crypto.md](categories/crypto.md) |
| Dashboard | 24 | [dashboard.md](categories/dashboard.md) |
| Date Time | 81 | [date-time.md](categories/date-time.md) |
| Devices | 195 | [devices.md](categories/devices.md) |
| Download Upload | 24 | [download-upload.md](categories/download-upload.md) |
| E Commerce | 149 | [e-commerce.md](categories/e-commerce.md) |
| Editing | 435 | [editing.md](categories/editing.md) |
| Education | 115 | [education.md](categories/education.md) |
| Emojis | 62 | [emojis.md](categories/emojis.md) |
| Energy | 100 | [energy.md](categories/energy.md) |
| Files Folders | 210 | [files-folders.md](categories/files-folders.md) |
| Filter Sorting | 39 | [filter-sorting.md](categories/filter-sorting.md) |
| Foods | 126 | [foods.md](categories/foods.md) |
| Furnitures | 80 | [furnitures.md](categories/furnitures.md) |
| Games | 135 | [games.md](categories/games.md) |
| Git | 11 | [git.md](categories/git.md) |
| Gym | 50 | [gym.md](categories/gym.md) |
| Hands | 168 | [hands.md](categories/hands.md) |
| Hierarchy | 60 | [hierarchy.md](categories/hierarchy.md) |
| Home | 21 | [home.md](categories/home.md) |
| Image Camera | 76 | [image-camera.md](categories/image-camera.md) |
| Islamic | 45 | [islamic.md](categories/islamic.md) |
| Kitchen | 46 | [kitchen.md](categories/kitchen.md) |
| Layout | 57 | [layout.md](categories/layout.md) |
| Legal | 36 | [legal.md](categories/legal.md) |
| Link Unlink | 27 | [link-unlink.md](categories/link-unlink.md) |
| Login Logout | 16 | [login-logout.md](categories/login-logout.md) |
| Logistics | 93 | [logistics.md](categories/logistics.md) |
| Logos | 193 | [logos.md](categories/logos.md) |
| Maps | 107 | [maps.md](categories/maps.md) |
| Mathematics | 148 | [mathematics.md](categories/mathematics.md) |
| Media | 72 | [media.md](categories/media.md) |
| Medical | 88 | [medical.md](categories/medical.md) |
| Menu | 28 | [menu.md](categories/menu.md) |
| Mouse | 88 | [mouse.md](categories/mouse.md) |
| Notes Tasks | 29 | [notes-tasks.md](categories/notes-tasks.md) |
| Presentation | 15 | [presentation.md](categories/presentation.md) |
| Programming | 78 | [programming.md](categories/programming.md) |
| Science Technology | 22 | [science-technology.md](categories/science-technology.md) |
| Search | 16 | [search.md](categories/search.md) |
| Security | 99 | [security.md](categories/security.md) |
| Settings | 45 | [settings.md](categories/settings.md) |
| Shapes | 16 | [shapes.md](categories/shapes.md) |
| Space | 28 | [space.md](categories/space.md) |
| Users | 70 | [users.md](categories/users.md) |
| Weather | 96 | [weather.md](categories/weather.md) |
| Wifi | 73 | [wifi.md](categories/wifi.md) |

## Notes

- Descriptions are generated from the official icon name, category, and tags because the MCP icon index does not include prose descriptions.
- Tags are normalized to lowercase search tokens and include official tags, icon-name tokens, the full icon name, and category tokens. Numeric-only variant tokens are intentionally omitted because the full icon name remains searchable.
