#!/usr/bin/env python3
"""Search the bundled HugeIcons markdown reference."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALL_ICONS_PATH = ROOT / "all-icons.md"

STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "glyph",
    "hugeicon",
    "hugeicons",
    "i",
    "icon",
    "icons",
    "need",
    "needs",
    "of",
    "please",
    "show",
    "showing",
    "symbol",
    "the",
    "to",
    "want",
    "with",
}


@dataclass(frozen=True)
class Icon:
    name: str
    category: str
    description: str
    tags: tuple[str, ...]


@dataclass(frozen=True)
class SearchResult:
    icon: Icon
    score: float
    matches: tuple[str, ...]


def normalize_words(value: str) -> str:
    lowered = value.lower()
    lowered = lowered.replace("&", " and ")
    lowered = lowered.replace("+", " plus ")
    lowered = lowered.replace("#", " sharp ")
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def slugify(value: str) -> str:
    return normalize_words(value).replace(" ", "-")


def word_tokens(value: str) -> tuple[str, ...]:
    normalized = normalize_words(value)
    if not normalized:
        return ()
    return tuple(token for token in normalized.split(" ") if token and token not in STOP_WORDS)


def unique_ordered(values: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def query_terms(query: str) -> tuple[str, ...]:
    return unique_ordered(list(word_tokens(query)))


def split_markdown_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split(" | ")]


def strip_backticks(value: str) -> str:
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def parse_tags(value: str) -> tuple[str, ...]:
    return tuple(re.findall(r"`([^`]+)`", value))


def load_icons(path: Path = ALL_ICONS_PATH) -> list[Icon]:
    if not path.exists():
        raise FileNotFoundError(f"Icon reference not found: {path}")

    icons: list[Icon] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue

        parts = split_markdown_row(line)
        if len(parts) != 4:
            continue

        name, category, description, tags = parts
        icons.append(
            Icon(
                name=strip_backticks(name),
                category=category,
                description=description,
                tags=parse_tags(tags),
            )
        )

    return icons


def candidate_terms(icon: Icon) -> tuple[str, ...]:
    values: list[str] = []
    values.extend(word_tokens(icon.name))
    values.extend(word_tokens(icon.category))
    for tag in icon.tags:
        values.extend(word_tokens(tag))
    return unique_ordered(values)


def phrase_in_any(phrase: str, values: tuple[str, ...]) -> bool:
    return any(phrase == value or phrase in value for value in values)


def best_fuzzy_ratio(term: str, candidates: tuple[str, ...]) -> float:
    if len(term) < 4:
        return 0
    return max((SequenceMatcher(None, term, candidate).ratio() for candidate in candidates), default=0)


def add_match(matches: list[str], text: str) -> None:
    if text not in matches:
        matches.append(text)


def score_icon(icon: Icon, query: str, terms: tuple[str, ...], fuzzy: bool) -> tuple[float, tuple[str, ...], set[str]]:
    name_slug = slugify(icon.name)
    category_slug = slugify(icon.category)
    description_words = set(word_tokens(icon.description))
    tag_slugs = tuple(slugify(tag) for tag in icon.tags)
    tag_slug_set = set(tag_slugs)
    tag_words = {token for tag in icon.tags for token in word_tokens(tag)}
    name_words = set(word_tokens(icon.name))
    category_words = set(word_tokens(icon.category))
    all_candidate_terms = candidate_terms(icon) if fuzzy else ()

    query_slug = slugify(query)
    score = 0.0
    matches: list[str] = []
    matched_terms: set[str] = set()

    if query_slug:
        if query_slug == name_slug:
            score += 300
            add_match(matches, "exact icon name")
        elif name_slug.startswith(query_slug):
            score += 180
            add_match(matches, "icon name starts with query")
        elif query_slug in name_slug:
            score += 110
            add_match(matches, "icon name contains query")

        if query_slug in tag_slug_set:
            score += 160
            add_match(matches, "exact tag")
        elif phrase_in_any(query_slug, tag_slugs):
            score += 90
            add_match(matches, "tag phrase")

        if query_slug == category_slug:
            score += 70
            add_match(matches, "category")

    for term in terms:
        term_matched = False

        if term == name_slug:
            score += 90
            add_match(matches, f"name:{term}")
            term_matched = True
        elif term in name_words:
            score += 55
            add_match(matches, f"name token:{term}")
            term_matched = True
        elif any(name_word.startswith(term) for name_word in name_words if len(term) >= 3):
            score += 25
            add_match(matches, f"name prefix:{term}")
            term_matched = True

        if term in tag_slug_set:
            score += 48
            add_match(matches, f"tag:{term}")
            term_matched = True
        elif term in tag_words:
            score += 42
            add_match(matches, f"tag token:{term}")
            term_matched = True
        elif any(tag_word.startswith(term) for tag_word in tag_words if len(term) >= 3):
            score += 16
            add_match(matches, f"tag prefix:{term}")
            term_matched = True

        if term == category_slug or term in category_words:
            score += 28
            add_match(matches, f"category:{term}")
            term_matched = True

        if term in description_words:
            score += 14
            add_match(matches, f"description:{term}")
            term_matched = True

        if not term_matched and fuzzy:
            ratio = best_fuzzy_ratio(term, all_candidate_terms)
            if ratio >= 0.86:
                score += 18 * ratio
                add_match(matches, f"fuzzy:{term}")
                term_matched = True

        if term_matched:
            matched_terms.add(term)

    return score, tuple(matches[:6]), matched_terms


def matches_category(icon: Icon, categories: list[str]) -> bool:
    if not categories:
        return True
    category_slug = slugify(icon.category)
    wanted = {slugify(category) for category in categories}
    return category_slug in wanted


def matches_tags(icon: Icon, tags: list[str]) -> bool:
    if not tags:
        return True
    icon_tag_slugs = {slugify(tag) for tag in icon.tags}
    return all(slugify(tag) in icon_tag_slugs for tag in tags)


def search_icons(
    icons: list[Icon],
    query: str,
    limit: int,
    categories: list[str],
    tags: list[str],
    require_all_terms: bool,
    fuzzy: bool,
) -> list[SearchResult]:
    terms = query_terms(query)
    results: list[SearchResult] = []

    for icon in icons:
        if not matches_category(icon, categories) or not matches_tags(icon, tags):
            continue

        score, matches, matched_terms = score_icon(icon, query, terms, fuzzy)
        base_score = score
        if tags:
            score += 20 * len(tags)
            matches = (*matches, "required tag")
        if categories:
            score += 15
            matches = (*matches, "required category")

        if require_all_terms and terms and not set(terms).issubset(matched_terms):
            continue
        if base_score <= 0 and query:
            continue
        if score <= 0 and not (tags or categories):
            continue

        results.append(SearchResult(icon=icon, score=score, matches=tuple(matches[:7])))

    return sorted(results, key=lambda result: (-result.score, result.icon.name))[:limit]


def result_to_dict(result: SearchResult) -> dict[str, object]:
    return {
        "name": result.icon.name,
        "category": result.icon.category,
        "description": result.icon.description,
        "tags": list(result.icon.tags),
        "score": round(result.score, 2),
        "matches": list(result.matches),
    }


def markdown_table(results: list[SearchResult], query: str) -> str:
    if not results:
        return f"No HugeIcons matches found for `{query}`."

    lines = [
        f"## HugeIcons matches for `{query or 'filtered search'}`",
        "",
        "| Icon | Category | Score | Matches | Description |",
        "| --- | --- | ---: | --- | --- |",
    ]

    for result in results:
        matches = ", ".join(result.matches) if result.matches else "filter match"
        lines.append(
            "| "
            f"`{result.icon.name}` | "
            f"{result.icon.category} | "
            f"{result.score:.1f} | "
            f"{matches} | "
            f"{result.icon.description} |"
        )

    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search the local HugeIcons icon reference.")
    parser.add_argument("query", nargs="*", help="Search words, phrase, or icon name.")
    parser.add_argument("--limit", "-l", type=int, default=12, help="Maximum results to print.")
    parser.add_argument("--category", action="append", default=[], help="Restrict to a category slug/name. Repeatable.")
    parser.add_argument("--tag", action="append", default=[], help="Require an exact normalized tag. Repeatable.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json", "names"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument("--require-all-terms", action="store_true", help="Only show icons matching every query term.")
    parser.add_argument("--fuzzy", action="store_true", help="Enable typo-tolerant matching.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    query = " ".join(args.query).strip()

    if not query and not args.category and not args.tag:
        print("Provide a query, --category, or --tag.", file=sys.stderr)
        return 2
    if args.limit < 1:
        print("--limit must be greater than 0.", file=sys.stderr)
        return 2

    try:
        icons = load_icons()
    except OSError as error:
        print(str(error), file=sys.stderr)
        return 1

    results = search_icons(
        icons=icons,
        query=query,
        limit=args.limit,
        categories=args.category,
        tags=args.tag,
        require_all_terms=args.require_all_terms,
        fuzzy=args.fuzzy,
    )

    if args.format == "json":
        print(json.dumps([result_to_dict(result) for result in results], indent=2))
    elif args.format == "names":
        for result in results:
            print(result.icon.name)
    else:
        print(markdown_table(results, query))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
