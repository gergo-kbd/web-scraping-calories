import json

with open("foundationDownload.json", "r") as f:
    raw_data = json.load(f)

with open("usda_pretty.json", "w") as f:
    json.dump(raw_data, f, indent=4)