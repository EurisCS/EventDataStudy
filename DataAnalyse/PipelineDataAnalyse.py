from DataManagement.ManagementDataFramesPandas import ManageDataFrames
from DataCleaning import CleanData
from Preprocessing import Preprocessing
from DataVisualisation import VisualiseDataPlotlyExpress
from ReductionDimension import ReductionDimensionUmap
from DataClustering import UnsupervisedLearning

from Utilities.FileManipulation import create_directory
from Utilities.JsonFunctions import store_json_file


# Non setup Args ::
#
# Preprocessing : impute_missing_numerical_value, impute_missing_categorical_value, scaler, encoder
# DataVis :  marginal_x=None, marginal_y=None,

## PROBLEMS
#  LA SERIE TIMESTAMP S'ARRONDI A LA MINUTE POUR LE scatter_timestamp_3D
#
# PROBLEME DE LOGIQUE DANS CLEAN DATA : DROP ROW WITH NA NE FONCITONNE PAS SI = 0.99
#   --> CAR ON VERIFIE DES COLONNE COMME TS_SERIES ou SEVERITY


## TO DO
# indicateurs du meilleurs clustering
# Possibilitée de clusteriser sur les données réduites 2D 3D etc...


class PipelineDataAnalyse:

    def __init__(self, dict_param_clean_data, dict_param_preprocessing,
                 extension_data='pickle', extension_figure='html',
                 algorithm_reduction_dimension='umap', dict_param_reduction_dimension=None,
                 list_algorithm_clustering='hdbscan', list_dict_param_clustering=None,

                 list_name_column_color_name=None, timestamp_column_name=None,
                 make_clustering=False,
                 scatter_2D=False,
                 scatter_3D=False,
                 scatter_ternary=False,
                 scatter_matrix=True,
                 scatter_2D_timestamp=False,
                 scatter_3D_timestamp=False,
                 scatter_features_timestamp=False,
                 histogram_timestamp=False,
                 heatmap_correlation=False):

        # load objects for treatment
        self.data_manager = ManageDataFrames()
        self.cleaner = CleanData()
        self.preprocessor = Preprocessing(**dict_param_preprocessing)
        self.visualiser = VisualiseDataPlotlyExpress()
        # set up the reducer
        if True in [scatter_2D, scatter_3D, scatter_ternary, scatter_2D_timestamp, scatter_3D_timestamp,
                    histogram_timestamp]:
            self.reducer = ReductionDimensionUmap(algorithm_reduction_dimension, dict_param_reduction_dimension)

        self.list_name_clustering = list_algorithm_clustering
        if type(self.list_name_clustering) in [str, None]:
            self.list_name_clustering = [self.list_name_clustering]

        self.list_dict_param_clustering = list_dict_param_clustering
        if type(self.list_dict_param_clustering) in [dict, None]:
            self.list_dict_param_clustering = [self.list_dict_param_clustering]

        self.dict_param_clean_data = dict_param_clean_data

        # in saved data
        self.timestamp_column_name = timestamp_column_name

        # in saved data
        if type(list_name_column_color_name) is str:
            list_name_column_color_name = [list_name_column_color_name]
        self.list_name_column_color_name = list_name_column_color_name

        # dict of series color/label
        self.dict_series_color = {'uncolored': None}

        # extension save
        self.extension_data = extension_data
        self.extension_fig = extension_figure

        # chose program
        self.make_clustering = make_clustering

        self.scatter_2D = scatter_2D
        self.scatter_3D = scatter_3D
        self.scatter_ternary = scatter_ternary
        self.scatter_matrix = scatter_matrix
        self.scatter_2D_timestamp = scatter_2D_timestamp
        self.scatter_3D_timestamp = scatter_3D_timestamp
        self.scatter_features_timestamp = scatter_features_timestamp
        self.histogram_timestamp = histogram_timestamp
        self.heatmap_correlation = heatmap_correlation

    def pipeline_multiple_df(self, in_path_data_directory, save_path_root):

        create_directory(save_path_root)

        # load dfs
        dict_df_input = ManageDataFrames().load_dict_df(in_path_data_directory)

        # multiprocessing to setup
        for name_df in dict_df_input.keys():
            self.pipeline_one_df(dict_df_input[name_df], f'{save_path_root}/{name_df}')

    def pipeline_one_df(self, input_data, save_path):

        create_directory(save_path)

        dict_data = self.run_dataframe_treatment(input_data, f'{save_path}/data')

        self.run_global_figure_creation(dict_data, f'{save_path}/global_figures')

        for label in self.dict_series_color.keys():
            self.run_figure_creation(dict_data, self.dict_series_color[label], f'{save_path}/{label}')

        store_json_file(self.cleaner.report, f'{save_path}/report_clean_data.json')

    # PIPELINE : DATA TREATMENT ######################################################################################

    def run_dataframe_treatment(self, input_data, save_path_data):

        create_directory(save_path_data)

        dict_data = dict()

        dict_data['cleaned_data'], dict_data['saved_data'] = \
            self.clean_data_and_store_data_to_save(input_data, save_path_data)

        if self.timestamp_column_name is not None:
            dict_data['timestamp_series'] = dict_data['saved_data'][self.timestamp_column_name]

        if self.list_name_column_color_name is not None:
            for name_column in self.list_name_column_color_name:
                self.dict_series_color[name_column] = dict_data['saved_data'][name_column]

        dict_data['preprocessed_data'] = \
            self.preprocess_and_store_data(dict_data['cleaned_data'], save_path_data)

        if self.make_clustering:
            for cluster_name, dict_param in zip(self.list_name_clustering, self.list_dict_param_clustering):
                self.dict_series_color[cluster_name] = self.run_clustering(cluster_name, dict_param,
                                                                           dict_data['preprocessed_data'])

        if self.scatter_2D_timestamp or self.histogram_timestamp:
            dict_data['reduced_1D_data'] = self.run_reduction_dimension_and_store_data(dict_data['preprocessed_data'],
                                                                                       1, save_path_data)

        if self.scatter_2D or self.scatter_3D_timestamp:
            dict_data['reduced_2D_data'] = self.run_reduction_dimension_and_store_data(dict_data['preprocessed_data'],
                                                                                       2, save_path_data)

        if self.scatter_3D or self.scatter_ternary:
            dict_data['reduced_3D_data'] = self.run_reduction_dimension_and_store_data(dict_data['preprocessed_data'],
                                                                                       3, save_path_data)
        if self.heatmap_correlation:
            dict_data['data_correlation_matrix'] = dict_data['cleaned_data'].corr(method='pearson')
            self.data_manager.store_df(dict_data['data_correlation_matrix'],
                                       f'{save_path_data}/data_correlation_matrix', self.extension_data, False)

        return dict_data

    # FUNCTIONS : DATA TREATMENT ######################################################################################

    def clean_data_and_store_data_to_save(self, input_data, save_path_data):

        cleaned_data, data_to_save = self.cleaner(input_data, **self.dict_param_clean_data)

        self.data_manager.store_df(cleaned_data, f'{save_path_data}/cleaned_data', self.extension_data, False)

        if data_to_save is not None:
            self.data_manager.store_df(data_to_save, f'{save_path_data}/saved_data', self.extension_data, False)

        return cleaned_data, data_to_save,

    def preprocess_and_store_data(self, cleaned_data, save_path_data):

        # preprocess
        preprocessed_data = self.preprocessor.preprocessing_data_unlabelled(cleaned_data, out_format='dataframe')

        # store
        self.data_manager.store_df(preprocessed_data, f'{save_path_data}/preprocessed_data', self.extension_data, False)

        return preprocessed_data

    def run_reduction_dimension_and_store_data(self, data_to_reduce, dimension, save_path_data=None):

        reduced_data = self.reducer.run(data_to_reduce, output_dimension=dimension, raw_output_returned=False)

        if save_path_data is not None:
            self.data_manager.store_df(reduced_data, f'{save_path_data}/reduced_{dimension}D_data',
                                       self.extension_data, False)

        return reduced_data

    @staticmethod
    def run_clustering(cluster_name, dict_param, preprocessed_data):
        return UnsupervisedLearning(cluster_name, dict_param).fit_predict(preprocessed_data)

    # PIPELINE : FIGURE CREATION ######################################################################################

    def run_global_figure_creation(self, dict_data, save_path):

        create_directory(save_path)

        if self.heatmap_correlation:
            self.make_heatmap_correlation(dict_data['data_correlation_matrix'], save_path)

        if self.scatter_features_timestamp:
            self.make_scatter_features_timestamp(dict_data['timestamp_series'], dict_data['preprocessed_data'], save_path)

        '''
            
            
        if self.dataframe_figure:
            self.make_dataframe_figure(dict_data['cleaned_data'], save_path)
        '''

    def run_figure_creation(self, dict_data, series_color, save_path):

        create_directory(save_path)

        print(f'TYPE_SERIES_COLOR : {type(series_color)}')

        if self.scatter_2D:
            self.make_scatter_plot_2D(dict_data['reduced_2D_data'], series_color, save_path)

        if self.scatter_3D:
            self.make_scatter_plot_3D(dict_data['reduced_3D_data'], series_color, save_path)

        if self.scatter_ternary:
            self.make_scatter_plot_ternary(dict_data['reduced_3D_data'], series_color, save_path)

        if self.scatter_matrix:
            self.make_scatter_matrix(dict_data['cleaned_data'], series_color, save_path)

        if self.scatter_2D_timestamp:
            self.make_scatter_timestamp_2D(dict_data['timestamp_series'], dict_data['reduced_1D_data'], series_color,
                                           save_path)
            self.make_scatter_timestamp_2D_continuous(dict_data['timestamp_series'], dict_data['reduced_1D_data'],
                                                      series_color, save_path)

        if self.scatter_3D_timestamp:
            self.make_scatter_timestamp_3D(dict_data['timestamp_series'], dict_data['reduced_2D_data'], series_color,
                                           save_path)

        if self.histogram_timestamp:
            self.make_histogram_timestamp(dict_data['timestamp_series'], dict_data['reduced_1D_data'], series_color,
                                          save_path)
        '''
            if self.histogram_features:
                self.make_histogram_features()
        '''
    # FUNCTIONS : FIGURE CREATION ###################################################################################

    # 2D
    def make_scatter_plot_2D(self, reduced_2D_data, series_color, save_path):
        self.visualiser.create_scatter_plot_2D(reduced_2D_data.iloc[:, 0],
                                               reduced_2D_data.iloc[:, 1],
                                               series_color,
                                               f'{save_path}/scatter_plot_2D.{self.extension_fig}')

    # 3D
    def make_scatter_plot_3D(self, reduced_3D_data, series_color, save_path):
        self.visualiser.create_scatter_plot_3D(reduced_3D_data.iloc[:, 0],
                                               reduced_3D_data.iloc[:, 1],
                                               reduced_3D_data.iloc[:, 2],
                                               series_color,
                                               f'{save_path}/scatter_plot_3D.{self.extension_fig}')

    # 2D
    def make_scatter_plot_ternary(self, reduced_3D_data, series_color, save_path):
        self.visualiser.create_scatter_ternary(reduced_3D_data.iloc[:, 0],
                                               reduced_3D_data.iloc[:, 1],
                                               reduced_3D_data.iloc[:, 2],
                                               series_color,
                                               f'{save_path}/scatter_ternary.{self.extension_fig}')

    # 2D
    def make_scatter_matrix(self, cleaned_data, series_color, save_path):

        self.visualiser.create_scatter_matrix(cleaned_data,
                                              series_color,
                                              f'{save_path}/scatter_matrix.{self.extension_fig}')

    # 2D
    def make_scatter_timestamp_2D(self, timestamp_series, reduced_1D_data, series_color, save_path):
        self.visualiser.create_scatter_line_2D_3D_color_discrete(timestamp_series,
                                                                 reduced_1D_data.iloc[:, 0],
                                                                 None,
                                                                 series_color,
                                                                 f'{save_path}/scatter_2D_timestamp.{self.extension_fig}')

    def make_scatter_timestamp_2D_continuous(self, timestamp_series, reduced_1D_data, series_color, save_path):
        self.visualiser.create_scatter_line_2D_3D_color_scale(timestamp_series,
                                                              reduced_1D_data.iloc[:, 0],
                                                              None,
                                                              series_color,
                                                              f'{save_path}/scatter_2D_timestamp_continuous.{self.extension_fig}')


    # 3D
    def make_scatter_timestamp_3D(self, timestamp_series, reduced_2D_data, series_color, save_path):
        self.visualiser.create_scatter_line_2D_3D_color_discrete(timestamp_series,
                                                                 reduced_2D_data.iloc[:, 0],
                                                                 reduced_2D_data.iloc[:, 1],
                                                                 series_color,
                                                                 f'{save_path}/scatter_3D_timestamp.{self.extension_fig}')

    # 2D
    def make_scatter_features_timestamp(self, timestamp_series, preprocessed_data, save_path):
        self.visualiser.create_multiple_scatter_line(timestamp_series,
                                                     preprocessed_data,
                                                     'lines+markers',
                                                     f'{save_path}/scatter_features_2D_timestamp.{self.extension_fig}')

    # 2D
    def make_histogram_timestamp(self, timestamp_series, reduced_1D_data, series_color, save_path_data):
        self.visualiser.create_histogram(timestamp_series,
                                         reduced_1D_data.iloc[:, 0],
                                         series_color,
                                         f'{save_path_data}/histogram_timestamp.{self.extension_fig}')

    # ooD
    def make_heatmap_correlation(self, correlated_data, save_path_data):
        self.visualiser.create_heatmap(correlated_data,
                                       f'{save_path_data}/heatmap_correlation.{self.extension_fig}')
