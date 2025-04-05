import json

# 1. USDA foundation food json datase input
with open("foundationDownload.json", "r") as f:
    raw_data = json.load(f)

# 2. format to analyze
with open("usda_pretty.json", "w") as f:
    json.dump(raw_data, f, indent=4)