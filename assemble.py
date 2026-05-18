#!/usr/bin/env python3
"""
Furry Convention Accessibility Framework - Document Assembler
=============================================================
Enhanced to support multi-team notes integration.
"""

import os
import sys
import yaml
import re
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONVENTIONS_DIR = os.path.join(SCRIPT_DIR, "conventions")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
TOC_FILE = os.path.join(SCRIPT_DIR, "toc.md")

# ── Helpers ──────────────────────────────────────────────────────────────────
def find_conventions():
    if not os.path.isdir(CONVENTIONS_DIR):
        return []
    return [
        name for name in sorted(os.listdir(CONVENTIONS_DIR))
        if os.path.isdir(os.path.join(CONVENTIONS_DIR, name))
        and name != "template"
    ]

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_framework(toc_path):
    toc_dir = os.path.dirname(toc_path)
    if not os.path.isfile(toc_path):
        print(f"Error: toc.md not found at {toc_path}")
        sys.exit(1)

    chapters = []
    with open(toc_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and lines starting with # (comments)
            if not line or line.startswith("#"):
                continue
            
            # Ensure the path is relative to the toc_dir
            chapter_path = os.path.join(toc_dir, line)
            if not os.path.isfile(chapter_path):
                print(f"Warning: Chapter file not found, skipping: {chapter_path}")
                continue
            chapters.append(load_text(chapter_path))

    return "\n\n".join(chapters)

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

def collect_notes(notes_dir):
    if not os.path.isdir(notes_dir):
        return ""
    
    notes_content = []
    for filename in sorted(os.listdir(notes_dir)):
        if not filename.endswith(".md"):
            continue
        
        filepath = os.path.join(notes_dir, filename)
        content = load_text(filepath)
        
        lines = content.split('\n')
        current_section = None
        section_lines = []
        
        for line in lines:
            match = re.match(r'^#\s+([a-zA-Z0-9\-_]+)\s*(?:-.*)?$', line.strip())
            if match:
                if current_section:
                    notes_content.append(f"### {current_section.title()}\n" + "\n".join(section_lines))
                current_section = match.group(1).replace("-", " ").title()
                section_lines = []
            else:
                if current_section:
                    section_lines.append(line)
        
        if current_section:
            notes_content.append(f"### {current_section.title()}\n" + "\n".join(section_lines))
    
    return "\n\n".join(notes_content)

def build_convention_header(config):
    c = config.get("convention", {})
    v = config.get("venue", {})
    contacts = config.get("contacts", {})
    director = contacts.get("accessibility_director", {})

    lines = [
        "---",
        "",
        f"# {c.get('name', '[Convention Name]')} — Accessibility Plan {c.get('year', '')}",
        "",
        f"**Dates:** {c.get('dates', '[Not set]')}  ",
        f"**Venue:** {v.get('name', '[Not set]')}  ",
        f"**Accessibility Director:** {director.get('name', '[Not set]')}  ",
        f"**Generated:** {datetime.now().strftime('%B %d, %Y')}  ",
        "",
        "*This document was generated from the Furry Convention Accessibility Framework.*",
        "*Common framework content applies to all conventions. Convention-specific details*",
        "*are drawn from this convention's configuration and notes.*",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)

def build_convention_appendix(config):
    c = config.get("convention", {})
    v = config.get("venue", {})
    contacts = config.get("contacts", {})
    desk = config.get("desk_hours", {})
    interp = config.get("interpreter_services", {})
    equip = config.get("equipment", {})
    budget = config.get("budget", {})
    shared = config.get("shared_resources", {})

    def val(d, key, fallback="[Not set]"):
        return str(d.get(key) or fallback)

    def yn(d, key):
        return "Yes" if d.get(key) else "No"

    lines = [
        "---",
        "",
        "## Convention-Specific Details",
        "",
        f"### {val(c, 'name')} Configuration Summary",
        "",
        "**Convention**",
        f"- Name: {val(c, 'name')}",
        f"- Year: {val(c, 'year')}",
        f"- Dates: {val(c, 'dates')}",
        f"- Website: {val(c, 'website')}",
        "",
        "**Venue**",
        f"- Name: {val(v, 'name')}",
        f"- Address: {val(v, 'address')}",
        f"- Accessibility Desk Location: {val(v, 'accessibility_desk_location')}",
        f"- Quiet Room Location: {val(v, 'quiet_room_location')}",
        f"- Registration Location: {val(v, 'registration_location')}",
        f"- Notes: {val(v, 'notes')}",
        "",
        "**Desk Hours**",
        f"- Open: {val(desk, 'open')}",
        f"- Close: {val(desk, 'close')}",
        f"- Notes: {val(desk, 'notes')}",
        "",
        "**Key Contacts**",
    ]

    for role, label in [
        ("accessibility_director", "Accessibility Director"),
        ("accessibility_assistant_director", "Assistant Director"),
        ("safety_lead", "Safety Lead"),
        ("it_lead", "IT Lead"),
        ("registration_lead", "Registration Lead"),
        ("convention_chair", "Convention Chair"),
    ]:
        person = contacts.get(role, {})
        name = person.get("name") or "[Not set]"
        email = person.get("email") or "[Not set]"
        lines.append(f"- {label}: {name} ({email})")

    lines += [
        "",
        "**Interpreter Services**",
        f"- ASL Contracted: {yn(interp, 'asl_contracted')}",
        f"- ASL Vendor: {val(interp, 'asl_vendor')}",
        f"- ASL Cost: {val(interp, 'asl_cost')}",
        f"- Rooms Covered: {val(interp, 'asl_rooms_covered')}",
        f"- CART Contracted: {yn(interp, 'cart_contracted')}",
        f"- CART Vendor: {val(interp, 'cart_vendor')}",
        f"- Notes: {val(interp, 'notes')}",
        "",
        "**Equipment**",
        f"- Wheelchairs: {val(equip, 'wheelchair_count', '0')}",
        f"- Transport Chairs: {val(equip, 'transport_chair_count', '0')}",
        f"- Walkers: {val(equip, 'walker_count', '0')}",
        f"- Canes: {val(equip, 'cane_count', '0')}",
        f"- Scooters: {val(equip, 'scooter_count', '0')}",
        f"- Ownership Model: {val(equip, 'ownership_model')}",
        f"- Storage Location: {val(equip, 'storage_location')}",
        f"- Liability Waiver Required: {yn(equip, 'liability_waiver_required')}",
        f"- Liability Waiver Confirmed: {yn(equip, 'liability_waiver_confirmed')}",
        "",
        "**Budget**",
        f"- Total Allocated: {val(budget, 'total_allocated')}",
        f"- Interpreter Budget: {val(budget, 'interpreter_budget')}",
        f"- Equipment Budget: {val(budget, 'equipment_budget')}",
        f"- Printed Materials: {val(budget, 'printed_materials_budget')}",
        f"- Contingency: {val(budget, 'contingency_budget')}",
        "",
        "**Shared Resources**",
        f"- Partner Conventions: {val(shared, 'partner_conventions')}",
        f"- Shared Equipment: {yn(shared, 'shared_equipment')}",
        f"- Primary Storage Convention: {val(shared, 'primary_storage_convention')}",
        f"- Transport Notes: {val(shared, 'transport_notes')}",
        "",
    ]

    return "\n".join(lines)

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 60)
    print("  Furry Convention Accessibility Framework")
    print("  Document Assembler (Enhanced)")
    print("=" * 60)
    print()

    conventions = find_conventions()
    if not conventions:
        print("No conventions found in the conventions/ folder.")
        print("Copy conventions/template/ and fill in convention.yaml.")
        sys.exit(1)

    print("Available conventions:")
    for i, name in enumerate(conventions, 1):
        print(f"  {i}. {name}")
    print()

    while True:
        try:
            choice = input("Enter the number of the convention to generate: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(conventions):
                selected = conventions[idx]
                break
            else:
                print(f"Please enter a number between 1 and {len(conventions)}.")
        except (ValueError, KeyboardInterrupt):
            print("\nCancelled.")
            sys.exit(0)

    print(f"Generating document for: {selected}")

    yaml_path = os.path.join(CONVENTIONS_DIR, selected, "convention.yaml")
    if not os.path.isfile(yaml_path):
        print(f"Error: No convention.yaml found at {yaml_path}")
        sys.exit(1)

    config = load_yaml(yaml_path)
    flat = flatten(config)

    framework_text = load_framework(TOC_FILE)
    framework_text = apply_placeholders(framework_text, flat)

    notes_dir = os.path.join(CONVENTIONS_DIR, selected, "notes")
    notes_text = collect_notes(notes_dir)
    
    header = build_convention_header(config)
    appendix = build_convention_appendix(config)
    
    full_document = header + framework_text
    if notes_text:
        full_document += "\n\n---\n\n## Convention-Specific Notes\n\n" + notes_text
    full_document += "\n\n" + appendix

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    con_name = config.get("convention", {}).get("name", selected).replace(" ", "-").lower()
    con_year = config.get("convention", {}).get("year", "")
    filename = f"{con_name}-accessibility-plan-{con_year}.md".strip("-")
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_document)

    print()
    print(f"Document generated successfully!")
    print(f"Output: {output_path}")
    if notes_text:
        print(f"  • Included {len(notes_text.split('###')) - 1} note sections from team members.")
    print()

if __name__ == "__main__":
    main()