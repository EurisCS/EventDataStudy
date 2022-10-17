import pandas as pd


class PostTreatmentsDataFrame:

    def __init__(self, list_col_to_convert_to_datetime=None, list_col_for_sort_df=None,
                 list_col_to_set_index=None):

        if type(list_col_to_convert_to_datetime) is str:
            list_col_to_convert_to_datetime = [list_col_to_convert_to_datetime]
        self.list_col_to_convert_to_datetime = list_col_to_convert_to_datetime

        if type(list_col_for_sort_df) is str:
            list_col_for_sort_df = [list_col_for_sort_df]
        self.list_col_for_sort_df = list_col_for_sort_df

        if type(list_col_to_set_index) is str:
            list_col_to_set_index = [list_col_to_set_index]
        self.list_col_to_set_index = list_col_to_set_index

    # POST TREATMENT OPERATIONS : CONVERT TYPE COLUMNS AND SORT DF ####################################################

    def post_treatment_dict_dataframes(self, dict_df):

        for key in dict_df.keys():
            dict_df[key] = self.post_treatment_dataframe(dict_df[key])

        return dict_df

    def post_treatment_dataframe(self, df):

        # convert columns to datetime
        if self.list_col_to_convert_to_datetime is not None:
            df = self._convert_column_to_datetime(df)

        # sort df by a column
        if self.list_col_for_sort_df is not None:
            df = df.sort_values(by=self.list_col_for_sort_df, axis=0, inplace=False)

        # set index
        if self.list_col_to_set_index is not None:
            df = df.set_index(self.list_col_to_set_index, drop=True, inplace=False)

        return df

    def _convert_column_to_datetime(self, df):
        for column in self.list_col_to_convert_to_datetime:
            series_converted = pd.to_datetime(df[column])
            df = df.drop(column, axis=1)
            df = pd.concat([series_converted, df], axis=1)

        return df


class ConcatenateEventsAndAlerts:

    # CONCATENATE ALERTS LABELS FROM EVENTS ######################################################################

    # NEED TO ADD SOME OBSERVATIONS
    def concatenate_alerts_labels_from_observations(self, dict_df_events, df_alerts):

        for key in dict_df_events.keys():

            name_observation = None

            if key == 'cpu':
                name_observation = 'cpu_utilization'

            if key == 'fsstat':
                name_observation = None

            if key == 'network':
                name_observation = None

            if key == 'memory':
                name_observation = None

            dict_df_events[key] = self.concatenate_column_severity_to_event_data(dict_df_events[key], df_alerts,
                                                                                 name_observation)
        return dict_df_events

    @staticmethod
    def concatenate_column_severity_to_event_data(df_events, df_alerts, name_observation):

        if name_observation is not None:
            df_obs = df_alerts[df_alerts['observation'] == name_observation]

            # if no observation
            if df_obs.shape[0] == 0:
                df_events['severity'] = 'INFO'

            else:
                df_events = pd.concat([df_events, df_obs[['severity']]],
                                      axis=1, ignore_index=False)

            # not clean : look the doc for a better way to do that
            df_events['severity'] = df_events['severity'].fillna(method='ffill', inplace=False)
            df_events['severity'] = df_events['severity'].fillna(value='INFO', inplace=False)
        else:
            df_events['severity'] = 'INFO'

        return df_events
