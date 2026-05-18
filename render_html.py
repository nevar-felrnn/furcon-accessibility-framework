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

def render_to_html(md_path):
    """Convert Markdown to HTML with a clean, readable style."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert Markdown to HTML
    # Extensions: 'tables' for budget tables, 'fenced_code' for code blocks
    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])

    # Wrap in a clean HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Accessibility Plan</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }}
            h1, h2, h3, h4 {{
                color: #2c3e50;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            h2 {{ border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            p {{ margin-bottom: 1em; }}
            ul, ol {{ margin-bottom: 1em; padding-left: 20px; }}
            li {{ margin-bottom: 0.5em; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1em 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{ background-color: #f2f2f2; }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: monospace;
            }}
            blockquote {{
                border-left: 4px solid #ddd;
                margin: 0;
                padding-left: 15px;
                color: #666;
            }}
            hr {{
                border: 0;
                border-top: 1px solid #eee;
                margin: 2em 0;
            }}
            .footer {{
                margin-top: 3em;
                padding-top: 1em;
                border-top: 1px solid #eee;
                font-size: 0.9em;
                color: #888;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {html_body}
            <div class="footer">
                <p>Generated on {datetime.now().strftime("%B %d, %Y")} | Furry Convention Accessibility Framework</p>
            </div>
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