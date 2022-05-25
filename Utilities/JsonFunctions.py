import json


def load_json_file(path_file):
    with open(path_file) as file:
        json_file = json.load(file)
        file.close()
        return json_file


def store_json_file(dict_to_write, path_file):
    with open(path_file, 'w') as file:
        json.dump(dict_to_write, file)
        file.close()
