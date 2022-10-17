import pandas as pd
from DataManagement.ManagementDataFramesPandas import ManageDataFrames
from DataCleaning import CleanData
from Preprocessing import Preprocessing
from DataVisualisation import VisualiseDataPlotlyExpress
from DataVisualisationDashBoard import Dashboard
from ReductionDimension import ReductionDimensionUmap
from DataClustering import UnsupervisedLearning
from Utilities.FileManipulation import create_directory
from Utilities.JsonFunctions import store_json_file
from dataclasses import dataclass


# DataVis :  marginal_x=None, marginal_y=None,

# PROBLEMS
#  LA SERIE TIMESTAMP S'ARRONDI A LA MINUTE POUR LE scatter_timestamp_3D
#
# PROBLEME DE LOGIQUE DANS CLEAN DATA : DROP ROW WITH NA NE FONCITONNE PAS SI = 0.99
#   --> CAR CE CHECK S'EFFECTUE SUR LE DATASET INCLUANT DES COLONNE COMME TS_SERIES ou SEVERITY

# use this for create a main navigator :
# https://stackoverflow.com/questions/25148462/open-a-url-by-clicking-a-data-point-in-plotly

## TO DO
# sauvegarder silhouette score

# PROBLEMES
# rajouter si possible les axes dans heatmap_correlation
# dashboard global analyse affiche seulement le tableau de données
# le scatter 3d fait nptq et il manque la ligne grise
# gerer le pblm des init avec field

@dataclass
class PipeDataAnalyseDataClass:
    # INIT  ###############################################################################################

    # cleaning & preprocessing
    dict_param_clean_data: dict
    dict_param_preprocessing: dict

    dict_list_features_to_save: dict

    # columns in saved data
    list_name_columns_color: list = None
    timestamp_column_name: str = None  # should be a str

    list_discrete_color_for_series_color_imported: list = None  # test non optimal
    mapped_series_color: dict = None

    # extension save data
    extension_data: str = 'csv'
    extension_figure: str = 'html'

    # Reduction Dimension
    list_dimension_to_reduce: list = None
    algorithm_reduction_dimension: str = 'umap'
    dict_param_reduction_dimension: dict = None

    # correlation Analyse
    list_name_data_to_analyse_correlation: list = None
    method_correlation: str = "pearson"

    # clustering
    make_clustering: bool = False
    list_algorithm_clustering: list = 'hdbscan'
    list_dict_param_clustering: list = None
    list_dimensions_to_make_clustering: list = None  # None => clustering on preprocessed_data

    # general figures
    dashboard_data_analyse: bool = False
    scatter_features_timestamp: bool = False
    heatmap_correlation: bool = False
    table_figure: bool = False

    # 2d figures
    dashboard_2D: bool = False
    scatter_2D: bool = False
    scatter_2D_timestamp: bool = False

    # 3d figures
    # dashboard_3D: bool = False
    scatter_3D: bool = False
    scatter_3D_timestamp: bool = False

    # others figures
    histogram_features: bool = False
    scatter_matrix: bool = False

    dict_series_color = {'uncolored': None}
    dict_score_clustering = {}
    report_run = {}

    def __post_init__(self):

        # load objects for treatment ################################################################################

        self.report_run = dict()

        self.data_manager = ManageDataFrames()
        self.cleaner = CleanData()
        self.preprocessor = Preprocessing(**self.dict_param_preprocessing)

        self.visualiser_2 = Dashboard()
        self.visualiser = VisualiseDataPlotlyExpress()

        # Reduction Dimension #######################################################################################

        if type(self.list_dimension_to_reduce) is not list:
            self.list_dimension_to_reduce = [self.list_dimension_to_reduce]

        if None in self.list_dimension_to_reduce:
            self.list_dimension_to_reduce = []

        if self.scatter_2D_timestamp:
            self.list_dimension_to_reduce.append(1)

        if self.scatter_2D or self.scatter_3D_timestamp:
            self.list_dimension_to_reduce.append(2)

        if self.scatter_3D:
            self.list_dimension_to_reduce.append(3)

        self.list_dimension_to_reduce = list(set(self.list_dimension_to_reduce))

        if self.list_dimension_to_reduce is not None:
            self.reducer = ReductionDimensionUmap(self.algorithm_reduction_dimension,
                                                  self.dict_param_reduction_dimension)

        # Correlation Analyse ########################################################################################

        if self.list_name_data_to_analyse_correlation is None:
            self.list_name_data_to_analyse_correlation = []
        if type(self.list_name_data_to_analyse_correlation) is not list:
            self.list_name_data_to_analyse_correlation = [self.list_name_data_to_analyse_correlation]

        #  Clustering ###############################################################################################

        if type(self.list_algorithm_clustering) is not list:
            self.list_algorithm_clustering = [self.list_algorithm_clustering]

        if type(self.list_dict_param_clustering) is not list:
            self.list_dict_param_clustering = [self.list_dict_param_clustering]

        # Figure and Dashboard #######################################################################################

        if self.mapped_series_color is None:
            self.mapped_series_color = {}

        if type(self.list_name_columns_color) is not list:
            self.list_name_columns_color = [self.list_name_columns_color]

        if False in [self.scatter_2D, self.scatter_2D_timestamp]:
            self.dashboard_2D = False

        # if False in [self.scatter_3D, self.scatter_3D_timestamp]:
        #   self.dashboard_3D = False

        if False in [self.scatter_matrix, self.scatter_features_timestamp, self.heatmap_correlation, self.table_figure]:
            self.dashboard_data_analyse = False

    # STOP INIT ###############################################################################################

    # PIPELINES ###############################################################################################

    def pipeline_analyse_multiple_df(self, in_path_data_directory, save_path_root):

        # load dfs
        dict_data_input = ManageDataFrames().load_dict_df(in_path_data_directory)

        create_directory(save_path_root)

        # multiprocessing to setup
        for name_data in dict_data_input.keys():
            self.pipeline_analyse_one_df(dict_data_input[name_data], name_data, f'{save_path_root}/{name_data}')
            self.reset_variables()

    def reset_variables(self):
        self.dict_series_color = {'uncolored': None}
        self.dict_score_clustering = {}
        self.report_run = {}

    def pipeline_analyse_one_df(self, input_data, name_data, save_path):

        create_directory(save_path)

        # data cleaning / preprocessing
        dict_data = self.run_dataframe_treatment(input_data, name_data, f'{save_path}/data')

        # reduction dimension
        dict_data = self.run_reduction_dimension_and_store_data(dict_data, f'{save_path}/data')

        # correlation test
        dict_data = self.correlation_test(dict_data, f'{save_path}/correlated_data')

        # data vis : global figures
        self.create_global_analyse_figures(dict_data, f'{save_path}/general_figures')

        # clustering
        if self.make_clustering:
            self.run_clustering(dict_data)
        self.data_manager.store_df(pd.DataFrame(self.dict_series_color).drop('uncolored', axis=1),
                                   f'{save_path}/data/data_series_color', self.extension_data, False)

        # data vis : figures after clustering
        create_directory(f'{save_path}/figures_colored')
        for label in self.dict_series_color.keys():
            try:
                mapped_series_color = self.mapped_series_color[label[:-2]]
            except KeyError:
                mapped_series_color = None

            self.create_figure_after_clustering(dict_data, self.dict_series_color[label], mapped_series_color,
                                                f'{save_path}/figures_colored/{label}')

        # store report
        store_json_file(self.report_run, path_file=f'{save_path}/report_{name_data}.json')

    # DATA CLEANING / DATA PREPROCESSING #############################################################################

    def run_dataframe_treatment(self, input_data, name_data, save_path):

        create_directory(save_path)
        dict_data = dict()
        dict_data['input_data'] = input_data

        # clean data
        dict_data['cleaned_data'], dict_data['saved_data'] = \
            self.clean_data_and_store_data_to_save(input_data, name_data, save_path)

        # preprocessing
        dict_data['preprocessed_data'] = self.preprocess_and_store_data(dict_data['cleaned_data'], save_path)

        # append timestamp column
        if self.timestamp_column_name is not None:
            dict_data['series_timestamp'] = dict_data['saved_data'][self.timestamp_column_name]

        # append series color already existent and get the silhouette score from preprocessed data
        if self.list_name_columns_color is not None:
            self.append_series_color_to_dict_series_color__get_cluster_score(dict_data)

        return dict_data

    # FUNCTIONS : DATA TREATMENT ######################################################################################

    def clean_data_and_store_data_to_save(self, input_data, name_data, save_path_data):

        # chose corresponding list features to save
        try:
            list_features_to_save = self.dict_list_features_to_save[name_data]
        except KeyError:
            list_features_to_save = None

        # clean
        cleaned_data, data_to_save = self.cleaner.generic_cleaning_dataframe(input_data, list_features_to_save,
                                                                             **self.dict_param_clean_data)

        # store cleaned data
        self.data_manager.store_df(cleaned_data, f'{save_path_data}/cleaned_data', self.extension_data, False)

        # store saved data
        if data_to_save is not None:
            self.data_manager.store_df(data_to_save, f'{save_path_data}/saved_data', self.extension_data, False)

        return cleaned_data, data_to_save

    def preprocess_and_store_data(self, cleaned_data, save_path_data):

        # preprocess
        preprocessed_data = self.preprocessor.preprocessing_data_unlabelled(cleaned_data, out_format='dataframe')

        # store
        self.data_manager.store_df(preprocessed_data, f'{save_path_data}/preprocessed_data', self.extension_data,
                                   False)

        return preprocessed_data

    def append_series_color_to_dict_series_color__get_cluster_score(self, dict_data):

        for name_column in self.list_name_columns_color:
            # append
            self.dict_series_color[f'{name_column}__'] = dict_data['saved_data'][name_column]

            # cluster score
            try:
                self.dict_score_clustering[f'{name_column}__'] = UnsupervisedLearning(None, None) \
                    .silhouette_score(dict_data['preprocessed_data'], dict_data['saved_data'][name_column])
            except ValueError:
                self.dict_score_clustering[f'{name_column}__'] = None

    # REDUCTION DIMENSION ###################################################################################

    def run_reduction_dimension_and_store_data(self, dict_data, save_path_data):

        for dimension in self.list_dimension_to_reduce:

            if dict_data['preprocessed_data'].shape[1] != dimension:
                dict_data[f'{dimension}D_data'] = \
                    self._run_one_reduction_dimension_and_store_data(dict_data['preprocessed_data'], dimension,
                                                                     save_path_data)
            else:
                dict_data[f'{dimension}D_data'] = dict_data['preprocessed_data']

        return dict_data

    def _run_one_reduction_dimension_and_store_data(self, data_to_reduce, dimension, save_path_data=None):

        reduced_data = self.reducer.run(data_to_reduce, output_dimension=dimension, raw_output_returned=False)

        if save_path_data is not None:
            self.data_manager.store_df(reduced_data, f'{save_path_data}/reduced_{dimension}D_data',
                                       self.extension_data, False)

        return reduced_data

    # STATISTICS TESTS ###################################################################################

    def correlation_test(self, dict_data, save_path):

        for name_data in self.list_name_data_to_analyse_correlation:
            name_data_corr = f'{name_data}_data_correlation_matrix'

            try:
                dict_data[name_data_corr] = dict_data[f'{name_data}_data'].corr(method=self.method_correlation)
                self.data_manager.store_df(dict_data[name_data_corr], f'{save_path}/{name_data_corr}',
                                           self.extension_data, False)
            except KeyError:
                self.report_run[name_data_corr] = f'{name_data}_data nonexistent in dict_data'

        return dict_data

    # CLUSTERING ###################################################################################

    def run_clustering(self, dict_data):
        for cluster_name, dict_param in zip(self.list_algorithm_clustering, self.list_dict_param_clustering):
            for dimension in self.list_dimensions_to_make_clustering:

                if dimension is None:
                    self._run_one_clustering(cluster_name, dict_param, dict_data[f'preprocessed_data'])
                else:
                    self._run_one_clustering(cluster_name, dict_param, dict_data[f'{dimension}D_data'])

    def _run_one_clustering(self, cluster_name, dict_param, data):

        cluster = UnsupervisedLearning(cluster_name, dict_param)
        name_series = f'{cluster_name}_on_{data.shape[1]}D_data'

        labels = cluster.fit_predict(data)

        self.dict_series_color[name_series] = pd.Series(labels, name=name_series)

        try:
            self.dict_score_clustering[name_series] = cluster.silhouette_score(data, labels)
        except ValueError:
            self.dict_score_clustering[name_series] = None

    # MANAGER FIGURES CREATION ###################################################################################

    def create_global_analyse_figures(self, dict_data, save_path):

        create_directory(save_path)

        if self.dashboard_data_analyse:
            self.make_dashboard_data_analyse(dict_data['cleaned_data'], dict_data['cleaned_data_correlation_matrix'],
                                             dict_data['series_timestamp'], save_path)
        else:
            if self.scatter_features_timestamp:
                self.make_scatter_features_timestamp(dict_data['series_timestamp'], dict_data['cleaned_data'],
                                                     save_path)
            if self.heatmap_correlation:
                self.make_heatmap_correlation(dict_data['cleaned_data_correlation_matrix'], save_path)

            if self.table_figure:
                self.make_table_figure(dict_data['cleaned_data'], save_path)

    # CAN BE SIMPLIFIED IF THE CLASS DASHBOARD BECOME SMARTER
    def create_figure_after_clustering(self, dict_data, series_color, list_discrete_color, save_path):

        create_directory(save_path)

        if self.scatter_matrix:
            self.make_scatter_matrix(dict_data['cleaned_data'], series_color, save_path)

        if self.histogram_features:
            self.make_histogram_features(dict_data['cleaned_data'], series_color, save_path)

        if self.dashboard_2D:
            try:
                self.make_dashboard_2D(dict_data['2D_data'], dict_data['1D_data'],
                                       dict_data['series_timestamp'], series_color, list_discrete_color,
                                       save_path)
            except KeyError as non_existent_data:
                self.report_run['2D_dashboard'] = non_existent_data
        else:
            if self.scatter_2D:
                try:
                    self.make_scatter_2D(dict_data['2D_data'], series_color, list_discrete_color, save_path)
                except KeyError as non_existent_data:
                    self.report_run['2D_dashboard'] = non_existent_data

            if self.scatter_2D_timestamp:
                try:
                    self.make_scatter_2D_timestamp(dict_data['series_timestamp'], dict_data['2D_data'],
                                                   list_discrete_color, series_color, save_path)
                except KeyError as non_existent_data:
                    self.report_run['2D_dashboard'] = non_existent_data

        # if self.dashboard_3D:
        #   try:
        # self.make_dashboard_3D(dict_data['3D_data'], dict_data['2D_data'],
        #   dict_data['series_timestamp'], series_color, save_path)
        #   except KeyError as non_existent_data:
        # self.report['2D_dashboard'] = non_existent_data
        # else:
        if self.scatter_3D:
            try:
                self.make_scatter_3D(dict_data['3D_data'], series_color, save_path)
            except KeyError as non_existent_data:
                self.report_run['2D_dashboard'] = non_existent_data
        if self.scatter_3D_timestamp:
            try:
                self.make_scatter_3D_timestamp(dict_data['series_timestamp'], dict_data['3D_data'], series_color,
                                               save_path)
            except KeyError as non_existent_data:
                self.report_run['2D_dashboard'] = non_existent_data

    # GLOBAL FIGURES ###############################################################################################

    def make_dashboard_data_analyse(self, data, correlated_data, series_timestamp, save_path):

        self.visualiser_2.dataframe__heatmap_correlation__scatter_features(data, correlated_data, series_timestamp,
                                                                           f'{save_path}/dashboard_data_analyse.{self.extension_figure}')

    def make_scatter_features_timestamp(self, series_timestamp, data, save_path):
        figure = self.visualiser_2.subplot.create_multiple_scatter_line(series_timestamp, data, None)
        self.visualiser_2.store_or_return_figure(figure,
                                                 f'{save_path}/scatter_features_timestamp.{self.extension_figure}')

    def make_heatmap_correlation(self, correlated_data, save_path):
        figure = self.visualiser_2.subplot.create_heatmap(correlated_data, True, True, None)
        self.visualiser_2.store_or_return_figure(figure, f'{save_path}/heatmap_correlation.{self.extension_figure}')

    def make_table_figure(self, data, save_path):
        figure = self.visualiser_2.subplot.create_table_figure(data, None)
        self.visualiser_2.store_or_return_figure(figure, f'{save_path}/table_figure.{self.extension_figure}')

    # HISTOGRAM FEATURES MATRIX ###################################################################################

    def make_scatter_matrix(self, data, series_color, save_path):

        figure = self.visualiser_2.subplot.create_scatter_plot_matrix(data, series_color, show_scale=True)
        self.visualiser_2.store_or_return_figure(figure, f'{save_path}/scatter_matrix.{self.extension_figure}')

    def make_histogram_features(self, data, series_color, save_path):
        self.visualiser_2.histograms_features(data, series_color,
                                              save_path=f"{save_path}/histogram_features.{self.extension_figure}")

    # 2D : DASHBOARD AND FIGURES ###################################################################################

    def make_dashboard_2D(self, data_2D, data_1D, series_timestamp, series_color, list_discrete_color, save_path):

        self.visualiser_2. \
            plot_reduced_2D_data_markers__reduced_1D_data_ts_line(data_2D, data_1D, series_timestamp,
                                                                  series_color, 'dashboard_2D',
                                                                  list_discrete_color,
                                                                  f'{save_path}/dashboard_2D.{self.extension_figure}')

    # 2D markers
    def make_scatter_2D(self, data_2D, series_color, list_discrete_color, save_path):

        figure = self.visualiser_2.subplot.create_scatter_plot_2D(data_2D.iloc[:, 0],
                                                                  data_2D.iloc[:, 1],
                                                                  series_color, mode='markers', show_legend=True,
                                                                  mapped_series_color=list_discrete_color)
        self.visualiser_2.store_or_return_figure(figure, f'{save_path}/scatter_2D.{self.extension_figure}')

    # 2D timestamp
    def make_scatter_2D_timestamp(self, series_timestamp, data_1D, series_color, list_discrete_color, save_path):

        figure = self.visualiser_2.subplot.create_scatter_plot_2D(series_timestamp, data_1D.iloc[:, 0], series_color,
                                                                  mapped_series_color=list_discrete_color)
        self.visualiser_2.store_or_return_figure(figure, f'{save_path}/scatter_2D_timestamp.{self.extension_figure}')

    # 3D DASHBOARD AND FIGURES ###################################################################################

    # 3D dashboard
    def make_dashboard_3D(self, data_3D, data_2D, series_timestamp, series_color, save_path):
        pass
        # self.visualiser_2. \
        #  plot_reduced_3D_data_markers__reduced_2D_data_ts_line(data_3D, data_2D, series_timestamp, series_color,
        #                                                      'dashboard_3D',  # useless to test
        #                                                       f'{save_path}/dashboard_3D.{self.extension_figure}')

    # 3D markers
    def make_scatter_3D(self, data_3D, series_color, save_path):

        figure = self.visualiser_2.subplot.create_scatter_plot_3D(data_3D.iloc[:, 0], data_3D.iloc[:, 1],
                                                                  data_3D.iloc[:, 2], series_color,
                                                                  mode='markers', show_legend=True)
        self.visualiser_2.store_or_return_figure(figure, f'{save_path}/scatter_3D.{self.extension_figure}')

    # 3D timestamp
    def make_scatter_3D_timestamp(self, series_timestamp, data_2D, series_color, save_path):

        figure = self.visualiser_2.subplot.create_scatter_plot_3D(series_timestamp,
                                                                  data_2D.iloc[:, 0], data_2D.iloc[:, 1],
                                                                  series_color, show_legend=True)
        self.visualiser_2.store_or_return_figure(figure, f'{save_path}/scatter_3D_timestamp.{self.extension_figure}')
