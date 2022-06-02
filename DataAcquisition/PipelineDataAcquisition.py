from ElasticApi_6_8_2 import ElasticAPI
from DataPreparation import PrepareData
from DataManagement.PandasFrameManagement import ManageDataFrames

prepare = PrepareData()
data_manager = ManageDataFrames()


def pipeline_data_acquisition(host, port, index_cluster, path_json_query, list_features_to_extract,
                              list_col_to_convert_to_datetime, list_col_to_sort_df,out_path_data, extension_store, update_query):
    """
        - connect to Elastic Cluster
        - get data and update query
        - sort and extract system data
        - update local dataFrame
    """

    preparator = PrepareData(list_features_to_extract, list_col_to_convert_to_datetime, list_col_to_sort_df,True)

    # connect to Elastic Cluster
    client = ElasticAPI(host, port)

    # get data and update query
    raw_data = client.get_raw_data_from_json_query_and_update_query(index_cluster, path_json_query, update_query)


    '''
    # sort and extract data
    dict_df = prepare.extract_relevant_system_data_and_sort_it(raw_data, list_features_to_extract,
                                                               type_output_in_dict_df=True)
    '''


    # sort and extract data
    dict_df = preparator.INDEV_extract_relevant_system_data_and_sort_it(raw_data)


    # update local dataFrame
    data_manager.append_dict_df_into_bdd(out_path_data, dict_df, extension_store)
