import re
import pickle
import os


def store_object_as_pickle(object_to_store, save_path):
    save_path = add_extension(save_path, "pickle")
    with open(save_path, "wb") as output:
        try:
            pickle.dump(object_to_store, output)
        except Exception as err:
            print(f'impossible to save the object :\n{err}')
        output.close()


def open_pickle_object(path_file):
    path_file = add_extension(path_file, "pickle")
    try:
        input_file = open(path_file, "rb")
        return pickle.load(input_file)
    except Exception as err:
        print(f'impossible to open the object with the path : {path_file}\n===> None returned ==> {err}')
        return None


def add_extension(path_file, extension_without_the_dot):
    search = re.search(f"\.{extension_without_the_dot}", path_file)
    if search is None:
        path_file += f".{extension_without_the_dot}"
    return path_file


def check_extension(path_file, extension_without_the_dot):
    if re.search(f"\.{extension_without_the_dot}", path_file) is None:
        return False
    return True

def get_name_file_into_path(path):
    basename = os.path.basename(path)
    return os.path.splitext(basename)[0]


def get_extension_into_path(path):
    root, extension = os.path.splitext(path)
    return extension

def get_path_without_extension(path):
    root, extension = os.path.splitext(path)
    return root