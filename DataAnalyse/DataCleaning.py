import pandas as pd


class CleanData:

    def __init__(self):
        self.toolbox = CleanDataToolBox()
        self.report = dict()

    def __call__(self, data, columns_to_save_out, columns_to_delete,
                 threshold_na_in_column=0.5, threshold_na_in_row=0.2,
                 threshold_correlation=0.95, reset_index=True):

        self.report = dict()
        self.report['init_shape'] = str(data.shape)

        if reset_index:
            data = data.reset_index(drop=True)

        # drop duplicates rows
        data = self.toolbox.drop_duplicates_row(data)
        self.report['drop_duplicates_row'] = str(data.shape)

        # drop rows by checking Nan
        data = self.toolbox.drop_row_with_na(data, threshold_na_in_row)
        self.report['drop_na_row'] = str(data.shape)

        # save data from columns_to_save_out && delete data from columns_to_delete
        data, saved_data = self.save_and_drop_columns(data, columns_to_save_out, columns_to_delete)
        self.report['saved_data'] = str(saved_data.shape)

        # drop columns by checking Nan & constants
        data = self.toolbox.drop_na_and_constants_columns(data, threshold_na_in_column)
        self.report['drop_na_and_constants_columns'] = str(data.shape)

        data = self.toolbox.drop_correlated_data(data, threshold=threshold_correlation)
        self.report['drop_correlated_data'] = str(data.shape)

        return data, saved_data

    def save_and_drop_columns(self, data, columns_to_save_out, columns_to_delete):
        # drop data to save
        data, saved_data = self.toolbox.split_data_from_list(data, columns_to_save_out)

        self.report['column_to_saves'] = str(data.shape)

        # delete data to delete
        data, __ = self.toolbox.split_data_from_list(data, columns_to_delete)

        self.report['columns_to_delete'] = str(data.shape)

        return data, saved_data


class CleanDataToolBox:

    # COLUMNS TREATMENT ############################################################################################

    @staticmethod
    def split_data_from_list(data, list_data_to_drop):

        if list_data_to_drop is not None:
            if type(list_data_to_drop) is str:
                list_data_to_drop = [list_data_to_drop]

            # split
            try:
                data_dropped = data[list_data_to_drop]
                data = data.drop(list_data_to_drop, axis=1)

                if data_dropped.shape[1] == 0:  # check data dropped
                    return data, pd.DataFrame()
                return data, data_dropped
            except KeyError:
                return data, pd.DataFrame()

        return data, pd.DataFrame()

    @staticmethod
    def drop_correlated_data(data, threshold=0.95):

        if threshold is None:
            return data

        column_to_drop = set()
        corr_matrix = abs(data.corr())

        # browse the lower part of the correlated matrix
        for index_col in range(len(corr_matrix.columns)):
            for index_row in range(index_col):
                if corr_matrix.iloc[index_col, index_row] >= threshold:
                    column_to_drop.add(corr_matrix.columns[index_col])
        return data.drop(column_to_drop, axis=1)

    def drop_na_and_constants_columns(self, data, threshold_na=0.5):
        set_drop = set()

        for column_name in data.columns:
            if self._check_na_rate_in_column(data[column_name], threshold_na):
                set_drop.add(column_name)
            if self._check_column_is_constant(data[column_name]):
                set_drop.add(column_name)

        return data.drop(set_drop, axis=1)

    @staticmethod
    def _check_na_rate_in_column(column, threshold):
        na_rate = column.isna().sum() / len(column)
        if na_rate >= threshold:
            return True
        return False

    @staticmethod
    def _check_column_is_constant(column):
        if len(list(column.value_counts())) <= 1:
            return True
        return False

    @staticmethod
    def get_modality_of_a_column(column):
        return list(pd.unique(column))

    # ROWS TREATMENT ############################################################################################

    @staticmethod
    def drop_duplicates_row(data):
        return data.drop_duplicates()

    #  TO TEST
    def drop_row_if_value_unwanted_in_a_column(self, data, column_name, set_value_unwanted):
        for value in self.get_modality_of_a_column(data[column_name]):
            if value in set_value_unwanted:
                data = data.drop([data[column_name] == value], axis=0)
        return data

    # TO TEST
    @staticmethod
    def drop_row_with_na(data, threshold=0.2):
        list_drop = []
        print(data.shape)
        for index in range(data.shape[0]):
            list_null = list(data.iloc[index].isnull())
            if (list_null.count(True) / len(list_null)) >= threshold:
                list_drop.append(index)

        data = data.drop(list_drop, axis=0)
        return data.reset_index(drop=True)


# NOT IN DEV / NOT USED ############################################################################################

class CleanDataSandBox:

    @staticmethod
    def read_csv(self, path_data, sep=','):
        try:
            return pd.read_csv(path_data, sep=sep)
        except Exception:  # define exception
            print(Exception)
        return None

    # pipeline for unsup,sup learning
    def clean_data_and_define_components(self, data, features_to_drop=None, y_name=None, ):

        if features_to_drop is not None:
            self.drop_features(data, features_to_drop)

        if y_name is not None:
            self.split_data_into_X_y(data, y_name)

    @staticmethod
    def drop_features(data, features_to_drop):
        if type(features_to_drop) in [str, int, float]:
            features_to_drop = [features_to_drop]

        for feature in features_to_drop:
            if feature in list(data.columns):
                data = data.drop(feature, axis=1)

    @staticmethod
    def split_data_into_X_y(data, y_name):
        try:
            y = data[[y_name]].values
            X = data.drop(y_name, axis=1)
            return X, y
        except KeyError as err:
            print(f'{y_name} not in column name --> \n{err}')

    @staticmethod
    def count_na_ratio_for_each_columns(data):
        dict_na = {}
        for column in data.columns:
            percent = round(data[column].isna().sum() / data.shape[0], 3)
            dict_na[column] = percent
        return dict_na

    @staticmethod
    def drop_row_that_contain_unwanted_values(data, column_name, list_unwanted_value):

        if type(list_unwanted_value) is str:
            list_unwanted_value = list(list_unwanted_value.split(sep=','))

        data_cleaned = data.copy()
        for value_unwanted in list_unwanted_value:
            lines_index_to_drop = data_cleaned[data_cleaned[column_name] == value_unwanted].index
            data_cleaned.drop(lines_index_to_drop, inplace=True)

        return data_cleaned
