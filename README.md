[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/Megahertz418/MegaOCR)](../../releases)
[![Downloads](https://img.shields.io/github/downloads/Megahertz418/MegaOCR/total.svg)](../../releases)

# MegaOCR

![MegaOCR UI](docs/User%20Interface.gif)

**MegaOCR** is a **portable OCR application for Windows** powered by [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).  
It can read **PDF / PNG / JPG** and export extracted text to **.txt / .docx / .pdf**.

👉 [Download Latest Portable EXE](../../releases/latest) — *no installation required, just run and use.*

---

## For Users

### Features
- Works out of the box on Windows — **no Python, no Tesseract installation required**.
- Supports **120+ languages** (common models already bundled in the Release).
- Exports to multiple formats: `.txt`, `.docx`, `.pdf`.
- Clean and simple interface built with Tkinter (using `ttkbootstrap`).

### Limitations
- OCR accuracy depends on input quality (high-DPI recommended).
- Complex page layouts may reduce accuracy.
- Current PDF export has **limited RTL shaping** (Persian/Arabic). Use `.docx` or `.txt` for best results.

---

## For Developers

### Run from Source

```bash
git clone https://github.com/Megahertz418/MegaOCR.git
cd MegaOCR
pip install -r requirements.txt
python Mega_OCR.py
````

> Make sure Tesseract `traineddata` files for your target languages are available.

### Build (Windows, PyInstaller)

```bat
pyinstaller --onefile --noconsole ^
  --add-data "tesseract.exe;." ^
  --add-data "tessdata;tessdata" ^
  --add-data "fonts;fonts" ^
  --add-data "*.dll;." ^
  --add-data "mega_ocr.ico;." ^
  --icon=mega_ocr.ico Mega_OCR.py
```

The executable will appear at `dist/Mega_OCR.exe`.

> **Tip:** Use the helper script for clean builds:
>
> ```powershell
> scripts\build.ps1 -VendorDir .\vendor
> ```

---

## Vendor Bundle (for Reproducible Builds)

Each Release ships a **Vendor Bundle ZIP**, which includes:

* `tesseract.exe` + required `*.dll`
* curated `tessdata/` models
* `fonts/`
* `mega_ocr.ico` and `mega_ocr.png`
* all third-party licenses
* `MANIFEST.json` (components + SHA256 hashes)
* `SHA256SUMS.txt`

📥 Available on the [Releases page](../../releases).

> **Note:** End-users **don’t need this ZIP**. It is only for developers who want to reproduce the official Release build.

---



## Project Layout (source repo)

```text
MegaOCR/
│   .gitignore
│   CHANGELOG.md
│   CONTRIBUTING.md
│   LICENSE
│   Mega_OCR.py
│   Mega_OCR.spec
│   README.md
│   requirements.txt
│   SECURITY.md
│   THIRD_PARTY_NOTICES.md
│
├── .github/               # GitHub-specific configs (PR/Issue templates)
│   │   pull_request_template.md
│   └── ISSUE_TEMPLATE/
│           bug_report.md
│           feature_request.md
│
├── docs/                  # Documentation & media (UI preview, etc.)
│       User Interface.gif
│
└── scripts/               # Build & manifest generation helpers
        build.ps1
        generate-manifest.ps1
```

> Note: `vendor/`, `dist/`, and `build/` directories are not committed to the repo.
> They are provided as part of the downloadable **Release assets** (Vendor Bundle ZIP & EXE).

---

## Releases

* Portable EXE (`Mega_OCR.exe`) — recommended for most users.
* Vendor Bundle ZIP — for developers who want reproducible builds.

Both are available on the [Releases page](../../releases).

---

## Troubleshooting

* **Empty OCR output:** Try higher-resolution images or check language settings (e.g., `eng+fas`).
* **Persian/Arabic shaping in PDF:** Use `.docx` or `.txt` instead.
* **Antivirus false positive:** PyInstaller executables are sometimes flagged. Verify integrity with SHA256 checksums in the Vendor Bundle.

> Still stuck? Please [open an Issue](../../issues).

---

## Roadmap

* macOS/Linux support
* Better complex-layout handling
* Optional CLI mode
* Improved RTL shaping in PDF exports

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Security

If you discover a security issue, please follow the process in [SECURITY.md](./SECURITY.md).

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

---

## Third-Party Notices

See [THIRD\_PARTY\_NOTICES.md](./THIRD_PARTY_NOTICES.md) for a list of included components.
Detailed license texts are provided in the **Vendor Bundle ZIP**.

---

## License

* MegaOCR code: [MIT](./LICENSE)
* Tesseract & models: Apache-2.0 (see [THIRD\_PARTY\_NOTICES.md](./THIRD_PARTY_NOTICES.md))
* Fonts: OFL and CC BY 4.0 (see Vendor Bundle)