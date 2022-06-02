from JsonFunctions import load_json_file, store_json_file

class ErrorManagement:

    def __init__(self):
        self.dict_error = {}


    def add_error(self, perimeter_error, error):
        self.dict_error[perimeter_error] = error

    def store_dict_errors_to_json(self,path_file):
        store_json_file(self.dict_error, path_file)