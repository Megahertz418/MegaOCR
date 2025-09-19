# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Mega_OCR.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Borna-PC\\Desktop\\MegaOCR\\scripts\\..\\vendor\\tesseract.exe', '.'), ('C:\\Users\\Borna-PC\\Desktop\\MegaOCR\\scripts\\..\\vendor\\tessdata', 'tessdata'), ('C:\\Users\\Borna-PC\\Desktop\\MegaOCR\\scripts\\..\\vendor\\fonts', 'fonts'), ('C:\\Users\\Borna-PC\\Desktop\\MegaOCR\\scripts\\..\\vendor\\*.dll', '.'), ('C:\\Users\\Borna-PC\\Desktop\\MegaOCR\\scripts\\..\\vendor\\mega_ocr.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Mega_OCR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Borna-PC\\Desktop\\MegaOCR\\vendor\\mega_ocr.ico'],
)
