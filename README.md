# ImageGuard
**Digital Image Forensic Analysis and Integrity Verification Tool**

It extracts available image metadata, calculates SHA-256 hashes, compares a file hash with a trusted reference, generates an ELA visualization for JPEG files, and exports a forensic report.

## Features
- Image selection and preview through a Tkinter desktop interface
- Metadata and available EXIF extraction
- SHA-256 calculation and reference hash comparison
- Error Level Analysis (ELA) visualization for JPEG images
- JSON and TXT report export

## Requirements
- Python 3.10 or later
- Pillow

Tkinter is included with many standard Python installations. On some Linux distributions, install the system package `python3-tk` if Tkinter is missing.

## Run on macOS
Open Terminal in the `ImageGuard` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If you use a different Python installation, use the corresponding `python` command.

## How to use
1. Click **Choose Image** and select a JPG, PNG, BMP, TIFF, or other supported Pillow image.
2. Click **Analyze Image** to view metadata and the SHA-256 digest.
3. Optionally paste a trusted 64-character SHA-256 digest into the reference field and click **Compare Reference Hash**.
4. For JPEG images, click **Generate ELA** and choose where to save the visualization.
5. Add observations in the notes area and click **Export Report** to save JSON or TXT.

## Important forensic limitations
- A SHA-256 match indicates byte-for-byte identical file contents for the compared files. A mismatch only means the files differ; it does not establish why.
- EXIF metadata can be absent, stripped, or modified. Missing metadata is not proof of manipulation.
- ELA visualizes differences after JPEG recompression. It is not a reliable standalone image forgery detector; image content, compression history, and processing can affect the result.
- This is a learning and triage tool, not a certified forensic suite. Preserve original evidence and document how it was acquired before examination.

## Suggested testing
- Analyze a JPEG with EXIF metadata and one without it.
- Calculate a hash, then compare it with the same hash (expected MATCH).
- Edit or re-save a copy of an image, calculate its hash, and compare against the original hash (expected MISMATCH).
- Generate ELA for a JPEG and verify that a PNG input is rejected for ELA.
- Export both JSON and TXT reports.
