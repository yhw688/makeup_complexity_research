
#this file is used to get all the names of the none makeup images
import os
import json
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--json_path",
        required=True,
        help="Path to mt_text_anno.json"
    )

    parser.add_argument(
        "--non_makeup_dir",
        required=True,
        help="Path to the non-makeup image folder"
    )

    parser.add_argument(
        "--out_json",
        default="mt_text_anno_with_nonmakeup.json",
        help="Output JSON path"
    )

    args = parser.parse_args()

    # Read existing makeup annotations
    with open(args.json_path, "r") as f:
        annotations = json.load(f)

    image_extensions = {".png", ".jpg", ".jpeg"}

    added = 0
    skipped = 0

    # Add every non-makeup image
    for filename in sorted(os.listdir(args.non_makeup_dir)):

        extension = os.path.splitext(filename)[1].lower()

        if extension not in image_extensions:
            continue

        # Do not overwrite existing annotation
        if filename in annotations:
            print(f"Skipped existing image: {filename}")
            skipped += 1
            continue

        annotations[filename] = {
            "eye": [],
            "lips": [],
            "face": []
        }

        added += 1

    # Save a new JSON
    with open(args.out_json, "w") as f:
        json.dump(annotations, f, indent=4)

    print(f"Added {added} non-makeup images.")
    print(f"Skipped {skipped} existing images.")
    print(f"Total images: {len(annotations)}")
    print(f"Saved to: {args.out_json}")


if __name__ == "__main__":
    main()
