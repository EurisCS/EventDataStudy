from ElasticApi_6_8_2 import ElasticAPI
from DataExtraction import ExtractData
from DataPreparation import PostTreatmentsDataFrame, ConcatenateEventsAndAlerts
from DataManagement.ManagementDataFramesPandas import ManageDataFrames


class PipelineDataAcquisition:

    def __init__(self, host, port, out_path_data, extension_store, update_query):

        # connect to Elastic Cluster
        self.client = ElasticAPI(host, port)

        self.out_path_data = out_path_data
        self.extension_store = extension_store
        self.update_query = update_query

        self.prepare = ExtractData()
        self.data_manager = ManageDataFrames()

        self.save_index_as_column = False
        # MAIN PIPELINE ################################################################################################

    def get_data_from_events_and_alerts_and_store_datas(self, index_events, path_json_query_events,
                                                        list_features_to_extract_in_events=None, index_alerts=None,
                                                        path_json_query_alerts=None,
                                                        list_features_to_extract_in_alerts=None, timestamp_column=None,
                                                        alerts_in_labels=False, path_store_alerts=None):
        if timestamp_column is not None:
            self.save_index_as_column = True

        dict_df_events = self.get_data_from_events(index_events, path_json_query_events,
                                                   list_features_to_extract_in_events, timestamp_column)

        if None not in [index_alerts, path_json_query_alerts]:
            df_alerts = self.get_data_from_alerts(index_alerts, path_json_query_alerts,
                                                  list_features_to_extract_in_alerts, timestamp_column)

            if alerts_in_labels:
                dict_df_events = ConcatenateEventsAndAlerts().\
                    concatenate_alerts_labels_from_observations(dict_df_events, df_alerts)

            # update local dataFrame
            if path_store_alerts is not None:
                self.data_manager.store_df(df_alerts, f'{path_store_alerts}/alerts', self.extension_store,
                                           self.save_index_as_column)

        # update local dataFrame
        self.data_manager.store_dict_df_into_directory(dict_df_events, f'{self.out_path_data}', self.extension_store,
                                                       self.save_index_as_column)

    # EVENTS ################################################################################################

    def get_data_from_events(self, index_cluster, path_json_query, list_features_to_extract=None,
                             timestamp_column=None):

        # recover timestamp : converting easier interface to real class interface
        list_features_to_extract, list_col_to_convert_to_datetime, list_col_to_sort_df, list_col_to_set_index \
            = self.setup_timestamp_to_list_treatments(timestamp_column, list_features_to_extract)

        # get data and update query
        raw_data = self.client.get_raw_data_from_json_query_and_update_query(index_cluster, path_json_query,
                                                                             update_query=self.update_query)
        # sort and extract data : create object and apply function
        dict_df = ExtractData(list_features_to_extract, True).extract_relevant_modules_data_and_sort_it(raw_data)

        # some conversions on the columns
        dict_df = PostTreatmentsDataFrame(list_col_to_convert_to_datetime, list_col_to_sort_df,
                                          list_col_to_set_index).post_treatment_dict_dataframes(dict_df)

        return dict_df

    # ALERTS ################################################################################################

    def get_data_from_alerts(self, index_cluster, path_json_query, list_features_to_extract, timestamp_column):

        # recover timestamp : converting easier interface to real class interface
        list_features_to_extract, list_col_to_convert_to_datetime, list_col_to_sort_df, list_col_to_set_index \
            = self.setup_timestamp_to_list_treatments(timestamp_column, list_features_to_extract)

        for feature in ['severity', 'observation']:
            if feature not in list_features_to_extract:
                list_features_to_extract.append(feature)

        # get data and update query
        raw_data = self.client.get_raw_data_from_json_query_and_update_query(index_cluster, path_json_query,
                                                                             update_query=self.update_query)

        # sort and extract data
        df_alerts = ExtractData(list_features_to_extract, True).extract_data_from_list_features(raw_data)

        # some conversions on the columns
        df_alerts = PostTreatmentsDataFrame(list_col_to_convert_to_datetime, list_col_to_sort_df,
                                            list_col_to_set_index).post_treatment_dataframe(df_alerts)

        return df_alerts

    # SETUP TIMESTAMP #############################################################################################

    @staticmethod
    def setup_timestamp_to_list_treatments(timestamp_column, list_features_to_extract):

        if list_features_to_extract is None:
            list_features_to_extract = []
        list_col_to_convert_to_datetime, list_col_to_sort_df, list_col_to_set_index = [], [], []

        if timestamp_column is not None:
            list_features_to_extract.append(timestamp_column)
            list_col_to_convert_to_datetime.append(timestamp_column)
            list_col_to_sort_df.append(timestamp_column)
            list_col_to_set_index.append(timestamp_column)

        return list_features_to_extract, list_col_to_convert_to_datetime, list_col_to_sort_df, list_col_to_set_index
