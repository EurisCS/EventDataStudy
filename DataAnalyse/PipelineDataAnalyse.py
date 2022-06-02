from Preprocessing import Preprocessing
from DataCleaning import CleanData
from DataVisualisation import VisualiseDataPlotlyExpress, VisualiseDataPlotlyGo
from ReductionDimension import ReductionDimensionUmap
from DataManagement.PandasFrameManagement import ManageDataFrames

from Utilities.FileManipulation import create_directory
from Utilities.ErrorManagement import ErrorManagement
from Utilities.JsonFunctions import store_json_file


# from StatisticAnalyse import CorrelationTest


# Non setup Args ::
#
# Preprocessing : impute_missing_numerical_value, impute_missing_categorical_value, scaler, encoder
# DataVis :  marginal_x=None, marginal_y=None,


# TO DO ::
#
# rajouter axe bloqué et gerer le pblm de changement de dimension quand on ajoute un/ des axes bloqué

class PipelineDataAnalyse:

    def __init__(self, dict_param_clean_data, dict_param_preprocessing,
                 extension_data='pickle', extension_figure='html',
                 algorithm_reduction_dimension='umap', dict_param_reduction_dimension=None,
                 scatter_matrix=True, scatter_features=False, heatmap=False, scatter_1D=False, scatter_2D=False,
                 scatter_3D=False,
                 scatter_ternary=False, scatter_2D_timestamp=False, scatter_3D_timestamp=False,
                 histogram_timestamp=None):

        """
            :param dict_param_clean_data: parameter for the main function in Clean Data Module
            :param extension_data:  extension of the data will be save (csv, pickle, ...)
            :param extension_figure: extension of the figure will be save (html, png, ...)
            :param algorithm_reduction_dimension: method used for r_dim (umap, parametric_umap, ...)
            :param dict_param_reduction_dimension: dict param for the r_dim
            :param scatter_matrix: if you want to create a scatter matrix
            :param heatmap: if you want to create a heatmap correlation features
            :param scatter_2D:  if you want to create a 2D plot ( created after a reduction dimension of the dataset )
            :param scatter_3D: if you want to create a 3D plot ( created after a reduction dimension of the dataset )

            :param scatter_ternary: if you want to create a 3D plot ( created after a reduction dimension of the dataset )
            :param scatter_2D_timestamp: if you want to create a 2D plot with x the timestamp axe. !!
                timestamp axe need to be the first column in saved data arg in the clean_data dict_param
            :param scatter_3D_timestamp: if you want to create a 3D plot with x the timestamp axe. !!
                timestamp axe need to be the first column in saved data arg in the clean_data dict_param
        """

        # load objects for treatment
        self.cleaner = CleanData()
        self.preprocessor = Preprocessing(**dict_param_preprocessing)
        self.visualiser = VisualiseDataPlotlyExpress()
        self.visualiser_go = VisualiseDataPlotlyGo()
        self.data_manager = ManageDataFrames()
        self.error_manager = ErrorManagement()

        # set up the reducer
        if scatter_3D or scatter_2D:
            self.reducer = ReductionDimensionUmap(algorithm_reduction_dimension, dict_param_reduction_dimension)  # V

        self.dict_param_clean_data = dict_param_clean_data

        # extension save
        self.extension_data = extension_data
        self.extension_fig = extension_figure

        # chose program
        self.scatter_matrix = scatter_matrix
        self.scatter_features = scatter_features  # PROBLEMATIQUE POUR LES VARIABLES CATEGORIELLE ?
        self.heatmap = heatmap
        self.scatter_1D = scatter_1D
        self.scatter_2D = scatter_2D
        self.scatter_3D = scatter_3D
        self.scatter_ternary = scatter_ternary
        self.scatter_2D_timestamp = scatter_2D_timestamp
        self.scatter_3D_timestamp = scatter_3D_timestamp
        self.histogram_timestamp = histogram_timestamp

    # PIPELINES ################################################################################################

    def pipeline_multiple_df(self, in_path_data_directory, save_path_data_root):
        """
        :param in_path_data_directory:  path of the directory where the df to load are stored
        :param save_path_data_root: path where the new dfs were store
        :return: None
        """

        dict_df_input = ManageDataFrames().load_dict_df(in_path_data_directory)  # load dfs
        create_directory(save_path_data_root)

        # multiprocessing to setup
        for name_df in dict_df_input.keys():
            current_save_path_data = f'{save_path_data_root}/{name_df}'

            create_directory(current_save_path_data)

            self.pipeline_one_df(dict_df_input[name_df], current_save_path_data)

            store_json_file(self.cleaner.report, f'{current_save_path_data}/report_clean_data.json')

    def pipeline_one_df(self, input_data, save_path_data):

        cleaned_data, saved_data = self.clean_data_and_store_data_to_save(input_data, save_path_data)

        preprocessed_data = self.preprocess_and_store_data(cleaned_data, save_path_data)

        if self.scatter_matrix:
            self.make_scatter_matrix(cleaned_data, save_path_data)

        if self.scatter_features:
            self.make_scatter_features(saved_data.iloc[:, 0], preprocessed_data, save_path_data)

        if self.heatmap:
            self.make_heatmap_correlation(cleaned_data, save_path_data)

        if self.scatter_1D or self.scatter_2D_timestamp or self.histogram_timestamp:

            reduced_1D_data = self.run_reduction_dimension_and_store_data(preprocessed_data, 1, save_path_data)

            if self.scatter_1D:
                self.make_scatter_plot(reduced_1D_data, save_path_data)

            if self.scatter_2D_timestamp:
                self.make_scatter_line(saved_data.iloc[:, 0], reduced_1D_data.iloc[:, 0], None, save_path_data)

            if self.histogram_timestamp:
                self.make_histogram(saved_data.iloc[:, 0], reduced_1D_data.iloc[:, 0], save_path_data)

        if self.scatter_2D or self.scatter_3D_timestamp:

            reduced_2D_data = self.run_reduction_dimension_and_store_data(preprocessed_data, 2, save_path_data)

            if self.scatter_2D:
                self.make_scatter_plot(reduced_2D_data, save_path_data)

            if self.scatter_3D_timestamp:
                self.make_scatter_line(saved_data.iloc[:, 0], reduced_2D_data.iloc[:, 0],
                                       reduced_2D_data.iloc[:, 1], save_path_data)

        # need to add data not treated
        if self.scatter_3D or self.scatter_ternary:

            reduced_3D_data = self.run_reduction_dimension_and_store_data(preprocessed_data, 3, save_path_data)

            if self.scatter_3D:
                self.make_scatter_plot(reduced_3D_data, save_path_data)

            if self.scatter_ternary:
                self.make_scatter_ternary(reduced_3D_data, save_path_data)

    # DATA TREATMENT ################################################################################################

    def clean_data_and_store_data_to_save(self, input_data, save_path_data):

        cleaned_data, data_to_save = self.cleaner(input_data, **self.dict_param_clean_data)

        if data_to_save is not None:
            self.data_manager.store_df(data_to_save, f'{save_path_data}/saved_data', self.extension_data)

        return cleaned_data, data_to_save

    def preprocess_and_store_data(self, cleaned_data, save_path_data):

        # preprocess
        preprocessed_data = self.preprocessor.preprocessing_data_unlabelled(cleaned_data, out_format='dataframe')

        # store
        self.data_manager.store_df(preprocessed_data, f'{save_path_data}/preprocessed_data', self.extension_data)

        return preprocessed_data

    def run_reduction_dimension_and_store_data(self, data_to_reduce, dimension, save_path_data=None):

        reduced_data = self.reducer.run(data_to_reduce, output_dimension=dimension, raw_output_returned=False)

        if save_path_data is not None:
            self.data_manager.store_df(reduced_data, f'{save_path_data}/reduced_{dimension}D_data', self.extension_data)

        return reduced_data

    # FIGURE CREATION ###################################################################################

    # oo D
    def make_heatmap_correlation(self, cleaned_data, save_path_data):

        correlated_data = cleaned_data.corr(method='pearson')

        self.data_manager.store_df(correlated_data, f'{save_path_data}/correlated_data', self.extension_data)

        self.visualiser.create_heatmap(correlated_data, f'{save_path_data}/heatmap_correlation.{self.extension_fig}')

    # oo D
    def make_scatter_matrix(self, preprocessed_data, save_path_data):
        self.visualiser.create_scatter_matrix(preprocessed_data,
                                              save_path=f'{save_path_data}/scatter_matrix.{self.extension_fig}')

    # 2D
    def make_scatter_features(self, series_x, data_y, save_path_data):
        self.visualiser_go.create_multiple_scatter_line(series_x, data_y, save_path=
        f'{save_path_data}/scatter_features_2D_timestamp.{self.extension_fig}')

    # 1D 2D 3D
    def make_scatter_plot(self, data_to_plot, save_path_data):
        self.visualiser.create_automatic_scatter_plot(
            data_to_plot, save_path=f'{save_path_data}/scatter_{data_to_plot.shape[1]}D.{self.extension_fig}')

    # 2D
    def make_histogram(self, x_series, y_series, save_path_data):
        self.visualiser.create_histogram(x_series, y_series,
                                         f'{save_path_data}/histogram_timestamp.{self.extension_fig}')

    # 3D
    def make_scatter_ternary(self, reduced_3D_data, save_path_data):
        self.visualiser.create_scatter_ternary(reduced_3D_data,
                                               save_path=f'{save_path_data}/scatter_ternary.{self.extension_fig}')

    # 2D 3D
    def make_scatter_line(self, x_series, y_series, z_series, save_path_data):

        if z_series is None:
            dimension = 2
        else:
            dimension = 3

        self.visualiser.create_automatic_scatter_line(x_series, y_series, z_series, markers=True,
                                                      save_path=f'{save_path_data}/scatter_{dimension}D_timestamp.'
                                                                f'{self.extension_fig}')
