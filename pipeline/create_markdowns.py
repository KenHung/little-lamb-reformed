import json
from datetime import datetime
from pathlib import Path

import pytz

# Define the input and output directories
input_dir = Path("posts")
output_dir = Path("../content/zh_TW/post")

# Loop through all the JSON files in the input directory
for filepath in input_dir.glob("*.json"):
    # Load the JSON data from the file
    with open(filepath, "r") as f:
        data = json.load(f)

    # Format the metadata as a Hugo front matter string
    title = data["title"].replace('"', '\\"')
    date = datetime.fromtimestamp(
        int(data["public_at"]), pytz.timezone("Asia/Taipei")
    ).strftime("%Y-%m-%d")
    lastmod = datetime.fromtimestamp(
        int(data["last_modified"]), pytz.timezone("Asia/Taipei")
    ).strftime("%Y-%m-%d")
    front_matter = (
        f"+++\n"
        f'title = "{title}"\n'
        f"date = {date}\n"
        f"lastmod = {lastmod}\n"
        f'categories = ["{data["category"]}"]\n'
        f"isCJKLanguage = true\n"
        f"+++\n\n"
    )

    # Combine the front matter, 'rawhtml' shortcode, and content into a single string
    markdown = (
        front_matter + "{{< rawhtml >}}\n" + data["body"] + "\n{{< /rawhtml >}}\n"
    )

    # Write the markdown to a file in the output directory
    output_filename = data["id"] + ".md"
    output_filepath = output_dir / output_filename
    with open(output_filepath, "w") as f:
        f.write(markdown)
