from pathlib import Path
from datetime import datetime
from PIL import Image, ExifTags

EXIF_TAGS = {value: key for key, value in ExifTags.TAGS.items()}
GPS_TAGS = {value: key for key, value in ExifTags.GPSTAGS.items()}

def _safe_value(value):
    try:
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)
    except Exception:
        return str(value)

def analyze_metadata(image_path):
    path = Path(image_path)
    stat = path.stat()
    with Image.open(path) as image:
        result = {
            "filename": path.name,
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "file_size_bytes": stat.st_size,
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            "exif": {}
        }
        try:
            exif_data = image.getexif()
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                if tag_name == "GPSInfo" and hasattr(value, "items"):
                    gps_result = {}
                    for gps_id, gps_value in value.items():
                        gps_name = ExifTags.GPSTAGS.get(gps_id, str(gps_id))
                        gps_result[gps_name] = _safe_value(gps_value)
                    result["exif"]["GPSInfo"] = gps_result
                else:
                    result["exif"][tag_name] = _safe_value(value)
        except Exception:
            pass
    return result
