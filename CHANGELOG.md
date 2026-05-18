# Changelog

All notable changes to the Furry Convention Accessibility Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## How to write a changelog entry

Entries go under `[Unreleased]` until a version is tagged. Each entry is a single bullet point — one change, one line. Aim for a sentence that tells someone *what changed and why it matters to them*, without editorializing.

**Format:** `- [Added/Updated/Fixed/Removed] short description of the change.`

**Good examples:**
- `- Added a quiet room setup checklist to the templates folder.`
- `- Fixed broken placeholder in Chapter 6 that showed [Not set] for ASL vendor name.`
- `- Updated Chapter 3 timeline to recommend contacting interpreters 9 months out instead of 6.`

**Too vague:**
- `- Updated some stuff.`
- `- Fixed a bug.`

**Too much:**
- `- Completely overhauled and rewrote the entire interpreter services chapter from the ground up based on extensive community feedback gathered over several months to better reflect real-world ASL booking timelines and best practices.`

**A few rules:**
- One bullet per change. If you changed three things, write three bullets.
- Use plain language — not everyone reading this is technical.
- File names in backticks: `` `convention.yaml` ``, not "the yaml file".
- Don't editorialize ("massively improved", "finally fixed") — just say what changed.

---

## [Unreleased]

## [1.1.0] - 2026-05-18

### Content
- Lite Mode documentation (`docs/LITE_MODE.md`) for non-technical users.
- 6 new practical templates: Venue Checklist, Budget, Training, Equipment Log, Incident Report, Post-Con Report.

### Tooling
- Multi-team notes integration (`notes/` folder support).
- HTML rendering script (`render_html.py`).
- Validation script (`validate_slots.py`).
- Updated `assemble.py` to support notes injection.
- Improved `toc.md` parsing to strictly ignore comments.

### Fixed
- Fixed validator crash when `toc.md` contains non-file lines.
- Fixed placeholder mismatch in validation logic.

## [1.0.0] - 2026-04-20

### Added
- Initial release of the Furry Convention Accessibility Framework.
- 14 core chapters covering the full lifecycle.
- 2 appendices (Master Checklist, Conditions Reference).
- Python assembler (`assemble.py`) with YAML configuration.
- Basic documentation and setup guides.