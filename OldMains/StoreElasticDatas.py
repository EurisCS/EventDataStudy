# better way ?
import sys
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/')
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/DataAcquisition')
sys.path.append('/home/eguimard/PycharmProjects/DataStudy/Utilities')

from GenericLauncher import LaunchProgramManager
from Mains.MainDataAcquisition import ElasticAPI
import argparse
from Utilities.JsonFunctions import load_json_file
from Utilities.OsFunctions import get_name_file_into_path


class LauncherPipelineStoreDatas(LaunchProgramManager):

    def __init__(self):
        super().__init__(self.pipeline_store_datas)

    # OVERRIDED FUNCTIONS ############################################################################################

    #
    @staticmethod
    def console_parse_args():
        parser = argparse.ArgumentParser(description='pipeline for store data')

        parser.add_argument('-sf', '--setup_file', default=None, required=False, help='setup file for launch')
        parser.add_argument('-opd', '--out_path_data', help="define the out_path of data_store", required=False)
        parser.add_argument('-opf', '--out_path_file', help="define the out_path of out run file", required=False)
        parser.add_argument('-host', '--host', help="host of the elastic cluster", required=False)
        parser.add_argument('-port', '--port', help="port of the elastic cluster", required=False)
        parser.add_argument('-jsonp', '--path_json_query', help="path of the json query", required=False)
        parser.add_argument('-index', '--index_cluster', help="index in the elastic cluster ", required=False)
        parser.add_argument('-ext', '--extension_store', help='extension for storing the datas', required=False)
        return vars(parser.parse_args())

    #
    def management_command_errors(self, dict_args):

        # create out_file or not
        if dict_args['out_path_file'] is not None:
            self.out_path_file = dict_args['out_path_file']
        del dict_args['out_path_file']

        # setup file case
        if dict_args['setup_file'] is not None:
            dict_param = load_json_file(dict_args['setup_file'])
            if 'out_path_file' in dict_param:
                self.out_path_file = dict_param['out_path_file']
                del dict_param['out_path_file']
            return dict_param

        # command parse case
        del dict_args['setup_file']
        is_command_good = True
        for key in dict_args.keys():
            if dict_args[key] is None:
                print(f'error :-> {key} is not specified ')
                is_command_good = False

        if is_command_good:
            return dict_args
        # else
        sys.exit()

    # IMPLEMENTED PIPELINE #####################################################################################

    #
    def pipeline_store_datas(self, host, port, index_cluster, path_json_query, out_path_data, extension_store):

        # connect to elastic client
        elastic_client = ElasticAPI(host, port)

        # get data from setups
        elastic_df = elastic_client.create_elastic_dataframe_from_json_query(index_cluster, path_json_query)

        # create paths
        out_path_file_data = self.create_save_path(index_cluster, path_json_query, elastic_df.df.shape[0],
                                                   out_path_data)
        # store dataframe
        elastic_df.store_df(f'{out_path_file_data}', extension= extension_store)

    def create_save_path(self, index_cluster, path_json_query, nb_row, out_path_data):

        # create path save data
        filename = f'{index_cluster}_{get_name_file_into_path(path_json_query)}_{nb_row}_row'
        out_path_data = f'{out_path_data}/{filename}'

        #  create path outfile
        if self.out_path_file is not None:
            self.out_path_file = f'{self.out_path_file}/{filename}.json'

        return out_path_data

    ###############################################################################################################


if __name__ == '__main__':
    LauncherPipelineStoreDatas().run()
