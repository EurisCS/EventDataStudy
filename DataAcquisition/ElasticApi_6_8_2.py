from elasticsearch6 import Elasticsearch
from Utilities.JsonFunctions import load_json_file, store_json_file
from datetime import datetime


class ElasticAPI:

    def __init__(self, host='localhost', port=9200):
        try:
            self.client = Elasticsearch(f'{host}:{port}')
        except ConnectionError:  # check the except
            self.client = None

    # SOME UTILITIES AND GETTING-INFO WITH ELASTIC CLUSTER  ####################################################

    def __enter__(self):
        return self

    def __exit__(self):
        pass

    def get_info_cluster(self):
        pass

    # QUERY EXECUTE  ################################################################################################

    def get_raw_data_from_json_query_and_update_query(self, index, path_json_query, update_query=True):
        str_json_query = load_json_file(path_json_query)

        print(f'type json query : {str_json_query}')

        raw_data = self.client.search(index=index, body=str_json_query)

        if update_query:
            self.update_json_query_from_now(str_json_query, path_json_query)

        return raw_data

    def get_raw_data_from_json_query(self, index, path_json_query):
        str_json_query = load_json_file(path_json_query)
        return self.client.search(index=index, body=str_json_query)

    # QUERY UPDATE ################################################################################################

    # A TESTER
    @staticmethod
    def update_json_query_from_now(json_query, save_path_query, elastic_utc_format="%Y-%m-%dT%H:%M:%S.%f"):

        if not 'must' in json_query['query']['bool'].keys():
            json_query['query']['bool']['must'] = []

        time_actualised = f'{datetime.now().strftime(elastic_utc_format)}+00:00'
        created = False

        # if (range in utctimestamp) already exist in the query then modify it
        for request in json_query['query']['bool']['must']:
            if type(request) is dict:
                if 'range' in request.keys():
                    if 'utctimestamp' in request['range'].keys():
                        request['range']['utctimestamp'] = {"gt": time_actualised}
                        created = True
                        break

        # else create it
        if not created:
            json_query['query']['bool']['must'].append({'range': {'utctimestamp': {'gt': time_actualised}}})

        # save it
        store_json_file(json_query, save_path_query)
