[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/Megahertz418/MegaOCR)](../../releases)
[![Downloads](https://img.shields.io/github/downloads/Megahertz418/MegaOCR/total.svg)](../../releases)

# MegaOCR

![MegaOCR UI](docs/User%20Interface.gif)

**MegaOCR** is a portable, multi-language OCR GUI for Windows, built on Tesseract.  
It reads **PDF / PNG / JPG** and exports to **.txt / .docx / .pdf**.

👉 [Download Latest Release](../../releases/latest)

---

## Features
- 120+ languages (any Tesseract `traineddata`; the Vendor Bundle includes curated models).
- Fully portable on Windows: no Python or Tesseract install required when using the Release binary.
- Clean Tkinter UI (ttkbootstrap).
- Outputs: `.txt`, `.docx`, `.pdf`.

## Limitations
- Lower accuracy on low-DPI / low-quality images.
- Complex / messy layouts may reduce accuracy.
- Note: ReportLab alone does not fully handle complex RTL shaping (e.g., Persian/Arabic).

---

## Run from Source

```bash
pip install -r requirements.txt
python Mega_OCR.py
````

> If you use non-default languages, ensure the related Tesseract `traineddata` files are available on your system.

---

## Build (Windows, PyInstaller)

This project’s portable binary is built with (Windows **CMD** syntax):

```bat
pyinstaller --onefile --noconsole ^
  --add-data "tesseract.exe;." ^
  --add-data "tessdata;tessdata" ^
  --add-data "fonts;fonts" ^
  --add-data "*.dll;." ^
  --add-data "mega_ocr.ico;." ^
  --icon=mega_ocr.ico Mega_OCR.py
```

The output binary will appear at `dist/Mega_OCR.exe`.

> **PowerShell note:** Replace `^` line continuations with backticks `` ` `` or put the command on a single line.

If you extracted the Vendor Bundle (see below) to `vendor/`, copy the files from `vendor/` next to the project root **before** running the command above (or use `scripts/build.ps1`).

> **Build script note:** The provided `scripts/build.ps1` automatically tells PyInstaller to use all required files directly from the `vendor/` folder (no extra files are copied to the project root).

> **Icon note:** The build uses `mega_ocr.ico` from the Vendor Bundle (`vendor/mega_ocr.ico`). Make sure the Vendor Bundle is extracted to `vendor/` before building.

---

## Vendor Bundle (Reproducible Builds)

Each Release ships a **Vendor Bundle ZIP** that contains:

* `tesseract.exe` + required `*.dll`
* curated `tessdata/` (including improved models)
* `fonts/`
* `mega_ocr.ico` and `mega_ocr.png`
* all third-party licenses
* `MANIFEST.json` (components, origin, license, SHA256)
* `SHA256SUMS.txt`

📦 Available on the [Releases page](../../releases).

### Rebuild exactly like the Release

1. Clone this repository.
2. Download the matching Vendor Bundle zip from the Release page and extract it to `vendor/` at the repo root.
3. Either:

   * Run the PyInstaller command above **after copying** vendor files next to the project root, **or**
   * Run the helper script:

   ```powershell
   scripts\build.ps1 -VendorDir .\vendor
   ```

---

## Releases

* Portable EXE (`dist/Mega_OCR.exe`) and the Vendor Bundle ZIP are available on the GitHub [Releases page](../../releases).
* The Vendor Bundle ZIP includes `MANIFEST.json` and `SHA256SUMS.txt` at the root for integrity verification.

---

## Platform Support

* Windows 10/11 x64: ✅ (Portable EXE)
* macOS / Linux: ⏳ (planned)

---

## Troubleshooting

* **Nothing detected / empty output:** Try higher-DPI input, or ensure correct language(s) are selected (e.g., `eng+fas`).
* **Persian/Arabic shaping in PDF:** Current PDF export via ReportLab has limited RTL shaping; use `.txt`/`.docx` for best quality.
* **Antivirus false-positive:** PyInstaller-packed EXEs can be flagged by some AVs. Verify checksums with `SHA256SUMS.txt`.

> If problems persist, please [open an Issue](../../issues).

---

## Project Layout (source repo)

```text
MegaOCR/
  Mega_OCR.py
  Mega_OCR.spec
  /scripts
  README.md
  LICENSE
  THIRD_PARTY_NOTICES.md
  CHANGELOG.md
  CONTRIBUTING.md
  SECURITY.md
  requirements.txt
```

> In the source repository, `dist/`, `build/`, and `vendor/` are excluded via `.gitignore`.

---

## Roadmap

* macOS/Linux support
* Better layout handling for complex documents
* Optional CLI mode
* Proper RTL shaping in PDF output

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Security

If you discover a security vulnerability, please report it responsibly via the process described in [SECURITY.md](./SECURITY.md).

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

---

## Third-Party Notices

See [THIRD\_PARTY\_NOTICES.md](./THIRD_PARTY_NOTICES.md) for bundled components and license references.
All detailed license texts are included in the **Vendor Bundle ZIP**.

---

## License

* MegaOCR code: MIT (see [`LICENSE`](./LICENSE))
* Tesseract & models: Apache-2.0 (see [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md))
* Fonts: OFL and CC BY 4.0 (included in the Vendor Bundle)"# MegaOCR" 
