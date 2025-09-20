import os
import fitz
import cv2
import numpy as np
import pytesseract
from PIL import Image
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
import tkinter as tk
from tkinter import filedialog, ttk
import ttkbootstrap as tb
from tkinter import Checkbutton, BooleanVar, Toplevel, Frame, Scrollbar
import threading
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
pytesseract.pytesseract.tesseract_cmd = os.path.join(BASE_DIR, "tesseract.exe")
TESSDATA_DIR = os.path.join(BASE_DIR, "tessdata")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
def try_register_font(ttf_path, font_name):
    if os.path.exists(ttf_path):
        try:
            pdfmetrics.registerFont(TTFont(font_name, ttf_path))
            return True
        except Exception as e:
            print(f"Font register error for {font_name}: {e}")
    return False
FONT_VAZ = os.path.join(FONTS_DIR, "Vazirmatn-Regular.ttf")
FONT_NOTO = os.path.join(FONTS_DIR, "NotoSans-Regular.ttf")
FONT_CJK_TTF = os.path.join(FONTS_DIR, "Noto Sans CJK SC Regular.ttf")
FONT_CJK_OTF = os.path.join(FONTS_DIR, "Noto Sans CJK SC Regular.otf")
HAS_VAZ = try_register_font(FONT_VAZ, "Vazirmatn")
HAS_NOTO = try_register_font(FONT_NOTO, "NotoSans")
HAS_CJK_TTF = try_register_font(FONT_CJK_TTF, "NotoSansCJK")
HAS_CJK_OTF = try_register_font(FONT_CJK_OTF, "NotoSansCJKsc")
if not (HAS_VAZ or HAS_NOTO or HAS_CJK_TTF or HAS_CJK_OTF):
    print("Warning: No custom fonts registered; falling back to Helvetica")
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 15, 15)
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 5)
    return th
def pdf_to_images(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(np.array(img))
    return images
def load_image(path):
    img = cv2.imread(path)
    return [img] if img is not None else []
def extract_text_from_images(images, languages):
    all_text = ""
    lang_str = '+'.join(languages)
    for idx, img in enumerate(images, 1):
        processed = preprocess_image(img)
        text = pytesseract.image_to_string(processed, config=f'--oem 3 --psm 3 -l {lang_str}')
        all_text += f"\nPage {idx}:\n{text.strip()}\n"
    return all_text
def save_as_txt(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
def save_as_docx(text, output_path):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(output_path)
def save_as_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    text_lines = text.split("\n")
    y = height - 50
    font = 'Vazirmatn' if HAS_VAZ else 'NotoSans' if HAS_NOTO else 'Helvetica'
    c.setFont(font, 12)
    for line in text_lines:
        if y < 50:
            c.showPage()
            c.setFont(font, 12)
            y = height - 50
        c.drawString(50, y, line)
        y -= 15
    c.save()
def run_ocr_pipeline(input_path, output_path, output_format, languages):
    if not languages:
        raise ValueError("At least one language must be selected.")
    ext = os.path.splitext(input_path)[-1].lower()
    if ext == ".pdf":
        images = pdf_to_images(input_path)
    else:
        images = load_image(input_path)
    if not images:
        raise ValueError("Invalid image/file.")
    text = extract_text_from_images(images, languages)
    if output_format == "txt":
        save_as_txt(text, output_path)
    elif output_format == "docx":
        save_as_docx(text, output_path)
    elif output_format == "pdf":
        save_as_pdf(text, output_path)
    else:
        raise ValueError("Unsupported output format.")
class MessageDialog(Toplevel):
    def __init__(self, parent, title, message, icon_type="info"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        try:
            self.iconbitmap(os.path.join(BASE_DIR, "mega_ocr.ico"))
        except Exception:
            pass
        if icon_type == "error":
            self.icon_name = "error"
        elif icon_type == "warning":
            self.icon_name = "warning"
        elif icon_type == "info":
            self.icon_name = "info"
        else:
            self.icon_name = "info"
        frame = Frame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        icon_label = ttk.Label(frame, text=icon_type.upper(), font=("Arial", 24))
        icon_label.pack(pady=10)
        message_label = ttk.Label(frame, text=message, wraplength=350, justify="center")
        message_label.pack(pady=10)
        tb.Button(frame, text="OK", command=self.destroy, bootstyle="primary").pack(pady=10)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
def show_error(parent, title, message):
    dlg = MessageDialog(parent, title, message, "error")
    parent.wait_window(dlg)
def show_warning(parent, title, message):
    dlg = MessageDialog(parent, title, message, "warning")
    parent.wait_window(dlg)
def show_info(parent, title, message):
    dlg = MessageDialog(parent, title, message, "info")
    parent.wait_window(dlg)
class LanguageDialog(Toplevel):
    def __init__(self, parent, available_langs, initial_selected=None):
        super().__init__(parent)
        self.title("Select Languages")
        self.geometry("300x400")
        self.resizable(False, False)
        try:
            self.iconbitmap(os.path.join(BASE_DIR, "mega_ocr.ico"))
        except Exception:
            pass
        self.selected = set(initial_selected or [])
        self.vars = {}
        frame = Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        canvas = tk.Canvas(frame, borderwidth=0, highlightthickness=0)
        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner = Frame(canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=(0, 0, e.width, max(e.height, 800))))
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        for lang in available_langs:
            var = BooleanVar(value=(lang in self.selected))
            cb = tb.Checkbutton(inner, text=lang, variable=var, bootstyle="round-toggle")
            cb.pack(anchor="w", pady=2)
            self.vars[lang] = var
        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        btn_frame = Frame(self)
        btn_frame.pack(pady=10, fill="x")
        inner_btn_frame = Frame(btn_frame)
        inner_btn_frame.pack(expand=True)
        tb.Button(inner_btn_frame, text="OK", command=self._ok, bootstyle="primary").pack(side="left", padx=5)
        tb.Button(inner_btn_frame, text="Cancel", command=self.destroy, bootstyle="primary").pack(side="left", padx=5)
        self.result = None
        self.transient(parent)
        self.grab_set()
    def _ok(self):
        self.selected = [k for k, v in self.vars.items() if v.get()]
        self.result = '+'.join(self.selected) if self.selected else ''
        self.destroy()
class ProgressDialog(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Processing OCR")
        self.geometry("400x100")
        self.resizable(False, False)
        try:
            self.iconbitmap(os.path.join(BASE_DIR, "mega_ocr.ico"))
        except Exception:
            pass
        blue_color = "#2534FF"
        red_color = "#FF0000"
        ttk.Label(self, text="Processing OCR, please wait...", foreground=red_color).pack(pady=10)
        self.progress = tb.Progressbar(self, mode="indeterminate", bootstyle="custom", length=350)
        self.progress.pack(pady=10)
        self.progress.start()
        style = ttk.Style()
        style.configure("custom.Horizontal.TProgressbar", troughcolor="white", background=blue_color)
        self.transient(parent)
        self.grab_set()
class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MegaOCR")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap(os.path.join(BASE_DIR, "mega_ocr.ico"))
        except Exception:
            pass
        self.file_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.output_format = tk.StringVar(value="txt")
        self.lang_combined = tk.StringVar(value="eng")
        self.available_languages = []
        self.create_widgets()
        self.load_languages()
    def create_widgets(self):
        blue_color = "#2534FF"
        red_color = "#FF0000"
        style = ttk.Style()
        style.configure("primary.TButton", foreground="white", background=blue_color)
        style.configure("success.TButton", foreground="white", background=blue_color)
        style.configure("TEntry", fieldbackground="white", bordercolor=blue_color, lightcolor=blue_color, darkcolor=blue_color)
        style.configure("TCombobox", fieldbackground="white", bordercolor=blue_color, foreground="black")
        style.map("TCombobox", 
                  fieldbackground=[("readonly", "!background")], 
                  selectbackground=[("readonly", "!background")], 
                  selectforeground=[("readonly", "black")])
        title = ttk.Label(self.root, text="MegaOCR - Advanced OCR Tool", font=("Arial", 16, "bold"), foreground=red_color)
        title.pack(pady=10)
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=5, padx=20, fill="x")
        ttk.Label(file_frame, text="Input File:", width=15, anchor="w").pack(side="left")
        ttk.Entry(file_frame, textvariable=self.file_path, width=40).pack(side="left", padx=5)
        tb.Button(file_frame, text="Select File", command=self.select_file, bootstyle="primary", width=15).pack(side="left")
        output_frame = ttk.Frame(self.root)
        output_frame.pack(pady=5, padx=20, fill="x")
        ttk.Label(output_frame, text="Output Directory:", width=15, anchor="w").pack(side="left")
        ttk.Entry(output_frame, textvariable=self.output_dir, width=40).pack(side="left", padx=5)
        tb.Button(output_frame, text="Select Directory", command=self.select_output, bootstyle="primary", width=15).pack(side="left")
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(pady=5, padx=20, fill="x")
        ttk.Label(lang_frame, text="Languages:", width=15, anchor="w").pack(side="left")
        ttk.Entry(lang_frame, textvariable=self.lang_combined, width=40, state="readonly").pack(side="left", padx=5)
        tb.Button(lang_frame, text="Select Languages", command=self.open_language_dialog, bootstyle="primary", width=15).pack(side="left")
        format_frame = ttk.Frame(self.root)
        format_frame.pack(pady=5, padx=25, fill="x")
        ttk.Label(format_frame, text="Output Format:", width=15, anchor="w").pack(side="left")
        ttk.Combobox(format_frame, textvariable=self.output_format, values=["txt", "docx", "pdf"], state="readonly", width=58).pack(side="left")
        tb.Button(self.root, text="Start OCR", command=self.start_ocr, bootstyle="primary", width=50).pack(pady=20)
    def load_languages(self):
        if not os.path.exists(TESSDATA_DIR):
            show_error(self.root, "Error", "tessdata folder not found.")
            return
        self.available_languages = [f.replace('.traineddata', '') for f in os.listdir(TESSDATA_DIR) if f.endswith('.traineddata')]
        self.available_languages.sort()
    def open_language_dialog(self):
        initial = self.lang_combined.get().split('+') if self.lang_combined.get() else []
        dlg = LanguageDialog(self.root, self.available_languages, initial_selected=initial)
        self.root.wait_window(dlg)
        if dlg.result is not None:
            self.lang_combined.set(dlg.result)
    def select_file(self):
        filetypes = [("PDF or Image", "*.pdf *.png *.jpg *.jpeg *.tif")]
        path = filedialog.askopenfilename(title="Select File", filetypes=filetypes)
        if path:
            self.file_path.set(path)
    def select_output(self):
        folder = filedialog.askdirectory(title="Select Output Directory")
        if folder:
            self.output_dir.set(folder)
    def start_ocr(self):
        file_path = self.file_path.get()
        out_dir = self.output_dir.get()
        out_format = self.output_format.get()
        languages = self.lang_combined.get().split('+') if self.lang_combined.get() else []
        if not file_path or not out_dir:
            show_warning(self.root, "Warning", "Please select input file and output directory.")
            return
        if not languages:
            show_warning(self.root, "Warning", "Please select at least one language.")
            return
        filename = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(out_dir, f"{filename}_ocr.{out_format}")
        pd = ProgressDialog(self.root)
        def worker():
            try:
                run_ocr_pipeline(file_path, output_path, out_format, languages)
                self.root.after(0, lambda: show_info(self.root, "Success", f"OCR saved successfully:\n{output_path}"))
            except Exception as e:
                self.root.after(0, lambda: show_error(self.root, "Error", f"An error occurred:\n{str(e)}"))
            finally:
                self.root.after(0, pd.destroy)
        threading.Thread(target=worker, daemon=True).start()
if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = OCRApp(root)
    root.mainloop()