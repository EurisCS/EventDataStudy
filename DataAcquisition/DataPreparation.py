import pandas as pd

class PrepareData:

    def __init__(self):
        pass

    #  EXTRACT ################################################################################################

    # extract relevant data and sort them into dict_of_list
    def extract_relevant_data_and_sort_it(self, raw_data, output_dict_df=False):

        dict_of_list_data = dict()

        for results in raw_data['hits']['hits']:  # the return of the query

            dict_data_system = results['_source']['details']['system']  # system info are relevant

            for system_name in list(dict_data_system.keys()):  # one key expected, the loop is for security code

                if system_name not in dict_of_list_data:  # add into the dict_final if no exist
                    dict_of_list_data[system_name] = list()

                extracted_data = self._recursive_sort_data(dict_data_system[system_name])  # extract data recursively
                dict_of_list_data[system_name].append(extracted_data)  # and append to dict_final

        if output_dict_df:
            return self.transform_list_data_to_dataframe(dict_of_list_data)

        return dict_of_list_data

    # goes back through dict of dict and create feature name foreach value found
    def _recursive_sort_data(self, current_object, name_feature=''):

        dict_result = dict()

        if type(current_object) is dict:
            for key, new_obj in current_object.items():
                dict_result.update(self._recursive_sort_data(new_obj, f'{name_feature}{key}_'))
                # update can delete field. in theory, not twice the same field
        else:
            dict_result[name_feature[:-1]] = current_object

        return dict_result

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
