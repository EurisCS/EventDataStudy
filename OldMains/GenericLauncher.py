from abc import ABC
from time import time
from JsonFunctions import store_json_file
from OsFunctions import get_extension_into_path


class LaunchProgramManager(ABC):

    def __init__(self, function_to_run, path_outfile=None):
        self.function_to_run = function_to_run
        self.out_path_file = path_outfile

    # need to override
    @staticmethod
    def console_parse_args():
        return {}

    # need to override
    @staticmethod
    def management_command_errors(dict_args):
        return dict_args

    def _run_function(self, dict_args):
        t_start = time()  # replace to wrapper
        try:
            output_function = self.function_to_run(**dict_args)
        except Exception as err:
            output_function = (err, Exception)

        return output_function, time() - t_start,

    # create out_file for the pipeline
    def create_out_file(self, dict_args, output_of_function_ran, time_run, *args):

        dict_info = {'input_args': dict_args,
                     'output_function': output_of_function_ran,
                     'running_time_in_s': float(round(time_run, 2)),
                     'other_information': args}

        store_json_file(dict_info, self.out_path_file)

    def run(self):

        # get args from commands or setup file
        dict_args = self.management_command_errors(self.console_parse_args())

        # run
        output_function_ran, time_execution = self._run_function(dict_args)

        # create out file if path not set to None
        ext_file = get_extension_into_path(self.out_path_file)

        if ext_file == '':  # case where outfile is not defined but not set to none
            self.out_path_file = f'{self.out_path_file}/default_file_{int(time())}.json'

        if ext_file in ['.json', '.xml', '.txt', '']:
            self.create_out_file(dict_args, str(output_function_ran), time_execution)
