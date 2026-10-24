# ImageGuard test checklist

| Test | Steps | Expected result |
|---|---|---|
| Valid image | Select a valid JPG or PNG and analyze | Metadata and SHA-256 are displayed |
| Missing EXIF | Analyze an image without EXIF | App reports no readable EXIF metadata |
| Same hash | Enter the calculated 64-character hash as reference | MATCH |
| Different hash | Enter a valid hash from a different file | MISMATCH |
| Invalid reference | Enter fewer than 64 characters | Validation error |
| JPEG ELA | Generate ELA for a JPG/JPEG | ELA output file is saved |
| Non-JPEG ELA | Try ELA on PNG | Clear warning that ELA is JPEG-only |
| Report export | Export JSON and TXT | Report file contains metadata and hash |
| Invalid image | Select a non-image file | Error message; app remains open |

Record actual outcomes and screenshots after running the application on your system. Do not report tests as passed until you have performed them.
