# conventions/

This folder holds convention-specific configuration files. Each convention gets its own subfolder containing a `convention.yaml` with that convention's private details.

**Convention subfolders are gitignored** — their contents will never be uploaded to GitHub, even if you accidentally run `git add .`. The `template/` folder is the only exception; it contains the public template and is safe to commit.

## How to add a convention

1. Copy the `template/` folder and rename it to your convention's name (no spaces — use hyphens):
   ```
   cp -r conventions/template conventions/furcationland
   ```
2. Open `conventions/furcationland/convention.yaml` and fill in your convention's details.
3. Run `python3 assemble.py` from the repository root and select your convention.

## Folder structure

```
conventions/
├── README.md                        ← this file (committed)
├── template/
│   └── convention.yaml              ← public template (committed)
└── furcationland/
    └── convention.yaml              ← your private details (gitignored)
```

## Where to store your convention folder

Your `convention.yaml` contains private information — staff contacts, venue details, internal procedures. The recommended approach is to keep your convention's folder in a **separate private repository** and only bring it onto your local machine when you need to assemble a document. See the main README for the full workflow.
