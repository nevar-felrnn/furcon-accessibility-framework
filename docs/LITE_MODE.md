# Lite Mode: Using the Framework Without Python

Not everyone wants to install Python, manage YAML files, or run scripts. That's completely fine. You can still use this framework effectively with nothing more than a text editor and a web browser.

This guide shows you how.

---

## What You Get Without Scripts

The framework's **chapters** and **templates** are just Markdown files — plain text that any human can read. You don't need any software to use them.

What you **lose** without the scripts:
- Automatic placeholder substitution (your convention name, contacts, etc. won't be filled in)
- The neat assembled single-document output
- The HTML rendering

What you **keep**:
- All the advice, checklists, and procedures
- All the templates (just fill them in by hand)
- All the knowledge

That's the important stuff.

---

## Option A: Read the Chapters Directly

The `chapters/` folder contains all the framework content. Just open any chapter file in:

- **Any text editor** (Notepad, TextEdit, VS Code, etc.)
- **Any Markdown viewer** (most code editors have one built in)
- **Right here on GitHub** (just click the file)

The chapters are numbered in the order you'll need them:
1. Mission & Scope
2. Roles & Responsibilities
3. Planning Timeline
4. Venue Assessment
5. Budget & Resources
6. Interpreter Services
7. Equipment & Mobility Aids
8. Staff Recruitment & Training
9. Badge Emblem System
10. Accessibility Desk Operations
11. Quiet Room
12. Cross-Department Coordination
13. At-Con Operations
14. Post-Con & Continuous Improvement

Plus two appendices:
- Appendix A: Master Checklist
- Appendix B: Conditions & Accommodations Reference

Read them in order, skip to what you need, or just bookmark the ones relevant to your role.

---

## Option B: Download and Customize Manually

1. **Download the repo** as a ZIP file:
   - Go to the GitHub page
   - Click the green **Code** button
   - Select **Download ZIP**
   - Extract it anywhere on your computer

2. **Make it yours:**
   - Open any chapter file in your text editor
   - Use **Find & Replace** to swap generic terms with your convention's info:
     - Find: `[Convention Name]` → Replace: `Furcationland`
     - Find: `[Not set]` → Replace: your actual details
   - Save the edited files in a separate folder so you don't lose your changes when the framework updates

3. **Use the templates:**
   - Open any template in the `templates/` folder
   - Print it, fill it in by hand, or edit it digitally
   - The templates are designed to work on paper too

---

## Option C: Use Google Docs Instead

If your team collaborates in Google Docs:

1. Download the ZIP (see Option B)
2. Upload the chapter files to Google Drive
3. Open each file in Google Docs (it will convert from Markdown automatically)
4. Share with your team and edit collaboratively

**Note:** Google Docs may not perfectly preserve Markdown formatting (tables, checkboxes). You may need to do some manual cleanup after importing.

---

## Option D: Ask Someone to Run the Scripts for You

If you want the assembled document but don't want to run Python yourself:

1. Fill in the `convention.yaml` file (it's just a text file — open it in Notepad)
2. Send it to someone on your team who is comfortable with Python
3. Ask them to run `assemble.py` and send you the output
4. Open the resulting `.html` file in your browser to read it

The YAML file has comments explaining every field. You don't need to understand YAML — just follow the instructions in the comments.

---

## When to Upgrade to the Full System

The full script-based system is worth using when:

- You have multiple conventions and want to generate separate documents for each
- You want your convention-specific details automatically filled in
- You have team members adding notes in the `notes/` folder
- You want to regenerate the document whenever the framework updates

If any of those apply to you, see the main [README.md](../README.md) for setup instructions.

---

## What About Updates?

When the framework is updated (new chapters, improved templates, etc.):

1. Download the new ZIP
2. Compare the new chapters with your customized versions
3. Copy over any new content you want
4. Keep your customized details

This is manual work, but it's straightforward. The framework doesn't change drastically between versions — you'll mostly be picking up new tips and minor improvements.

---

*You don't need to be technical to make your convention accessible. The tools are here to help, not to gatekeep.*