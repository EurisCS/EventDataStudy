import sys

sys.path.append('/home/eguimard/PycharmProjects/DataStudy/')
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/Utilities')
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/DataAcquisition')

import argparse
from time import time
from Utilities.JsonFunctions import load_json_file, store_json_file
from DataAcquisition.PipelineDataAcquisition import pipeline_data_acquisition


class DataAcquisition:

    def __init__(self):
        self.pipeline_to_run = pipeline_data_acquisition
        self.out_path_file = None

    def run(self, dict_args=None):

        # get args from commands or setup file
        if dict_args is None:
            dict_args = self.management_command_errors(self.console_parse_args())

        # run
        T_start = time()
        output_of_the_pipeline = self.pipeline_to_run(**dict_args)
        time_exec = time() - T_start

        # outfile
        if self.out_path_file is not None:
            self.create_and_store_out_file(dict_args, output_of_the_pipeline, time_exec)

    @staticmethod
    def console_parse_args():
        parser = argparse.ArgumentParser(description='pipeline for store data')

        parser.add_argument('-sf', '--setup_file', help='setup file for launch', default=None, required=False)

        parser.add_argument('-pjson', '--path_json_query', help="path of the json query", required=False)
        parser.add_argument('-opd', '--out_path_data', help="define the out_path of data_store", required=False)
        parser.add_argument('-ext', '--extension_store', help='extension for storing the datas', required=False)

        parser.add_argument('-host', '--host', help="host of the elastic cluster", required=False)
        parser.add_argument('-port', '--port', help="port of the elastic cluster", required=False)
        parser.add_argument('-index', '--index_cluster', help="index in the elastic cluster ", required=False)
        parser.add_argument('-uq', '--update_query', help='setup file for launch', default=None, required=False)

        parser.add_argument('-lf', '--list_features_to_extract', default=None, required=False,
                            help='list of wanted feature to get' )

        parser.add_argument('-opf', '--out_path_file',
                            help="define a path to create an outfile of the run",required=False)

        return vars(parser.parse_args())

    def management_command_errors(self, dict_args):

        print(f'dict args : {dict_args}')

        # out_path_file
        if dict_args['out_path_file'] is not None:
            self.out_path_file = dict_args['out_path_file']
        del dict_args['out_path_file']

        # setup_file
        if dict_args['setup_file'] is not None:
            dict_param = load_json_file(dict_args['setup_file'])

            # ecrase the previous out_path_file
            if 'out_path_file' in dict_param:
                self.out_path_file = dict_param['out_path_file']
                del dict_param['out_path_file']

            return dict_param

        # command parse case
        del dict_args['setup_file']
        missing_arg = False
        for key in dict_args.keys():
            if dict_args[key] is None:
                missing_arg = True
                print(f"error -> arg '{key}' is not specified ")

        if missing_arg:
            sys.exit()

        return dict_args

    # create out_file for the pipeline
    def create_and_store_out_file(self, dict_args, output_of_pipeline_ran, time_run, *args):

        dict_info = {'input_args': dict_args,
                     'output_function': str(output_of_pipeline_ran),
                     'running_time_in_s': float(round(time_run, 2)),
                     'more_information': args}

        store_json_file(dict_info, self.out_path_file)


if __name__ == '__main__':
    DataAcquisition().run()
