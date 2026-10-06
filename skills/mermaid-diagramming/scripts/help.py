#!/usr/bin/env python3
"""Show the purpose and starter syntax for the diagram types in this skill."""

import json
import re
import sys
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "references" / "diagram-types.json"


def normalize(value):
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def describe(entry):
    print(entry["name"])
    print(f"What: {entry['what']}")
    print(f"When: {entry['when']}")
    print(f"How: {entry['how']}")
    if entry.get("minimum_version"):
        print(f"Mermaid version: {entry['minimum_version']} or newer")
    print("Starter:")
    print("```mermaid")
    print(entry["starter"])
    print("```")
    print(f"Official syntax: {entry['docs']}")


def main():
    entries = json.loads(CATALOG.read_text(encoding="utf-8"))
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print("Usage: help.py [help] [list|all|diagram type]")
        print("With no type, list the 34 diagrams. Use a name or declaration for details.")
        return 0
    if args and args[0].casefold() == "help":
        args = args[1:]
    query = " ".join(args).strip()
    if query.casefold() in ("", "help", "list"):
        print("Mermaid diagram types (ask for a name to see when and how to use it):")
        for entry in entries:
            print(f"- {entry['name']}: {entry['what']}")
        return 0
    if query.casefold() == "all":
        for index, entry in enumerate(entries):
            if index:
                print()
            describe(entry)
        return 0
    matches = [
        entry
        for entry in entries
        if normalize(query)
        in {normalize(value) for value in [entry["name"], entry["keyword"], *entry.get("aliases", [])]}
    ]
    if len(matches) == 1:
        describe(matches[0])
        return 0
    print(f"Unknown or ambiguous diagram type: {query}", file=sys.stderr)
    print("Run this command without a type to list the available names.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
