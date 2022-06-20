import pandas as pd


# Preparation = extraction + formatting
class ExtractData:

    def __init__(self, list_features_to_extract=None, output_type_in_dict_df=True):

        self.list_features_to_extract = list_features_to_extract

        self.output_type_in_dict_df = output_type_in_dict_df

    #  MAINS LIST FEATURES ###########################################################################################

    def extract_data_from_list_features(self, raw_data):

        lists_of_dict_data = list()

        # the return of the query. each result is a row of the final df.
        for results in raw_data['hits']['hits']:
            if self.list_features_to_extract is not None:
                lists_of_dict_data.append(self._extract_features_from_source(results['_source'],
                                                                             self.list_features_to_extract, {}))
        if self.output_type_in_dict_df:
            return pd.DataFrame(lists_of_dict_data)

        return lists_of_dict_data

    #  MAINS MODULES DATA && LIST FEATURES ##########################################################################

    # NEED_TO multiprocess it
    # extracts relevant data and sort them into dict_of_list
    def extract_relevant_modules_data_and_sort_it(self, raw_data):

        dict_lists_of_dict_data = dict()

        # the return of the query. each result is a row of the final df.
        for results in raw_data['hits']['hits']:

            relevant_name, relevant_data = self._select_relevant_data_from_details(results['_source']['details'])

            if relevant_name is not None:
                dict_extracted_data = self._develop_data_recursively_for_extraction(relevant_data)

                # extract wanted data like timestamp , hostname , source 	...
                if self.list_features_to_extract is not None:
                    dict_extracted_data = self._extract_features_from_source(results['_source'],
                                                                             self.list_features_to_extract,
                                                                             dict_extracted_data)

                # append current dict (row) to the good list
                dict_lists_of_dict_data = self._append_dict_row_to_corresponding_list(relevant_name,
                                                                                      dict_extracted_data,
                                                                                      dict_lists_of_dict_data)

        if self.output_type_in_dict_df:
            dict_df = self._transform_list_data_to_dataframe(dict_lists_of_dict_data)
            return dict_df

        return dict_lists_of_dict_data

    #  SORT INTO LISTS ################################################################################################

    # NEED TO ADD SOME VALUE KEYS :  the unique non generic function
    @staticmethod
    def _select_relevant_data_from_details(details_data):
        # on imagine qu'il y'a qu'une key à recover dans details
        list_key = details_data.keys()

        if 'system' in list_key:
            relevant_key = list(details_data['system'].keys())[0]
            return relevant_key, details_data['system'][relevant_key]

        if 'monitor' in list_key:
            pass

        if 'other' in list_key:
            pass

        return None, None

    #  EXTRACT ################################################################################################

    # goes back through dict of dict and create feature name foreach value found
    def _develop_data_recursively_for_extraction(self, current_dict, name_feature=''):

        dict_final = dict()

        if type(current_dict) is dict:
            for key, new_obj in current_dict.items():
                dict_final.update(self._develop_data_recursively_for_extraction(new_obj, f'{name_feature}{key}_'))
                # update can delete field. in theory, we don't have twice the same field
        else:
            dict_final[name_feature[:-1]] = current_dict

        return dict_final

    # extract wanted data like timestamp , hostname , source 	...
    @staticmethod
    def _extract_features_from_source(source_data, list_features_to_extract, dict_extracted_data):
        for feature in list_features_to_extract:
            dict_extracted_data[feature] = source_data[feature]
        return dict_extracted_data

    #  APPEND ################################################################################################

    @staticmethod
    def _append_dict_row_to_corresponding_list(relevant_name, dict_extracted_data, dict_lists_of_dict_data):

        if relevant_name not in dict_lists_of_dict_data:
            dict_lists_of_dict_data[relevant_name] = list()

        dict_lists_of_dict_data[relevant_name].append(dict_extracted_data)

        return dict_lists_of_dict_data

    # TRANSFORM ################################################################################################

    @staticmethod
    def _transform_list_data_to_dataframe(dict_of_list_data):
        dict_df = dict()

        for key, list_data in dict_of_list_data.items():
            dict_df[key] = pd.DataFrame(list_data)

        return dict_df

