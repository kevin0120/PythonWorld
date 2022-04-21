import json


def read_curve_templates_from_file(file_path: str):
    with open(file_path, 'r', encoding="utf8") as file:
        return json.loads(file.read())
