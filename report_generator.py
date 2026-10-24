import json
from pathlib import Path
from datetime import datetime

def save_report(report_data, output_path):
    path = Path(output_path)
    if path.suffix.lower() == ".txt":
        lines = [
            "IMAGEGUARD - DIGITAL IMAGE FORENSIC REPORT",
            "=" * 48,
            f"Generated: {report_data.get('analysis_datetime', datetime.now().isoformat())}",
            f"File: {report_data.get('file_path', '')}",
            "",
            "METADATA",
            json.dumps(report_data.get("metadata", {}), indent=2, ensure_ascii=False),
            "",
            f"SHA-256: {report_data.get('sha256', '')}",
            f"Reference SHA-256: {report_data.get('reference_sha256') or 'Not provided'}",
            f"Integrity match: {report_data.get('integrity_match')}",
            f"ELA output: {report_data.get('ela_output') or 'Not generated'}",
            "",
            "NOTES",
            report_data.get("notes", ""),
            "",
            "DISCLAIMER",
            "This report records technical observations. Hash differences and ELA patterns do not independently prove malicious manipulation."
        ]
        path.write_text("\n".join(lines), encoding="utf-8")
    else:
        path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)
