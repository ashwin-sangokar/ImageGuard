import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from PIL import Image, ImageTk
import hashlib
import json
from datetime import datetime

from metadata_analyzer import analyze_metadata
from integrity_checker import calculate_sha256, compare_hashes
from ela_analyzer import generate_ela
from report_generator import save_report

APP_TITLE = "ImageGuard - Digital Image Forensic Analysis"

class ImageGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1050x760")
        self.root.minsize(900, 650)
        self.image_path = None
        self.metadata = None
        self.sha256 = None
        self.ela_path = None
        self.reference_hash = tk.StringVar()
        self.status = tk.StringVar(value="Select an image to begin analysis.")

        self._build_ui()

    def _build_ui(self):
        header = ttk.Frame(self.root, padding=(16, 12))
        header.pack(fill="x")
        ttk.Label(header, text="ImageGuard", font=("Arial", 22, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="Digital Image Forensic Analysis and Integrity Verification",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(2, 0))

        actions = ttk.Frame(self.root, padding=(16, 4))
        actions.pack(fill="x")
        ttk.Button(actions, text="Choose Image", command=self.choose_image).pack(side="left")
        ttk.Button(actions, text="Analyze Image", command=self.analyze_image).pack(side="left", padx=8)
        ttk.Button(actions, text="Generate ELA", command=self.run_ela).pack(side="left")
        ttk.Button(actions, text="Export Report", command=self.export_report).pack(side="left", padx=8)

        body = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        body.pack(fill="both", expand=True, padx=16, pady=8)

        left = ttk.Frame(body, padding=8)
        right = ttk.Frame(body, padding=8)
        body.add(left, weight=1)
        body.add(right, weight=2)

        ttk.Label(left, text="Image Preview", font=("Arial", 12, "bold")).pack(anchor="w")
        self.preview_label = ttk.Label(left, text="No image selected", anchor="center")
        self.preview_label.pack(fill="both", expand=True, pady=8)

        ttk.Label(left, text="Reference SHA-256 (optional)", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Entry(left, textvariable=self.reference_hash).pack(fill="x", pady=(4, 4))
        ttk.Button(left, text="Compare Reference Hash", command=self.compare_reference).pack(anchor="w")
        self.integrity_label = ttk.Label(left, text="Integrity status: not checked", wraplength=300)
        self.integrity_label.pack(anchor="w", pady=8)

        ttk.Label(right, text="Analysis Results", font=("Arial", 12, "bold")).pack(anchor="w")
        self.results = tk.Text(right, height=20, wrap="word", font=("Courier New", 10))
        self.results.pack(fill="both", expand=True, pady=(6, 8))
        self.results.insert("1.0", "Choose an image, then click Analyze Image.\n")
        self.results.configure(state="disabled")

        ttk.Label(right, text="Forensic Notes", font=("Arial", 10, "bold")).pack(anchor="w")
        self.notes = tk.Text(right, height=5, wrap="word")
        self.notes.pack(fill="x", pady=(4, 8))
        self.notes.insert("1.0", "Observations: ")

        footer = ttk.Label(self.root, textvariable=self.status, relief="sunken", anchor="w", padding=6)
        footer.pack(fill="x", side="bottom")

    def choose_image(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with Image.open(path) as img:
                img.verify()
            self.image_path = path
            self.metadata = None
            self.sha256 = None
            self.ela_path = None
            self._show_preview(path)
            self.status.set(f"Selected: {Path(path).name}")
            self._set_results("Image selected. Click Analyze Image to extract metadata and calculate SHA-256.")
            self.integrity_label.configure(text="Integrity status: not checked")
        except Exception as exc:
            messagebox.showerror("Invalid image", f"Could not open this image file.\n\n{exc}")

    def _show_preview(self, path):
        try:
            with Image.open(path) as img:
                img = img.convert("RGB")
                img.thumbnail((360, 420))
                self.preview_photo = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=self.preview_photo, text="")
        except Exception as exc:
            self.preview_label.configure(image="", text=f"Preview unavailable: {exc}")

    def _set_results(self, text):
        self.results.configure(state="normal")
        self.results.delete("1.0", tk.END)
        self.results.insert("1.0", text)
        self.results.configure(state="disabled")

    def analyze_image(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Please choose an image first.")
            return
        try:
            self.metadata = analyze_metadata(self.image_path)
            self.sha256 = calculate_sha256(self.image_path)
            report = {
                "application": "ImageGuard",
                "analysis_datetime": datetime.now().isoformat(timespec="seconds"),
                "file_path": self.image_path,
                "metadata": self.metadata,
                "sha256": self.sha256,
                "ela_output": self.ela_path,
                "notes": self.notes.get("1.0", tk.END).strip()
            }
            self.current_report = report
            lines = [
                "IMAGE METADATA",
                "=" * 55,
                f"Filename       : {self.metadata.get('filename')}",
                f"Format         : {self.metadata.get('format')}",
                f"Dimensions     : {self.metadata.get('width')} x {self.metadata.get('height')}",
                f"Mode           : {self.metadata.get('mode')}",
                f"File size      : {self.metadata.get('file_size_bytes')} bytes",
                f"Modified time  : {self.metadata.get('modified_time')}",
                "",
                "EXIF METADATA",
                "=" * 55,
            ]
            exif = self.metadata.get("exif", {})
            if exif:
                lines.extend([f"{key}: {value}" for key, value in exif.items()])
            else:
                lines.append("No readable EXIF metadata found.")
            lines += [
                "",
                "INTEGRITY",
                "=" * 55,
                f"SHA-256: {self.sha256}",
                "",
                "FORENSIC INTERPRETATION",
                "=" * 55,
                "Metadata may be missing or altered. A hash identifies the exact file contents;",
                "it does not by itself prove whether an image is authentic or manipulated.",
                "Use ELA output only as an indicator for further review, not as proof of forgery."
            ]
            self._set_results("\n".join(lines))
            self.status.set("Analysis completed.")
            self.compare_reference(silent=True)
        except Exception as exc:
            messagebox.showerror("Analysis error", str(exc))

    def compare_reference(self, silent=False):
        if not self.sha256:
            if not silent:
                messagebox.showwarning("Analyze first", "Click Analyze Image before comparing hashes.")
            return
        reference = self.reference_hash.get().strip().lower()
        if not reference:
            self.integrity_label.configure(text="Integrity status: no reference hash supplied")
            return
        result = compare_hashes(self.sha256, reference)
        if result:
            self.integrity_label.configure(text="Integrity status: MATCH — file hash equals reference")
        else:
            self.integrity_label.configure(text="Integrity status: MISMATCH — file hash differs from reference")
        if hasattr(self, "current_report"):
            self.current_report["reference_sha256"] = reference
            self.current_report["integrity_match"] = result

    def run_ela(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Please choose an image first.")
            return
        try:
            output = filedialog.asksaveasfilename(
                title="Save ELA output",
                defaultextension=".jpg",
                initialfile=f"{Path(self.image_path).stem}_ela.jpg",
                filetypes=[("JPEG image", "*.jpg")]
            )
            if not output:
                return
            result_path = generate_ela(self.image_path, output)
            self.ela_path = result_path
            messagebox.showinfo("ELA completed", f"ELA image saved to:\n{result_path}\n\nELA highlights compression differences and is not conclusive proof of manipulation.")
            self.status.set("ELA analysis image generated.")
            if hasattr(self, "current_report"):
                self.current_report["ela_output"] = result_path
        except ValueError as exc:
            messagebox.showwarning("ELA unavailable", str(exc))
        except Exception as exc:
            messagebox.showerror("ELA error", str(exc))

    def export_report(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Choose and analyze an image first.")
            return
        if not self.metadata or not self.sha256:
            self.analyze_image()
            if not self.metadata or not self.sha256:
                return
        self.current_report["analysis_datetime"] = datetime.now().isoformat(timespec="seconds")
        self.current_report["notes"] = self.notes.get("1.0", tk.END).strip()
        self.current_report["reference_sha256"] = self.reference_hash.get().strip() or None
        if self.reference_hash.get().strip():
            self.current_report["integrity_match"] = compare_hashes(self.sha256, self.reference_hash.get().strip())
        else:
            self.current_report["integrity_match"] = None

        path = filedialog.asksaveasfilename(
            title="Export forensic report",
            defaultextension=".json",
            initialfile=f"{Path(self.image_path).stem}_forensic_report.json",
            filetypes=[("JSON report", "*.json"), ("Text report", "*.txt")]
        )
        if not path:
            return
        try:
            save_report(self.current_report, path)
            self.status.set(f"Report saved: {Path(path).name}")
            messagebox.showinfo("Report saved", f"Forensic report saved successfully:\n{path}")
        except Exception as exc:
            messagebox.showerror("Report error", str(exc))


def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass
    ImageGuardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
