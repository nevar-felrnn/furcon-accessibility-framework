# Furry Convention Accessibility Framework

Welcome! This project helps furry conventions build and run an accessibility department from the ground up. Whether you're starting fresh or inheriting a department mid-stream, this framework gives you the structure, processes, and documentation you need.

This is a living document — it grows and improves with every convention that uses it.

---

## How It Works

The framework separates **shared knowledge** from **your convention's private details**:

- **`chapters/`** contains the common guide — everything about running an accessibility department, split into individual chapter files and assembled in the order defined by `toc.md`. It lives here, in this public repository, and any convention can read it, use it, or build on it.

- **Your `convention.yaml`** is your private configuration — your venue details, staff contacts, equipment inventory, budget, and more. This stays in a **separate private repository** that only your team can access.

- **`assemble.py`** combines them. Run it on your computer and it produces a complete, convention-specific document with your details filled in.

```
Public repo (anyone can see)        Private repo (your team only)
┌────────────────────────────┐      ┌──────────────────────────┐
│ chapters/  +  toc.md       │  +   │ convention.yaml          │
│ (the common framework)     │      │ (your private details)   │
└────────────────────────────┘      └──────────────────────────┘
              │                                  │
              └──────────────┬───────────────────┘
                             ▼
                        assemble.py
                             │
                             ▼
              ┌──────────────────────────────┐
              │ Your complete assembled plan  │
              │ (.md — keep this private)     │
              └──────────────────────────────┘
```

The assembled output **never gets posted publicly** — it stays on your computer or in your private team folder.

---

## What's in This Repo

```
accessibility-framework/
├── chapters/                         ← Framework content, one file per chapter
│   ├── intro.md
│   ├── chapter-01-mission-scope.md
│   ├── chapter-02-roles-responsibilities.md
│   └── … (14 chapters + 2 appendices)
├── templates/                        ← Reusable forms and checklists
├── conventions/
│   ├── template/
│   │   └── convention.yaml          ← Copy this to set up your convention
│   └── [your-convention-name]/
│       └── convention.yaml          ← Your convention's specific details
├── toc.md                            ← Controls chapter order during assembly
├── assemble.py                       ← The script that builds your document
├── output/                           ← Generated documents go here (gitignored)
└── README.md                         ← You are here
```

**Your private repository** (separate, one per convention):
```
my-con-accessibility/
├── convention.yaml          ← Your filled-in convention details
└── output/                  ← (optional) Store your assembled outputs here
```

---

## Quick Start

### Step 1: Install Python (if you don't have it)

**Windows:**
Download Python from https://www.python.org/downloads/ and run the installer.
During installation, check the box that says "Add Python to PATH".

**Mac:**
Open Terminal (search for it in Spotlight) and run:
```
python3 --version
```
If it's not installed, your Mac will offer to install it.

**Linux:**
```
sudo apt install python3 python3-pip
```

---

### Step 2: Install the required library

Open a terminal (or Command Prompt on Windows) in this folder and run:

```
pip install pyyaml
```

On Mac/Linux you may need:
```
pip3 install pyyaml
```

---

### Step 3: Set up your convention

1. Copy the `conventions/template/` folder
2. Rename the copy to your convention's name (e.g. `furcationland` — no spaces, use hyphens)
3. Open `convention.yaml` in any text editor (Notepad, TextEdit, VS Code, etc.)
4. Fill in your convention's details — instructions are in the comments

**YAML formatting tips:**
- Lines starting with `#` are comments — they're for you, not the document. Leave them or delete them.
- Text values go inside quotes: `name: "Furcationland"`
- Yes/no values don't use quotes: `asl_contracted: true`
- Numbers don't use quotes: `wheelchair_count: 2`
- If your text contains a colon `:`, wrap the whole value in quotes: `location: "Room 101: East Wing"`
- Leave a value as `""` if you don't know it yet — it will show as `[Not set]` in your document
- **Don't use tabs** — use spaces for indentation

When you're done, save the file and upload it to your private repository.

---

### Step 4: Generate your document

Open a terminal in this folder and run:

**Windows:**
```
python assemble.py
```

**Mac/Linux:**
```
python3 assemble.py
```

The script will show you a numbered list of your conventions. Type the number and press Enter. Your document will appear in the `output/` folder.

---

### Step 5: Share with your team

Share the assembled document through whatever secure channel you use — private Google Drive, email, your private GitHub repository, etc.

When your details change, update `convention.yaml`, re-run the script, and share the new version. The framework updates separately, and you just re-assemble when you want to pull in changes.

---

## Keeping Up With Updates

The framework will be updated over time as the community learns and improves things. To get updates:

1. On this GitHub page, click **Watch** (top right) and choose **Releases only** — you'll get an email when there's a new version.
2. When a new version comes out, download the updated `accessibility-framework.md`.
3. Re-run `assemble.py`. Your `convention.yaml` stays the same — only the framework content updates.

---

## Updating the Framework

The common framework lives in `accessibility-framework.md`. As you learn new things and improve your processes, update this file. All conventions benefit from improvements to the common framework.

Convention-specific details stay in each convention's `convention.yaml` and don't affect anyone else.

---

## Contributing

If you find something wrong, something missing, or something that could be better — please contribute!

- **Found a typo or error?** Open an Issue on GitHub (the "Issues" tab) and describe what you found.
- **Want to suggest new content?** Open an Issue describing what you think should be added and why.
- **Want to submit a fix directly?** Fork this repository, make your changes, and open a Pull Request. If you don't know what that means, an Issue is totally fine.

If your convention has figured out something that works well, please share it. This guide exists to help the whole community.

---

## Frequently Asked Questions

**Do I have to use GitHub?**

No. You can download the files, fill in `convention.yaml` by hand, and run the script locally without ever using GitHub. GitHub just makes it easier to keep up with updates and collaborate with your team.

**Can I change the framework for my convention?**

Yes — fork this repository and adapt it. But consider whether your change would benefit other conventions too. If it would, please open an Issue or Pull Request so everyone can benefit.

**What if my convention uses a different language?**

The framework is currently English-only. Translations are very welcome — open an Issue if you'd like to coordinate a translation effort.

**Who maintains this?**

This framework is maintained by community contributors from the furry convention community. It is shared openly so every convention can benefit.

**Is this legal advice?**

No. This is practical operational guidance, not legal advice. ADA compliance, local accessibility law, and venue contracts involve real legal considerations. Consult appropriate professionals for legal questions.

**Something isn't working — what do I check?**

1. Python is installed and accessible from your terminal
2. You ran `pip install pyyaml`
3. Your `convention.yaml` doesn't have formatting errors (make sure all text values are in quotes)

---

## License

This framework is shared under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to:
- **Share** — copy and redistribute in any format
- **Adapt** — modify, build upon, and use for your convention

Under the following terms:
- **Attribution** — Give credit to the source. Something like "Based on the Furry Convention Accessibility Framework" is sufficient.

You do **not** need to share your private `convention.yaml` or your assembled outputs. Those are yours.

---

*Built with love for the furry convention community. No attendee left behind.*
