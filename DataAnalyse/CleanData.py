import pandas as pd


class CleanData:

    def __init__(self):
        self.toolbox = CleanDataToolBox()

    def drop_bad_row_and_columns(self, data, threshold_na_column, threshold_na_row):

        # drop columns by checking Nan & constants
        data = self.toolbox.delete_bad_columns(data, threshold_na_column)

        data = self.toolbox.drop_duplicates_row(data)  # drop duplicates rows

        data = self.toolbox.drop_row_with_na(data, threshold_na_row)  # drop rows by checking Nan

        return data


class CleanDataToolBox:

    # COLUMNS TREATMENT ############################################################################################

    def delete_bad_columns(self, data, threshold_na=0.5):
        set_drop = set()

        for column_name in data.columns:
            if self.check_na_rate_in_column(data[column_name], threshold_na):
                set_drop.add(column_name)
            if self.check_column_is_constant(data[column_name]):
                set_drop.add(column_name)

        return data.drop(set_drop, axis=1)

    @staticmethod
    def check_na_rate_in_column(column, threshold):
        na_rate = column.isna().sum() / len(column)
        if na_rate >= threshold:
            return True
        return False

    @staticmethod
    def check_column_is_constant(column):
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
    def drop_row_with_na(self, data, threshold=0.2):
        list_drop = []
        for index in range(data.shape[0]):
            list_values = list(data.loc[index])
            if list_values.count(None) / len(list_values) >= threshold:
                list_drop.append(index)

        return data.drop(list_drop, axis=0)


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
            lines_index_to_drop = df[df[column_name] == value_unwanted].index
            data_cleaned.drop(lines_index_to_drop, inplace=True)

        return data_cleaned


#######################
# test main
path = "/DataStorage/Results/analyzer-events-202106_alert_query.csv"
df = pd.read_csv(path)
print(df.head())
list_unwanted_values = ['1gCdv3wBalp6tMCodniH', 'hQCpv3wBalp6tMCoXXnW']

data_clean = PrepareData().drop_row_that_contain_unwanted_values(df, 'alert_id', list_unwanted_values)

if data_clean.shape[0] == df.shape[0] - 2:
    print(True)
else:
    print(False)
