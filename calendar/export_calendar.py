"""
export_calendar.py

Exports the master agricultural calendar to:

1. JSON
2. CSV
3. Excel
"""

import json
import csv
from openpyxl import Workbook


# =====================================================
# Convert Lists to String
# =====================================================

def clean_value(value):
    """
    Excel/CSV cannot store Python lists.
    Convert them to comma-separated strings.
    """

    if value is None:
        return ""

    if isinstance(value, list):
        return ", ".join(str(v) for v in value if str(v).strip())

    return value


# =====================================================
# JSON
# =====================================================

def export_json(records, output_file):

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            records,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"JSON Saved : {output_file}")


# =====================================================
# CSV
# =====================================================

def export_csv(records, output_file):

    if not records:
        return

    headers = list(records[0].keys())

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(headers)

        for row in records:

            writer.writerow(
                [
                    clean_value(row.get(col, ""))
                    for col in headers
                ]
            )

    print(f"CSV Saved  : {output_file}")


# =====================================================
# Excel
# =====================================================

def export_excel(records, output_file):

    wb = Workbook()

    ws = wb.active

    ws.title = "Agricultural Calendar"

    if not records:

        wb.save(output_file)

        return

    headers = list(records[0].keys())

    ws.append(headers)

    for row in records:

        ws.append(
            [
                clean_value(row.get(col, ""))
                for col in headers
            ]
        )

    wb.save(output_file)

    print(f"Excel Saved: {output_file}")


# =====================================================
# Export Everything
# =====================================================

def export_all(

    records,

    json_path,

    csv_path,

    excel_path

):

    export_json(

        records,

        json_path

    )

    export_csv(

        records,

        csv_path

    )

    export_excel(

        records,

        excel_path

    )

    print("\nAll calendar files exported successfully.")