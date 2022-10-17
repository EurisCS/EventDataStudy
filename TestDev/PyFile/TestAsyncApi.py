import asyncio
from elasticsearch6 import Elasticsearch as E6
# from elasticsearch import AsyncElasticsearch, Elasticsearch
from Utilities.JsonFunctions import load_json_file


class ElasticAPI:

    def __init__(self, host='localhost', port=9200):
        self.client = E6(hosts=host, port=port)

        # self.client = Elasticsearch(f"{host}:{port}", api_key=("id", "api_key"))

    async def async_search(self, index, query, size=1000):
        resp = await self.client.search(
            index=index,
            query=query,
            size=size,
        )
        print(resp)

    def search_6(self, index, body_query,from_=0, size=10000):
        return self.client.search(index=index, body=body_query ,from_=from_ , size=size)

    def search(self, index, query, size=1000):
        resp = self.client.search(
            index=index,
            query=query,
            size=size,
            from_ =1000,
        )
        return resp

    def get_raw_data_from_json_query_and_update_query(self, index, path_json_query):
        str_json_query = load_json_file(path_json_query)

        raw_data = self.client.search(index=index, body=str_json_query)

        return raw_data


from DataAcquisition.DataExtraction import ExtractData



def main():
    # loop = asyncio.get_event_loop()

    index = "events-20220502"
    query = load_json_file('/home/eguimard/PycharmProjects/DataStudy/DataStorage/JsonQuery/CPUWarningCriticalVM2.json')

    raw_data = ElasticAPI().search_6(index, query,from_=0, size=1000)

    dict_df = ExtractData().extract_relevant_modules_data_and_sort_it(raw_data)

    for key in dict_df.keys():
        print(dict_df[key].head())
        print('\n')

    for key in dict_df.keys():
        print(f'{key} : ')
        print(dict_df[key].shape)

if __name__ == '__main__':
    main()
