from dataclasses import dataclass
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from DataManagement.ManagementDataFramesPandas import ManageDataFrames
from DataAnalyse.Preprocessing import Preprocessing
from SupervisedLearning import SupervisedLearning
from Utilities.FileManipulation import create_directory, store_object_as_pickle


@dataclass
class PipelineSupervisedLearning:

    # INIT ####################################################################################

    input_path_data: str
    save_path_root: str

    split_files: dict
    non_split_files: dict

    dict_params_cross_validate: dict

    list_name_model: list
    list_dict_params: list = None

    name_column_label: str = None
    encode_y_data: bool = True
    preprocess_x_data: bool = True
    test_size: int = None
    classification: bool = True
    random_state_train_test_split: int = 42

    '''
        "general_result_dashboard": true,
        "log_loss": true,
        "histogram_result": true,
        "confusion_matrix": true,
        "plot_auc": true
    '''

    def __post_init__(self):
        self.data_manager = ManageDataFrames()
        self.dict_data = dict()

        if self.list_dict_params is None:
            self.list_dict_params = [{} for _ in range(len(self.list_name_model))]

    # PIPELINES CROSS VALIDATES ####################################################################################

    def pipeline_repeated_cross_validate_multiple_models(self):

        create_directory(self.save_path_root)

        # data load, prepare
        dict_data = self.load_data__make_treatment_if_necessary()

        # store
        self.store_dict_data_as_pickle(dict_data)

        # run cross val fitting foreach model
        for name_model, dict_params_model in zip(self.list_name_model, self.list_dict_params):
            self.repeated_cross_validate_one_model(dict_data, name_model, dict_params_model,
                                                   f'{self.save_path_root}/{name_model}')

    #  LOAD INPUT DATA ####################################################################################

    def load_data__make_treatment_if_necessary(self):

        dict_data = self._load_data_from_split_files()

        if dict_data == dict():
            X_data, y_data = self._load_data_from_non_split_files()
            dict_data = self._make_preprocessing(X_data, y_data)

        return dict_data

    # when we load a set of x_train, y_train, X_test, y_test files
    def _load_data_from_split_files(self):

        dict_data = dict()

        for type_file in self.split_files:
            if self.split_files is not None:
                try:
                    dict_data[type_file] = self.data_manager.load_df_csv(
                        f'{self.input_path_data}/{self.split_files[type_file]}')
                except FileNotFoundError:
                    pass

        return dict_data

    # when we load a set of X,y files
    def _load_data_from_non_split_files(self):

        # load y_data (label series)
        y_data = self.data_manager.load_df_csv(f'{self.input_path_data}/{self.non_split_files["y_data"]}')

        # chose the right column if necessary
        if self.name_column_label is not None:
            y_data = y_data[self.name_column_label]

        if self.encode_y_data:
            y_data = LabelEncoder().fit_transform(y_data)

        # load x_data
        x_data = self.data_manager.load_df_csv(f'{self.input_path_data}/{self.non_split_files["x_data"]}')

        return x_data, y_data

    def _make_preprocessing(self, x_data, y_data):

        preprocessor = Preprocessing()
        dict_data = dict()

        if not self.preprocess_x_data:

            if self.test_size is None:
                dict_data['x_train'], dict_data['y_train'] = x_data, y_data
            else:
                dict_data['x_train'], dict_data['x_test'], dict_data['y_train'], dict_data['y_test'] = \
                    preprocessor.train_test_split_data(x_data, y_data, self.test_size,
                                                       self.random_state_train_test_split, self.classification)
        else:
            if self.test_size is None:
                dict_data['x_train'], dict_data['y_train'] = \
                    preprocessor.preprocessing_labelled_data_into_train_set(x_data, y_data)
            else:
                dict_data['x_train'], dict_data['x_test'], dict_data['y_train'], dict_data['y_test'] = \
                    preprocessor.preprocessing_labelled_data_into_train_test_set(x_data, y_data, self.test_size,
                                                                                 self.random_state_train_test_split)

        return dict_data

    # STORE DATA CREATED ###########################################################################################

    def store_dict_data_as_pickle(self, dict_data):
        create_directory(f'{self.save_path_root}/data')
        for key in dict_data.keys():
            store_object_as_pickle(dict_data[key], f'{self.save_path_root}/data/{key}')

    # CROSS VALIDATE ###########################################################################################

    def repeated_cross_validate_one_model(self, dict_data, name_model, dict_params_model, save_path):

        create_directory(save_path)

        # create supervisor
        supervisor = SupervisedLearning(name_model, self.classification, dict_params_model)

        # run cv for this model
        list_dict_results = supervisor.repeated_cross_validate_fitting(dict_data['x_train'], dict_data['y_train'],
                                                                       **self.dict_params_cross_validate)

        # store result
        self.data_manager.store_df(pd.DataFrame(list_dict_results), f'{save_path}/result', 'csv', False)

        # self.create_plots_results_from_list_dict_models(list_dict_model)  # plot

    # TREATMENT RESULTS ##########################################################################################

    def create_plots_results_from_list_dict_models(self, list_dict_model):
        pass
