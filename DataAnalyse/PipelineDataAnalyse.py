from Preprocessing import Preprocessing
from CleanData import CleanData
from DataVisualisation import VisualiseDataPlotly
from ReductionDImension import ReductionDimensionUmap
from DataManagement.PandasFrameManagement import ManageDataFrames

from Utilities.FileManipulation import create_folder


# from StatisticAnalyse import CorellationTest


# TO DO :
#
# create folder
# Test Corelation
# Heatmap


class PipelineDataVisualisation:

    def __init__(self, extension_data='pickle', extension_fig='html',
                 algorithm_reduction='umap', dp_reduction_dimension=None,
                 scatter_matrix=True, heatmap=False, scatter_3D=False, scatter_2D=False):

        # load objects for treatment
        self.cleaner = CleanData()
        self.preprocessor = Preprocessing()
        self.visualiser = VisualiseDataPlotly()
        self.data_manager = ManageDataFrames()

        if scatter_3D or scatter_2D:
            self.reducer = ReductionDimensionUmap(algorithm_reduction, dp_reduction_dimension)  # V

        # extension save
        self.extension_data = extension_data
        self.extension_fig = extension_fig

        # chose program
        self.scatter_matrix = scatter_matrix
        self.heatmap = heatmap
        self.scatter_3D = scatter_3D
        self.scatter_2D = scatter_2D

    # PIPELINES ################################################################################################

    def pipeline_multiple_df(self, in_path_data_directory, save_path_data):

        dict_df_input = ManageDataFrames().load_dict_df(in_path_data_directory)  # load dfs

        # multiprocessing to setup
        for name_df in dict_df_input.keys():
            current_save_path_data = f'{save_path_data}/{name_df}'

            create_folder(current_save_path_data)

            self.pipeline_one_df(dict_df_input[name_df], current_save_path_data)

    def pipeline_one_df(self, input_data, save_path_data):

        preprocessed_data = self.clean_preprocess_and_store_data(input_data, save_path_data)

        if self.scatter_matrix:
            self.make_scatter_matrix(preprocessed_data, save_path_data)

        if self.heatmap:
            # self.make_heatmap(preprocessed_data, save_path_data)
            pass

        if self.scatter_3D:
            self.make_scatter_3D(preprocessed_data, save_path_data)

        if self.scatter_2D:
            self.make_scatter_2D(preprocessed_data, save_path_data)

    # DATA TREATMENT ################################################################################################

    def clean_preprocess_and_store_data(self, input_data, save_path_data):

        # clean
        cleaned_data = self.cleaner.drop_bad_row_and_columns(input_data, threshold_na_column=0.5, threshold_na_row=0.2)

        # preprocess
        preprocessed_data = self.preprocessor.preprocessing_data_unlabelled(cleaned_data)

        # store
        self.data_manager.store_df(preprocessed_data, f'{save_path_data}/preprocessed_data', self.extension_data)

        return preprocessed_data

    # STATISTIC ANALYSE AND FIGURE ###################################################################################

    def make_scatter_matrix(self, preprocessed_data, save_path_data):

        self.visualiser.create_scatter_matrix(preprocessed_data,
                                              save_path=f'{save_path_data}/scatter_matrix.{self.extension_fig}')  # V

    '''
    def heatmap(self, preprocessed_data, save_path_data):
        
        correlated_data = CorellationTest.run(preprocessed_data)  # X
        
        self.data_manager.store_df(correlated_data, f'{save_path_data}/correlated_data', self.extension_data)
        
        self.visualiser.heatmap(correlated_data)  # X
    '''

    def make_scatter_3D(self, preprocessed_data, save_path_data):

        reduced_3D_data = self.reducer.run(preprocessed_data, output_dimension=3)
        self.data_manager.store_df(reduced_3D_data, f'{save_path_data}/reduced_3D_data', self.extension_data)

        self.visualiser.create_automatic_scatter_plot(reduced_3D_data,
                                                      f'{save_path_data}/scatter_3D.{self.extension_fig}')

    def make_scatter_2D(self, preprocessed_data, save_path_data):

        reduced_2D_data = self.reducer.run(preprocessed_data, output_dimension=2)
        self.data_manager.store_df(reduced_2D_data, f'{save_path_data}/reduced_2D_data', self.extension_data)

        self.visualiser.create_scatter_matrix(reduced_2D_data,
                                              save_path=f'{save_path_data}/scatter_2D.{self.extension_fig}')


