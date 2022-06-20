import pandas as pd
from Utilities.FileManipulation import check_extension, get_name_file_into_path, get_extension_into_path,\
    get_path_without_extension, create_directory

import os


class ManageDataFrames:
    """ Manage : store, load, concatenate dataframes """

    # MAIN FUNCTION ################################################################################################

    def INDEV__append_dict_df_into_storage(self, path_df_stored, dict_df_to_concatenate, extension='pickle'):

        create_directory(path_df_stored)

        dict_df_stored = self.load_dict_df(path_df_stored)

        dict_df_to_save = self.concatenate_dict_dfs_and_drop_duplicates_rows(dict_df_stored, dict_df_to_concatenate)

        self.store_dict_df_into_directory(dict_df_to_save, path_df_stored, extension=extension)



    # CONCATENATE ################################################################################################

    def concatenate_dict_dfs_and_drop_duplicates_rows(self, dict_df_1, dict_df_2):
        for key in dict_df_2:
            if key in dict_df_1.keys():
                dict_df_1[key] = self.concatenate_dfs(dict_df_1[key], dict_df_2[key])
            else:
                dict_df_1[key] = dict_df_2[key]

            # drop duplicates row
            dict_df_1[key].drop_duplicates(inplace=True)

        return dict_df_1

    @staticmethod
    def concatenate_dfs(df1, df2,  axis=0, ignore_index=False):
        return pd.concat([df1, df2], axis=axis, ignore_index=ignore_index)

    # STORE ################################################################################################

    def store_dict_df_into_directory(self, dict_df, save_path_directory, extension, save_index_as_column=True):

        create_directory(save_path_directory)

        for name_df in dict_df.keys():
            self.store_df(dict_df[name_df], f'{save_path_directory}/{name_df}', extension, save_index_as_column)

    def store_df(self, df_to_store, save_path_file, extension=None, save_index_as_column=True):

        if extension is None:
            extension = get_extension_into_path(save_path_file)
        save_path_file = get_path_without_extension(save_path_file)

        if extension in ['csv', '.csv']:
            self._store_df_into_csv(df_to_store, save_path_file, save_index_as_column)
        elif extension in ['pickle', '.pickle']:
            self._store_df_into_pickle(df_to_store, save_path_file)

    @staticmethod
    def _store_df_into_csv(df_to_store, save_path, save_index_as_column=True):
        try:
            df_to_store.to_csv(f'{save_path}.csv', index=save_index_as_column)
        except Exception as err:  # precisez l'exception
            return str(err)

    @staticmethod
    def _store_df_into_pickle(df_to_store, save_path, compression="infer", protocol=5):
        try:
            df_to_store.to_pickle(f'{save_path}.pickle', compression, protocol)
        except Exception as err:  # precisez l'exception
            return str(err)

    # LOAD ################################################################################################

    def load_dict_df(self, path_directory):

        dict_df = dict()

        for name_file in os.listdir(path_directory):

            if check_extension(name_file, extension_without_the_dot='pickle'):
                dict_df[get_name_file_into_path(name_file)] = self.load_df_pickle(f'{path_directory}/{name_file}')

            elif check_extension(name_file, extension_without_the_dot='csv'):
                dict_df[get_name_file_into_path(name_file)] = self.load_df_csv(f'{path_directory}/{name_file}')

        return dict_df

    @staticmethod
    def load_df_pickle(path_df):
        return pd.read_pickle(path_df)

    @staticmethod
    def load_df_csv(path_df):
        return pd.read_csv(path_df)
