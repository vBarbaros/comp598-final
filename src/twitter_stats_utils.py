import os
import json

from pathlib import Path
parentdir = Path(__file__).parents[1]

def read_from_json(input_csv_file):
    in_file = os.path.join(parentdir, input_csv_file)
    json_content = None
    with open(in_file, 'r') as fh:
        json_content = json.load(fh)
    return json_content