#!/usr/bin/env python3
"""
Render a single chapter or template as a standalone HTML file.
Useful for reprinting one section without regenerating the full document.

Usage:
    python render_chapter.py                          # interactive picker
    python render_chapter.py 3                        # Chapter 3 by number
    python render_chapter.py appendix-a               # Appendix A
    python render_chapter.py 3 --convention sample    # with placeholder substitution
"""

import os
import sys
import re
import yaml
import markdown
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOC_FILE = os.path.join(SCRIPT_DIR, "toc.md")
CONVENTIONS_DIR = os.path.join(SCRIPT_DIR, "conventions")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")


# ── Shared helpers ────────────────────────────────────────────────────────────

def load_toc():
    """Return ordered list of (label, path) tuples from toc.md."""
    entries = []
    with open(TOC_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            path = os.path.join(SCRIPT_DIR, line)
            if not os.path.isfile(path):
                continue
            label = os.path.splitext(os.path.basename(line))[0]
            # Make a human-readable label
            label = label.replace("-", " ").title()
            label = re.sub(r'Chapter (\d+)', lambda m: f"Chapter {int(m.group(1))}", label)
            entries.append((label, path))
    return entries


def fix_list_spacing(md_content):
    """Insert blank lines before lists that immediately follow a paragraph."""
    lines = md_content.splitlines()
    result = []
    for i, line in enumerate(lines):
        is_list_item = line.startswith("- ") or line.startswith("* ") or (
            len(line) > 2 and line[0].isdigit() and line[1] in ".)" and line[2] == " "
        )
        if is_list_item and i > 0:
            prev = lines[i - 1].strip()
            if prev and not prev.startswith("#") and not prev.startswith("-") and not prev.startswith("*"):
                result.append("")
        result.append(line)
    return "\n".join(result)


def flatten(data, parent_key="", sep="."):
    items = {}
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten(v, new_key, sep=sep))
        elif isinstance(v, list):
            items[new_key] = ", ".join(str(i) for i in v) if v else "None"
        else:
            items[new_key] = str(v) if v not in (None, "", False, True) else (
                "Yes" if v is True else ("No" if v is False else "[Not set]")
            )
    return items


def apply_placeholders(text, flat_data):
    for key, value in flat_data.items():
        placeholder = "{{" + key.upper().replace(".", "_") + "}}"
        text = text.replace(placeholder, value)
    return text


def load_convention(name):
    """Load and flatten a convention YAML. Returns flat dict or None."""
    yaml_path = os.path.join(CONVENTIONS_DIR, name, "convention.yaml")
    if not os.path.isfile(yaml_path):
        print(f"❌ No convention.yaml found for '{name}'.")
        return None
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    return flatten(config), config


# ── HTML rendering ────────────────────────────────────────────────────────────

PRINT_CSS = """
    @page {
        size: letter;
        margin: 0.75in 0.85in 0.85in 0.85in;
    }

    body {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 10.5pt;
        line-height: 1.55;
        color: #1a1a1a;
        max-width: 780px;
        margin: 0 auto;
        padding: 2em 2.5em;
        background-color: #f5f5f5;
    }
    .container {
        background: white;
        padding: 3em 4em;
        border-radius: 6px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    }

    h1, h2, h3, h4 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        color: #1a2e44;
        line-height: 1.25;
        margin-top: 1.5em;
        margin-bottom: 0.4em;
    }
    h1 { font-size: 20pt; border-bottom: 2px solid #1a2e44; padding-bottom: 0.3em; }
    h2 { font-size: 14pt; border-bottom: 1px solid #cdd8e3; padding-bottom: 0.15em; margin-top: 2em; }
    h3 { font-size: 11.5pt; color: #2c4a6e; }
    h4 { font-size: 10.5pt; color: #4a6080; font-style: italic; }

    p { margin: 0 0 0.65em 0; }
    ul, ol { margin: 0.3em 0 0.75em 0; padding-left: 1.5em; }
    li { margin-bottom: 0.25em; }
    li > ul, li > ol { margin-top: 0.2em; }

    table { width: 100%; border-collapse: collapse; margin: 1.2em 0; font-size: 10pt; }
    th, td { border: 1px solid #c8d4e0; padding: 7px 10px; text-align: left; vertical-align: top; }
    th {
        background-color: #eaf0f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        font-weight: 600; font-size: 9.5pt;
        text-transform: uppercase; letter-spacing: 0.03em; color: #1a2e44;
    }
    tr:nth-child(even) td { background-color: #f7fafc; }

    code {
        background-color: #f0f4f8; padding: 1px 5px; border-radius: 3px;
        font-family: "SFMono-Regular", Consolas, monospace; font-size: 9.5pt;
    }
    blockquote {
        border-left: 3px solid #5580a0; margin: 1em 0; padding: 0.5em 1em;
        color: #4a5568; background: #f7fafc; font-style: italic;
    }
    hr { border: 0; border-top: 1px solid #dde6ee; margin: 1.5em 0; }

    .chapter-meta {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        font-size: 8.5pt;
        color: #aaa;
        margin-bottom: 2em;
        padding-bottom: 0.75em;
        border-bottom: 1px solid #eee;
    }

    .print-footer { display: none; }

    @media print {
        body { background: white; max-width: none; margin: 0; padding: 0.65in 0.85in 0.85in 0.85in; color: #000; }
        .container { box-shadow: none; border-radius: 0; padding: 0; max-width: none; }
        h1, h2, h3, h4 { page-break-after: avoid; }
        p, li, blockquote { orphans: 3; widows: 3; }
        table { page-break-inside: avoid; }
        th { background-color: #e8e8e8 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        tr:nth-child(even) td { background-color: #f5f5f5 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        blockquote { background: #f5f5f5 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .print-footer {
            display: flex;
            position: fixed;
            bottom: 0.3in;
            left: 0.85in;
            right: 0.85in;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 7.5pt;
            color: #888;
            border-top: 0.5pt solid #ccc;
            padding-top: 3pt;
            justify-content: space-between;
        }
    }
"""


def render_chapter_html(label, md_content, convention_name, render_time):
    md_content = fix_list_spacing(md_content)
    html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])

    convention_line = f" &nbsp;·&nbsp; {convention_name}" if convention_name else ""
    meta_line = f"Furry Convention Accessibility Framework{convention_line} &nbsp;·&nbsp; Rendered {render_time}"

    footer_left = f"{label}{convention_line}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{label}</title>
    <style>{PRINT_CSS}</style>
</head>
<body>
    <div class="container">
        <div class="chapter-meta">{meta_line}</div>
        {html_body}
    </div>
    <div class="print-footer">
        <span>{footer_left}</span>
        <span>Rendered {render_time}</span>
    </div>
</body>
</html>"""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    convention_name = None
    convention_flat = None

    # Parse --convention flag
    if "--convention" in args:
        idx = args.index("--convention")
        if idx + 1 < len(args):
            convention_name = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        else:
            print("❌ --convention requires a name, e.g. --convention sample")
            sys.exit(1)

    if convention_name:
        result = load_convention(convention_name)
        if result is None:
            sys.exit(1)
        convention_flat, _ = result
        print(f"✅ Loaded convention: {convention_name}")

    entries = load_toc()
    if not entries:
        print("❌ No chapters found in toc.md.")
        sys.exit(1)

    # Resolve which chapter to render
    if args:
        selector = args[0].lower().strip()

        # Match by number (1-based index into chapters, skipping intro)
        if selector.isdigit():
            num = int(selector)
            # Find chapter entries by number in filename
            matches = [(l, p) for l, p in entries
                       if re.search(rf'chapter-0*{num}\b', p)]
            if not matches:
                print(f"❌ No chapter found for number {num}.")
                sys.exit(1)
            label, path = matches[0]

        # Match appendix-a / appendix-b
        elif selector.startswith("appendix"):
            matches = [(l, p) for l, p in entries if selector.replace(" ", "-") in p]
            if not matches:
                print(f"❌ No appendix found matching '{selector}'.")
                sys.exit(1)
            label, path = matches[0]

        # Match template by keyword
        else:
            matches = [(l, p) for l, p in entries if selector in p.lower()]
            if not matches:
                print(f"❌ No entry found matching '{selector}'.")
                sys.exit(1)
            label, path = matches[0]

    else:
        # Interactive picker
        print("\nAvailable chapters and templates:")
        for i, (label, _) in enumerate(entries, 1):
            print(f"  {i:2}. {label}")
        print()
        while True:
            try:
                choice = input("Enter a number: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(entries):
                    label, path = entries[idx]
                    break
                print(f"Please enter a number between 1 and {len(entries)}.")
            except (ValueError, KeyboardInterrupt):
                print("\nCancelled.")
                sys.exit(0)

    # Load and optionally substitute
    with open(path, "r", encoding="utf-8") as f:
        md_content = f.read()

    if convention_flat:
        md_content = apply_placeholders(md_content, convention_flat)

    render_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    html = render_chapter_html(label, md_content, convention_name, render_time)

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    slug = os.path.splitext(os.path.basename(path))[0]
    if convention_name:
        slug = f"{convention_name}-{slug}"
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Rendered: {os.path.basename(out_path)}")
    print(f"   Open: {out_path}")
    print()


if __name__ == "__main__":
    main()
