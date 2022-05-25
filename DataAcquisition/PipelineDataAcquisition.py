from ElasticApi_6_8_2 import ElasticAPI
from DataPreparation import PrepareData
from DataManagement.PandasFrameManagement import ManageDataFrames

prepare = PrepareData()
data_manager = ManageDataFrames()


def pipeline_data_acquisition(host, port, index_cluster, path_json_query, out_path_data, extension_store, update_query):
    # connect to Elastic Cluster
    client = ElasticAPI(host, port)

    # get data and update query
    raw_data = client.get_raw_data_from_json_query_and_update_query(index_cluster, path_json_query, update_query)

    # sort and extract data
    dict_df = prepare.extract_relevant_data_and_sort_it(raw_data, output_dict_df=True)

    # update local data
    data_manager.append_dict_df_into_bdd(out_path_data, dict_df, extension_store)
