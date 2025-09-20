# Contributing to MegaOCR

We welcome contributions!
Bug reports, feature requests, and pull requests all help improve this project.

---

## How to Contribute

1. **Fork** this repository on GitHub.

2. Create a new branch for your work:

   ```bash
   git checkout -b feature/my-feature
   ```

3. Make your changes.

4. **Test** your changes locally before committing.

5. Commit with a clear, descriptive message:

   ```bash
   git commit -m "Add feature: my-feature"
   ```

6. Push your branch to your fork and open a **Pull Request** against `main`.

---

## Guidelines

* Follow [PEP 8](https://peps.python.org/pep-0008/) style conventions for Python.
* Keep commits atomic and descriptive.
* Update documentation (README, CHANGELOG, etc.) if your change affects users.
* For major changes, please open an **Issue** first to discuss.

---

## Development Setup

Run MegaOCR from source without needing the Vendor Bundle:

```bash
git clone https://github.com/Megahertz418/MegaOCR.git
cd MegaOCR
pip install -r requirements.txt
python Mega_OCR.py
```

If you need to **build the portable EXE**, you must also download the matching **Vendor Bundle** from the [Releases page](../../releases) and extract it into `vendor/` before running the build script.

```powershell
scripts\build.ps1 -VendorDir .\vendor
```

---

## Code of Conduct

By participating in this project, you agree to uphold the standards described in the [Contributor Covenant](https://www.contributor-covenant.org/).