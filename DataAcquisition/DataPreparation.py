import pandas as pd


# Preparation = extraction + formatting
class PrepareData:

    def __init__(self, list_features_to_extract=None, list_col_to_convert_to_datetime=None, list_col_to_sort_df=None,
                 output_type_in_dict_df=True):

        self.list_features_to_extract = list_features_to_extract  # utctimestamp
        self.list_col_to_convert_to_datetime = list_col_to_convert_to_datetime  # utctimestamp
        self.list_col_to_sort_df = list_col_to_sort_df  # utctimestamp

        self.output_type_in_dict_df = output_type_in_dict_df

    # extract relevant data and sort them into dict_of_list
    def INDEV_extract_relevant_system_data_and_sort_it(self, raw_data):

        dict_lists_of_dict_data = dict()

        # the return of the query. each result is a row of the final df.
        for results in raw_data['hits']['hits']:
            # multiprocess it

            relevant_name, relevant_data = self.INDEV_select_relevant_data_from_details(results['_source']['details'])

            if relevant_name is not None:
                dict_extracted_data = self._develop_data_recursively_for_extraction(relevant_data)

                # extract wanted data like timestamp , hostname , source 	...
                if self.list_features_to_extract is not None:
                    dict_extracted_data = self.INDEV_extract_features_from_source(results['_source'],
                                                                                  self.list_features_to_extract,
                                                                                  dict_extracted_data)

                # append current dict (row) to the good list
                dict_lists_of_dict_data = self.INDEV_append_dict_to_corresponding_list(relevant_name, dict_extracted_data,
                                                                                       dict_lists_of_dict_data)

        if self.output_type_in_dict_df:
            dict_df = self.transform_list_data_to_dataframe(dict_lists_of_dict_data)
            dict_df = self.INDEV_post_treatment_dataframes(dict_df)
            return dict_df

        return dict_lists_of_dict_data

    #  EXTRACT ################################################################################################

    # ADD SOME VALUE KEYS
    @staticmethod
    def INDEV_select_relevant_data_from_details(details_data):
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

    @staticmethod
    def INDEV_extract_features_from_source(source_data, list_features_to_extract, dict_extracted_data):
        for feature in list_features_to_extract:
            dict_extracted_data[feature] = source_data[feature]
        return dict_extracted_data

    def INDEV_extract_timestamp_from_source(self, source_data, dict_extracted_data, timestamp_name='utctimestamp'):
        return self.INDEV_extract_features_from_source(source_data, [timestamp_name], dict_extracted_data)

    @staticmethod
    def INDEV_append_dict_to_corresponding_list(relevant_name, dict_extracted_data, dict_lists_of_dict_data):

        if relevant_name not in dict_lists_of_dict_data:
            dict_lists_of_dict_data[relevant_name] = list()

        dict_lists_of_dict_data[relevant_name].append(dict_extracted_data)

        return dict_lists_of_dict_data

    # POST TREATMENT OPERATIONS #######################################################################################

    def INDEV_post_treatment_dataframes(self, dict_df):

        if type(self.list_col_to_convert_to_datetime) is str:
            self.list_col_to_convert_to_datetime = [self.list_col_to_convert_to_datetime]
        if type(self.list_col_to_sort_df) is str:
            self.list_col_to_sort_df = [self.list_col_to_sort_df]

        for key in dict_df.keys():

            # To datetime
            if self.list_col_to_convert_to_datetime is not None:
                dict_df[key] = self.convert_column_to_datetime(dict_df[key])

            # Sort Dfs
            if self.list_col_to_sort_df is not None:
                dict_df[key].sort_values(by=self.list_col_to_sort_df, axis=0, inplace=True)

        return dict_df

    def convert_column_to_datetime(self, df):
        for column in self.list_col_to_convert_to_datetime:
            series_converted = pd.to_datetime(df[column])
            df = df.drop(column, axis=1)
            df = pd.concat([series_converted, df], axis=1)

        return df

    #  EXTRACT ################################################################################################

    # extract relevant data and sort them into dict_of_list
    def extract_relevant_system_data_and_sort_it(self, raw_data, list_wanted_features=None,
                                                 type_output_in_dict_df=True):

        dict_of_list_dict_data = dict()

        # the return of the query. each result is a row of the final df.
        for results in raw_data['hits']['hits']:

            current_data = results['_source']

            # extract system data
            system_name, dict_extracted_data = self._extract_system_data(current_data['details']['system'])

            # extract wanted data like timestamp , hostname , source 	...
            if list_wanted_features:
                dict_extracted_data = \
                    self.extract_wanted_features(current_data, list_wanted_features, dict_extracted_data)

            # append current dict (row) to the good list
            if system_name not in dict_of_list_dict_data:
                dict_of_list_dict_data[system_name] = list()
            dict_of_list_dict_data[system_name].append(dict_extracted_data)

        if type_output_in_dict_df:
            return self.transform_list_data_to_dataframe(dict_of_list_dict_data)

        return dict_of_list_dict_data

    def _extract_system_data(self, dict_data_system):

        # only one increment expected. loop used for avoid unexpected mistake
        system_name = list(dict_data_system.keys())[0]

        # extract data recursively and append to dict_final
        dict_extracted_data = self._develop_data_recursively_for_extraction(dict_data_system[system_name])

        return system_name, dict_extracted_data

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

    @staticmethod
    def extract_wanted_features(current_data, list_wanted_features, dict_extracted_data):

        for wanted_feature in list_wanted_features:
            dict_extracted_data[wanted_feature] = current_data[wanted_feature]

        return dict_extracted_data

    #  TRANSFORM ################################################################################################

    @staticmethod
    def transform_list_data_to_dataframe(dict_of_list_data):
        dict_df = dict()

        for key, list_data in dict_of_list_data.items():
            dict_df[key] = pd.DataFrame(list_data)

        return dict_df

    @staticmethod
    def NOT_ENDED_transform_list_data_to_spark_frame(dict_of_list_data):
        dict_df = dict()

        for key, list_data in dict_of_list_data.items():
            dict_df[key] = 'here the pyspark_frame from list_data'

        return dict_df


# U_TEST ################################################################################################

class SHIT:

    def unit_test_sort_memory_data(self, df):
        new_df = pd.Dataframe()
        for row in df:
            field_total = {'total': row['total']}

            used = {'used_pct': row['used']['pct'],
                    'used_bytes': row['used']['pct']}

            actual = {'actual_free': row['actual']['free'],
                      'actual_used_pct': row['actual']['used']['pct'],
                      'actual_used_bytes': row['actual']['free']['bytes']}

            page_stats = {
                'page_stats_pgsteal_direct_pages': row['page_stats']['pgsteal_direct']['pages'],
                'page_stats_pgsteal_kswapd_pages': row['page_stats']['pgsteal_kswapd']['pages'],

                'page_stats_pgscan_direct_pages': row['page_stats']['pgscan_direct']['pages'],
                'page_stats_pgscan_kswapd_pages': row['page_stats']['pgscan_kswapd']['pages'],

                'page_stats_pgfree_pages': row['page_stats']['pgfree']['pages'],

                'page_stats_direct_efficiency_pct': row['page_stats']['direct_efficiency']['pct'],
                'page_stats_kswapd_efficiency_pct': row['page_stats']['kswapd_efficiency']['pct']
            }

            swap = {
                'swap_in_page': row['swap']['in']['pages'],
                'swap_out_pages': row['swap']['out']['pages'],

                'swap_readahead_pages': row['swap']['readahead']['pages'],
                'swap_readahead_cached': row['swap']['readahead']['cached'],

                'swap_used_pct': row['swap']['used']['pct'],
                'swap_used_bytes': row['swap']['used']['bytes'],

                'swap_total': row['swap']['total'],
                'swap_free': row['swap']['free']
            }

            free = {'free': row['free']}

            hugepages = {
                'hugepages_swap_out_pages': row['hugepages']['swap_out']['pages'],
                'hugepages_swap_out_fallback': row['hugepages']['swap_out']['fallback'],
                'hugepages_total': row['hugepages']['total'],
                'hugepages_used_pct': row['hugepages']['used']['pct'],
                'hugepages_used_bytes': row['hugepages']['used']['bytes'],
                'hugepages_default_size': row['hugepages']['default_size'],
                'hugepages_free': row['hugepages']['free'],
                'hugepages_surplus': row['hugepages']['surplus'],
                'hugepages_reserved': row['hugepages']['reserved'],

            }

    def sort_cpu_data(self, df):
        pass

    def sort_fsstat_data(self, df):
        pass

    def sort_network_data(self, df):
        pass

    '''
     - cpu  # CPU usage
    - memory  # Memory usage
    - network  # Network IO
    - fsstat  # File system summary metrics
    '''

    #    - load            # CPU load averages

    #    - process         # Per process metrics
    #    - process_summary # Process summary
    #    - uptime          # System Uptime
    #    - socket_summary  # Socket summary
    #    - core           # Per CPU core usage
    #    - diskio         # Disk IO
    #    - filesystem     # File system usage for each mountpoint

    #    - raid           # Raid
    #    - socket         # Sockets and connection info (linux only)

    # ################################################################################################
