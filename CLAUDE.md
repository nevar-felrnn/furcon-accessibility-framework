# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A Python CLI tool that assembles a convention-specific accessibility planning document by merging a shared framework (split across chapter files) with a convention's private YAML configuration. The framework is public; each convention's `convention.yaml` lives in their own private repository.

## Running the Assembler

```bash
python3 assemble.py
```

The script presents a numbered list of conventions found in `conventions/` and prompts the user to select one. Output is written to `output/{convention-name}-accessibility-plan-{year}.md`.

## Dependencies

- Python >= 3.12 (see `.python-version`)
- `pip install pyyaml`

No external tools (pandoc, etc.) are required — output is Markdown only.

## Architecture

**Key files:**
- `toc.md` — ordered list of chapter files; `assemble.py` reads this to determine what to concatenate and in what order
- `chapters/` — one `.md` file per chapter/appendix; edit individual files here
- `conventions/template/convention.yaml` — canonical YAML template; copy to `conventions/[con-name]/convention.yaml` to add a new convention
- `assemble.py` — loads `toc.md`, concatenates chapter files, applies `{{PLACEHOLDER}}` substitution from the convention's YAML, prepends a convention header, and appends a convention-specific summary

**Placeholder system:**
Chapter files may contain `{{PLACEHOLDER}}` tokens. Keys are derived from `convention.yaml` using dot-notation flattened to `UPPER_SNAKE_CASE`:
```
contacts.safety_lead.phone → {{CONTACTS_SAFETY_LEAD_PHONE}}
```

Special YAML value handling in `flatten()`:
- `None` or `""` → `[Not set]`
- `True` → `Yes`, `False` → `No`
- Lists → comma-joined string (e.g. `["Furpocalypse", "FurCon"]` → `"Furpocalypse, FurCon"`)

`toc.md` format: one chapter path per line, relative to project root. Lines starting with `#` and blank lines are ignored (use `#` for comments).

**Adding a new convention:**
1. Copy `conventions/template/convention.yaml` to `conventions/[con-name]/convention.yaml`
2. Fill in the values
3. Run `python3 assemble.py` and select the convention

**Adding or reordering chapters:**
Edit `toc.md` — add, remove, or reorder lines. Each line is a path relative to the project root.
