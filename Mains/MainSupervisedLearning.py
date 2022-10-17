import sys
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/')
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/Utilities')
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/SupervisedLearning')

import argparse
from time import time
from Utilities.JsonFunctions import load_json_file, store_json_file
from PipelineSupervisedLearning import PipelineSupervisedLearning


class MainSupervisedLearning:

    def __init__(self):
        self.pipeline_to_run = PipelineSupervisedLearning
        self.out_path_file = None

    def run(self, dict_args=None):

        # get args from commands or setup file
        if dict_args is None:
            dict_args = self.management_command_errors(self.console_parse_args())

        # run
        T_start = time()
        output_of_the_pipeline = \
            self.pipeline_to_run(**dict_args).pipeline_repeated_cross_validate_multiple_models()
        time_exec = time() - T_start

        # outfile
        if self.out_path_file is not None:
            self.create_and_store_out_file(dict_args, output_of_the_pipeline, time_exec)

        try:
            print(f"\ndata stored at the path : {dict_args['save_path_root']}")
        except KeyError:
            pass

    @staticmethod
    def console_parse_args():
        parser = argparse.ArgumentParser(description='pipeline for store data')

        parser.add_argument('-sf', '--setup_file', default=None, required=False, help='setup file for launch')

        parser.add_argument('-ipdir', '--in_path_directory',
                            help='inpath directory where the input data are stocked',required=False)

        parser.add_argument('-sp', '--save_path_data',
                            help='save path for the dataframe and figure', required=False)

        parser.add_argument('-extd', '--extension_data',
                            help="define the extension of the new data created", required=False)

        parser.add_argument('-extf', '--extension_figure',
                            help="define the extension of the figure created", required=False)

        parser.add_argument('-opf', '--out_path_file',
                            help="define a path to create an ouftile of the run", required=False)

        return vars(parser.parse_args())

    # TO REDESIGN
    def management_command_errors(self, dict_args):

        # out_path_file
        if dict_args['out_path_file'] is not None:
            self.out_path_file = dict_args['out_path_file']
        del dict_args['out_path_file']

        # setup_file
        if dict_args['setup_file'] is not None:
            dict_param = load_json_file(dict_args['setup_file'])

            # overwrite the previous out_path_file
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
    MainSupervisedLearning().run()