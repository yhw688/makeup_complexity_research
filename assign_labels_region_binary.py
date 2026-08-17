import json
import csv
import argparse
from collections import Counter


def compute_region_stats(regions: dict) -> dict:
    # Get descriptors for the three regions
    eye = regions.get("eye", []) or []
    lips = regions.get("lips", []) or []
    face = regions.get("face", []) or []

    # Count descriptors for each region
    return {
        "eye_count": len(eye),
        "lips_count": len(lips),
        "face_count": len(face),
    }


# Binary labels for makeup-only experiments:
# 1-3 descriptors -> simple
# 4+ descriptors -> complex
def assign_binary_label(count: int) -> str:
    if count <= 3:
        return "simple"
    else:
        return "complex"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json_path",
        required=True,
        help="Path to makeup-only mt_text_anno.json"
    )
    parser.add_argument(
        "--out_csv",
        default="complexity_labels_region_binary.csv",
        help="Output CSV path"
    )
    args = parser.parse_args()

    # Read JSON annotations
    with open(args.json_path, "r") as f:
        annotations = json.load(f)

    rows = []

    for filename, regions in annotations.items():
        data = compute_region_stats(regions)
        data["filename"] = filename

        data["eye_label"] = assign_binary_label(data["eye_count"])
        data["lips_label"] = assign_binary_label(data["lips_count"])
        data["face_label"] = assign_binary_label(data["face_count"])

        rows.append(data)

    # Write CSV
    fieldnames = [
        "filename",
        "eye_count",
        "lips_count",
        "face_count",
        "eye_label",
        "lips_label",
        "face_label",
    ]

    with open(args.out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow(row)

    print(f"Processed {len(rows)} images.")
    print(f"Saved to: {args.out_csv}")
    print()

    label_order = ["simple", "complex"]

    print("Eye label distribution:")
    eye_counts = Counter(row["eye_label"] for row in rows)
    for label in label_order:
        print(f"  {label}: {eye_counts.get(label, 0)}")

    print()

    print("Lips label distribution:")
    lips_counts = Counter(row["lips_label"] for row in rows)
    for label in label_order:
        print(f"  {label}: {lips_counts.get(label, 0)}")

    print()

    print("Face label distribution:")
    face_counts = Counter(row["face_label"] for row in rows)
    for label in label_order:
        print(f"  {label}: {face_counts.get(label, 0)}")


if __name__ == "__main__":
    main()
