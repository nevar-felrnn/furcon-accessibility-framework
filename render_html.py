#!/usr/bin/env python3
"""
Render the generated Markdown accessibility plan as a clean HTML file.
Usage: python render_html.py
"""

import os
import glob
import markdown
from datetime import datetime

OUTPUT_DIR = "output"

def get_latest_md_file():
    """Find the most recently modified .md file in the output folder."""
    pattern = os.path.join(OUTPUT_DIR, "*.md")
    files = glob.glob(pattern)
    
    if not files:
        print("No Markdown files found in the output folder.")
        print("Run 'python assemble.py' first to generate a document.")
        return None
    
    # Sort by modification time (newest first)
    latest = max(files, key=os.path.getmtime)
    return latest

def extract_cover_fields(md_content):
    """Pull the header block fields out so we can render them as a cover page."""
    fields = {}
    for line in md_content.splitlines():
        line = line.strip()
        if line.startswith("# ") and "cover_title" not in fields:
            fields["cover_title"] = line[2:].strip()
        for label in ("Dates", "Venue", "Accessibility Director", "Generated"):
            if line.startswith(f"**{label}:**"):
                value = line.replace(f"**{label}:**", "").strip().rstrip("  ")
                fields[label.lower().replace(" ", "_")] = value
    return fields


def strip_header_block(md_content):
    """Remove the leading --- … --- header block from the Markdown before conversion."""
    lines = md_content.splitlines()
    # Find the pair of --- delimiters at the top
    in_header = False
    header_end = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_header:
                in_header = True
            else:
                header_end = i + 1
                break
    return "\n".join(lines[header_end:]).lstrip()


def fix_list_spacing(md_content):
    """Ensure a blank line precedes list items that follow a paragraph.

    The Python markdown library requires a blank line before a list when it
    immediately follows a non-blank, non-heading line. Without it, list items
    are rendered as a continuation of the paragraph instead of a <ul>/<ol>.
    """
    lines = md_content.splitlines()
    result = []
    for i, line in enumerate(lines):
        is_list_item = line.startswith("- ") or line.startswith("* ") or (
            len(line) > 2 and line[0].isdigit() and line[1] in ".)" and line[2] == " "
        )
        if is_list_item and i > 0:
            prev = lines[i - 1].strip()
            if prev and not prev.startswith("#") and not prev.startswith("-") and not prev.startswith("*"):
                result.append("")  # insert missing blank line
        result.append(line)
    return "\n".join(result)


def render_to_html(md_path):
    """Convert Markdown to HTML with a clean, readable style."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    render_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    cover = extract_cover_fields(md_content)
    body_md = strip_header_block(md_content)
    body_md = fix_list_spacing(body_md)

    # Convert Markdown to HTML
    # Extensions: 'tables' for budget tables, 'fenced_code' for code blocks
    html_body = markdown.markdown(body_md, extensions=['tables', 'fenced_code', 'toc'])

    # Tag h2 elements that start a new chapter or appendix so CSS can
    # target them for page breaks without breaking every section heading.
    # The toc extension adds id attributes, so we match <h2 ...> not just <h2>.
    import re
    html_body = re.sub(
        r'<h2([^>]*)>((Chapter|Appendix)\b[^<]*)</h2>',
        r'<h2\1 class="chapter-break">\2</h2>',
        html_body
    )

    cover_title = cover.get("cover_title", "Accessibility Plan")
    cover_html = f"""
        <div class="cover">
            <div class="cover-eyebrow">Furry Convention Accessibility Framework</div>
            <h1>{cover_title}</h1>
            <div class="cover-meta">
                <div><strong>Dates</strong> {cover.get('dates', '')}</div>
                <div><strong>Venue</strong> {cover.get('venue', '')}</div>
                <div><strong>Director</strong> {cover.get('accessibility_director', '')}</div>
            </div>
            <div class="cover-generated">Rendered {render_time}</div>
        </div>
    """

    # Wrap in a clean HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{cover_title}</title>
        <style>
            /* ── Page setup ─────────────────────────────────────────── */
            @page {{
                size: letter;
                margin: 1in 1in 0.85in 1in;
                @bottom-center {{
                    content: counter(page);
                    font-size: 9pt;
                    color: #999;
                }}
            }}

            /* ── Base ───────────────────────────────────────────────── */
            body {{
                font-family: Georgia, "Times New Roman", serif;
                font-size: 10.5pt;
                line-height: 1.55;
                color: #1a1a1a;
                max-width: 780px;
                margin: 0 auto;
                padding: 2em 2.5em;
                background-color: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 3em 4em;
                border-radius: 6px;
                box-shadow: 0 2px 16px rgba(0,0,0,0.07);
            }}

            /* ── Headings ───────────────────────────────────────────── */
            h1, h2, h3, h4 {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                color: #1a2e44;
                line-height: 1.25;
                margin-top: 1.5em;
                margin-bottom: 0.4em;
            }}
            h1 {{
                font-size: 20pt;
                border-bottom: 2px solid #1a2e44;
                padding-bottom: 0.3em;
            }}
            h2 {{
                font-size: 14pt;
                border-bottom: 1px solid #cdd8e3;
                padding-bottom: 0.15em;
                margin-top: 2em;
            }}
            h3 {{
                font-size: 11.5pt;
                color: #2c4a6e;
            }}
            h4 {{
                font-size: 10.5pt;
                color: #4a6080;
                font-style: italic;
            }}

            /* ── Body text ──────────────────────────────────────────── */
            p {{ margin: 0 0 0.65em 0; }}
            ul, ol {{
                margin: 0.3em 0 0.75em 0;
                padding-left: 1.5em;
            }}
            li {{ margin-bottom: 0.25em; }}
            li > ul, li > ol {{ margin-top: 0.2em; }}

            /* ── Tables ─────────────────────────────────────────────── */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1.2em 0;
                font-size: 10pt;
            }}
            th, td {{
                border: 1px solid #c8d4e0;
                padding: 7px 10px;
                text-align: left;
                vertical-align: top;
            }}
            th {{
                background-color: #eaf0f6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                font-weight: 600;
                font-size: 9.5pt;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                color: #1a2e44;
            }}
            tr:nth-child(even) td {{ background-color: #f7fafc; }}

            /* ── Other elements ─────────────────────────────────────── */
            code {{
                background-color: #f0f4f8;
                padding: 1px 5px;
                border-radius: 3px;
                font-family: "SFMono-Regular", Consolas, monospace;
                font-size: 9.5pt;
            }}
            blockquote {{
                border-left: 3px solid #5580a0;
                margin: 1em 0;
                padding: 0.5em 1em;
                color: #4a5568;
                background: #f7fafc;
                font-style: italic;
            }}
            hr {{
                border: 0;
                border-top: 1px solid #dde6ee;
                margin: 2em 0;
            }}
            .footer {{
                margin-top: 3em;
                padding-top: 1em;
                border-top: 1px solid #dde6ee;
                font-size: 9pt;
                color: #999;
                text-align: center;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            }}

            /* ── Cover page ─────────────────────────────────────────── */
            .cover {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                min-height: 85vh;
                padding: 3em 0 4em 0;
                border-bottom: 3px solid #1a2e44;
                margin-bottom: 2em;
            }}
            .cover-eyebrow {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                font-size: 9.5pt;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: #5580a0;
                margin-bottom: 0.75em;
            }}
            .cover h1 {{
                font-size: 28pt;
                border-bottom: none;
                margin: 0 0 0.25em 0;
                padding: 0;
                line-height: 1.15;
            }}
            .cover-meta {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                font-size: 10.5pt;
                color: #4a6080;
                margin-top: 1.5em;
                line-height: 2;
            }}
            .cover-meta strong {{
                color: #1a2e44;
                display: inline-block;
                min-width: 9em;
            }}
            .cover-generated {{
                margin-top: 2.5em;
                font-size: 8.5pt;
                color: #aaa;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            }}

            /* ── Print footer ───────────────────────────────────────── */
            .print-footer {{
                display: none;  /* hidden on screen */
            }}

            @media print {{
                body {{
                    background: white;
                    max-width: none;
                    margin: 0;
                    padding: 0.65in 0.85in 0.85in 0.85in;
                    font-size: 10.5pt;
                    color: #000;
                }}
                .container {{
                    box-shadow: none;
                    border-radius: 0;
                    padding: 0;
                    max-width: none;
                }}

                /* Cover fills first page then breaks */
                .cover {{
                    min-height: 0;
                    height: auto;
                    padding-bottom: 0;
                    page-break-after: always;
                    border-bottom-color: #000;
                }}

                /* Only Chapter/Appendix headings get a page break */
                h2.chapter-break {{
                    page-break-before: always;
                    margin-top: 0;
                    padding-top: 0;
                }}

                /* Keep headings with the content that follows */
                h1, h2, h3, h4 {{
                    page-break-after: avoid;
                }}

                /* Avoid breaking inside these elements */
                p, li, blockquote {{
                    orphans: 3;
                    widows: 3;
                }}
                table, figure {{
                    page-break-inside: avoid;
                }}

                /* Running footer — appears from page 2 onward.
                   Page 1 (cover) already shows the render time prominently. */
                .print-footer {{
                    display: block;
                    position: fixed;
                    bottom: 0.3in;
                    left: 0.85in;
                    right: 0.85in;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                    font-size: 7.5pt;
                    color: #888;
                    border-top: 0.5pt solid #ccc;
                    padding-top: 3pt;
                    display: flex;
                    justify-content: space-between;
                }}
                /* Push the footer off page 1 by offsetting it one page height down,
                   then reset. Chrome's fixed+print renders it on every page from
                   where it first appears in the flow. */
                .cover ~ .print-footer {{
                    margin-top: 0;
                }}

                /* Strip screen-only decoration */
                h1 {{ border-bottom-color: #000; }}
                h2 {{ border-bottom-color: #999; margin-top: 0; }}
                th {{ background-color: #e8e8e8 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                tr:nth-child(even) td {{ background-color: #f5f5f5 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                blockquote {{ background: #f5f5f5 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}

                .cover-eyebrow, .cover-generated {{ color: #666; }}
                .cover-meta {{ color: #333; }}
                .footer {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {cover_html}
            {html_body}
            <div class="footer">
                <p>Rendered {render_time} &nbsp;·&nbsp; Furry Convention Accessibility Framework</p>
            </div>
        </div>
        <div class="print-footer">
            <span>{cover_title}</span>
            <span>Rendered {render_time}</span>
        </div>
    </body>
    </html>
    """

    return html_template

def main():
    print("🔍 Looking for the latest generated Markdown file...")
    md_file = get_latest_md_file()
    
    if not md_file:
        return

    print(f"✨ Found: {os.path.basename(md_file)}")
    
    # Derive HTML filename
    html_file = md_file.replace(".md", ".html")
    
    print(f"🎨 Rendering to HTML: {os.path.basename(html_file)}")
    
    html_content = render_to_html(md_file)
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Done! Open {html_file} in your browser to read.")
    print()

if __name__ == "__main__":
    main()