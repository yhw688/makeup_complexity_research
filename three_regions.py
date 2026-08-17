
#this file is used to read JSON file
import json
import csv
import argparse

def compute_region_stats(regions: dict)-> dict:
    #get descriptors for the three regions
    eye = regions.get("eye", []) or []
    lips = regions.get("lips", []) or []
    face = regions.get("face", []) or []

    #count descriptors for each region
    return {
        "eye_count": len(eye),
        "lips_count": len(lips),
        "face_count": len(face),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_path", required = True, help = "Path to mt_text_anno.json")
    parser.add_argument("--out_csv", default = "region_scores.csv", help = "Output CSV path")
    args = parser.parse_args()

    #read the json annotation file
    with open(args.json_path, "r") as f:
        annotations = json.load(f)


    #get scores for every image
    rows = []
    for filename, regions in annotations.items():
        data = compute_region_stats(regions)
        data["filename"] = filename
        rows.append(data)


    #write output
    fieldnames = ["filename", "eye_count", "lips_count", "face_count"]

    with open(args.out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
 
    print(f"Processed {len(rows)} images.")
    print(f"Saved scores to: {args.out_csv}")

 
if __name__ == "__main__":
    main()
    
