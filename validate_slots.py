#!/usr/bin/env python3
"""
Validation Script for the Accessibility Framework
Checks for missing placeholders, unused YAML keys, and broken TOC links.
Usage: python validate_slots.py
"""

import os
import sys
import re
import yaml
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONVENTIONS_DIR = os.path.join(SCRIPT_DIR, "conventions")
TOC_FILE = os.path.join(SCRIPT_DIR, "toc.md")

def load_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"❌ Error: {path} not found.")
        return None

def flatten_keys(data, prefix=""):
    """Flatten a dict into dot-notation keys."""
    keys = []
    for k, v in data.items():
        new_key = f"{prefix}{k}" if prefix else k
        if isinstance(v, dict):
            keys.extend(flatten_keys(v, f"{new_key}."))
        else:
            keys.append(new_key)
    return keys

def find_placeholders(text):
    """Find all {{PLACEHOLDER}} patterns in text."""
    return re.findall(r'\{\{([A-Z0-9_\.]+)\}\}', text)

def validate_toc():
    """Check if all files in toc.md exist."""
    print("🔍 Checking Table of Contents (toc.md)...")
    if not os.path.isfile(TOC_FILE):
        print("   ❌ toc.md not found!")
        return False

    with open(TOC_FILE, "r") as f:
        lines = f.readlines()

    missing = []
    # Inside validate_toc() and load_framework():
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Skip lines that look like comments (start with #)
        if line.startswith("#"):
            continue
        
        # NEW: Skip lines that DO NOT look like file paths
        # (e.g., sentences that don't contain '/' or end in '.md')
        if "/" not in line and not line.endswith(".md"):
            continue
        
        # Now it's definitely a file path
        full_path = os.path.join(os.path.dirname(TOC_FILE), line)
        if not os.path.isfile(full_path):
            missing.append(line)
            
    if missing:
        print(f"   ❌ Missing {len(missing)} chapter file(s):")
        for m in missing:
            print(f"      - {m}")
        return False
    else:
        print("   ✅ All chapter files found.")
        return True
    
def validate_placeholders(selected_convention):
    """Check for missing or unused placeholders."""
    print(f"\n🔍 Validating placeholders for '{selected_convention}'...")
    
    yaml_path = os.path.join(CONVENTIONS_DIR, selected_convention, "convention.yaml")
    if not os.path.isfile(yaml_path):
        print(f"   ❌ {yaml_path} not found. Run assemble.py first.")
        return False

    config = load_yaml(yaml_path)
    if not config:
        return False

    # Get all available keys from YAML (dot notation)
    available_keys_dot = set(flatten_keys(config))
    
    # Transform them to placeholder format (UPPER_SNAKE with underscores)
    available_keys_placeholder = set()
    for key in available_keys_dot:
        placeholder = key.upper().replace(".", "_")
        available_keys_placeholder.add(placeholder)
    
    # Scan all chapter files
    toc_dir = os.path.dirname(TOC_FILE)
    with open(TOC_FILE, "r") as f:
        chapter_files = [
            line.strip() 
            for line in f 
            if line.strip() and not line.strip().startswith("#")
        ]

    all_used_keys = set()
    missing_keys = set()

    for chapter_file in chapter_files:
        chapter_path = os.path.join(toc_dir, chapter_file)
        if not os.path.isfile(chapter_path):
            continue
        
        with open(chapter_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        placeholders = find_placeholders(content)
        for ph in placeholders:
            all_used_keys.add(ph)
            if ph not in available_keys_placeholder:
                missing_keys.add(ph)

    # Report Missing
    if missing_keys:
        print(f"   ❌ Found {len(missing_keys)} placeholder(s) with NO matching YAML key:")
        for k in sorted(missing_keys):
            print(f"      - {{{{{k}}}}}")
    else:
        print("   ✅ All placeholders have matching YAML keys.")

    # Report Unused (Optional cleanup)
    unused_keys = available_keys_placeholder - all_used_keys
    if unused_keys:
        print(f"   ℹ️  Found {len(unused_keys)} YAML key(s) NOT used as placeholders (this is OK if used in appendix):")
        for k in sorted(unused_keys):
            print(f"      - {k}")
    else:
        print("   ℹ️  All YAML keys are used as placeholders.")

    return len(missing_keys) == 0

def main():
    print("=" * 60)
    print("  Framework Validator")
    print("=" * 60)
    print()

    # 1. Check TOC
    toc_ok = validate_toc()
    
    if not toc_ok:
        print("\n⚠️  Fix TOC errors before proceeding.")
        sys.exit(1)

    # 2. Find conventions
    if not os.path.isdir(CONVENTIONS_DIR):
        print("❌ conventions/ folder not found.")
        sys.exit(1)

    conventions = [d for d in os.listdir(CONVENTIONS_DIR) 
                   if os.path.isdir(os.path.join(CONVENTIONS_DIR, d)) and d != "template"]

    if not conventions:
        print("❌ No conventions found. Create one in conventions/ first.")
        sys.exit(1)

    # 3. Validate each convention
    all_ok = True
    for conv in conventions:
        if not validate_placeholders(conv):
            all_ok = False

    print("\n" + "=" * 60)
    if all_ok:
        print("✅ Validation Passed! Ready to generate.")
    else:
        print("❌ Validation Failed. Please fix the errors above.")
    print("=" * 60)
    print()

    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()