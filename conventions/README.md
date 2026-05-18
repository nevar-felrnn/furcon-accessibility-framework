# conventions/

This folder holds convention-specific configuration files. Each convention gets its own subfolder containing a `convention.yaml` with that convention's details.

## What's in here

**`template/`** — A blank `convention.yaml` with every field present and commented. Copy this to start a new convention. Committed to the public repo.

**`sample/`** — A fully filled-in `convention.yaml` using generic placeholder values (no real data). Use this to see what a complete configuration looks like, or to test the assembler without setting up your own convention. Committed to the public repo.

**Your convention folder** — Convention-specific YAML files are gitignored and will never be uploaded to GitHub, even if you accidentally run `git add .`. Only `template/` and `sample/` are exceptions.

## How to add your convention

1. Copy the `template/` folder and rename it to your convention's name (no spaces — use hyphens):
   ```
   cp -r conventions/template conventions/my-con-name
   ```
2. Open `conventions/my-con-name/convention.yaml` and fill in your details. The `sample/` folder is a useful reference for what filled-in values look like.
3. Run `python3 assemble.py` from the repository root and select your convention.

## Folder structure

```
conventions/
├── README.md                        ← this file (committed)
├── template/
│   └── convention.yaml              ← blank template (committed)
├── sample/
│   └── convention.yaml              ← example with placeholder values (committed)
└── your-convention/
    └── convention.yaml              ← your private details (gitignored)
```

## Where to store your convention folder

Your `convention.yaml` contains private information — staff contacts, venue details, internal procedures. The recommended approach is to keep your convention's folder in a **separate private repository** and only bring it onto your local machine when you need to assemble a document. See the main README for the full workflow.
