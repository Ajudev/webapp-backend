from audioop import mul
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Search, Float, Q
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import core.models

# Create a connection to ElasticSearch
connections.create_connection()

# ElasticSearch "model" mapping out what fields to index


class ProductIndex(Document):
    title = Text()
    description = Text()
    category = Text()
    small_img = Text()
    rent_daily = Float()
    city = Text()
    street = Text()
    location = Text()
    created_at = Date()
    enable_status = Text()
    tags = Text(multi=True)

    class Index:
        name = 'product-index'

# Bulk indexing function, run in shell


def bulk_indexing():
    """
    Function which will index all of the records in Product model with elastic search
    """

    ProductIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing()
         for b in core.models.Product.objects.all().iterator()))

# Simple search function


def run_search(search_index: str, search_term: str):
    """
    Function which will query elastic search and return results matching the given search value throughout 
    the given index

    :param search_index: Index which needs to be searched
    :type search_index: str

    :param search_val: Search term which needs to be used to search the index
    :type search_val: str

    :return: List containing the results of the search for the given search term
    :rtype: `list`

    """
    query = Q("multi_match", query=search_term)
    search_command = Search(index=search_index).query(query)
    response = search_command.execute()
    return response.to_dict()['hits']['hits']
