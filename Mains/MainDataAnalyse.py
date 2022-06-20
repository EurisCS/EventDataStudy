import sys
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/')
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/Utilities')
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/DataAnalyse')

import argparse
from time import time
from Utilities.JsonFunctions import load_json_file, store_json_file
from PipelineDataAnalyse import PipelineDataAnalyse


class DataAnalye:

    def __init__(self):
        self.pipeline_to_run = PipelineDataAnalyse
        self.out_path_file = None

    def run(self, dict_args=None):

        # get args from commands or setup file
        if dict_args is None:
            dict_args = self.management_command_errors(self.console_parse_args())

        # take out this for the instantiation
        in_path_data_directory = dict_args.pop('in_path_data_directory')
        save_path = dict_args.pop('save_path')

        # run
        T_start = time()
        output_of_the_pipeline = \
            self.pipeline_to_run(**dict_args).pipeline_multiple_df(in_path_data_directory, save_path)
        time_exec = time() - T_start

        # outfile
        if self.out_path_file is not None:
            self.create_and_store_out_file(dict_args, output_of_the_pipeline, time_exec)

        print(f"\ndata stored at the path : {save_path}")

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

        parser.add_argument('-rdim_alg', '--reduction_dimension_algorithm',
                            help="chose the algorithm for the reduction dimension", required=False)
        parser.add_argument('-sf_rdim', '--setup_file_reduction_dimension',
                            help="setupe file for the dict param of the reduction dimension", required=False)

        parser.add_argument('-sm', '--scatter_matrix',
                            help="if you want to create a scatter_matrix (bool)", required=False)
        parser.add_argument('-hm','--heatmap',
                            help="if you want to create a heatmap correlation (bool)", required=False)
        parser.add_argument('-s2d', '--scatter_2D',
                            help="if you want to create a scatter_2D (bool)", required=False)
        parser.add_argument('-s3d', '--scatter_3D',
                            help="if you want to create a scatter_3D (bool)", required=False)

        parser.add_argument('-ba', '--blocked_axis',
                            help="if you want to block an axis for the visualisation", required=False)

        parser.add_argument('-opf', '--out_path_file',
                            help="define a path to create an ouftile of the run", required=False)

        return vars(parser.parse_args())

    # TO REFONTE
    def management_command_errors(self, dict_args):

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
    DataAnalye().run()