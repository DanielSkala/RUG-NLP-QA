from abc import ABC, abstractmethod
from algorithm.models import EmbeddingEntry
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class EmbeddingFactory(ABC):

    @abstractmethod
    def store(self, embeddings: [EmbeddingEntry], *args, **kwargs):
        pass

    @abstractmethod
    def retrieve(self, embedding: [float], metadata: dict, *args, **kwargs) -> [EmbeddingEntry]:
        pass


class ESEmbeddingFactory(EmbeddingFactory):

    def __init__(self,
                 es_client_params: dict,
                 index_name,
                 embedding_size):
        self.es_client = Elasticsearch(**es_client_params)
        self.index_name = index_name
        self.embedding_size = embedding_size
        self.__create_index_if_not_exists()

    def destruct(self):
        self.es_client.indices.delete(index=self.index_name)

    def clear(self):
        self.destruct()
        self.__create_index_if_not_exists()

    def __create_index_if_not_exists(self):
        if self.es_client.indices.exists(index=self.index_name):
            return
        self.es_client.indices.create(index=self.index_name)
        self.es_client.indices.put_mapping(index=self.index_name, body={
            "properties": {
                "embedding": {
                    "type": "dense_vector",
                    "dims": self.embedding_size,
                },
                "metadata": {
                    "type": "object",
                },
            },
        })

    def store(self, embeddings: [EmbeddingEntry], refresh=False, *args, **kwargs):
        actions = [
            {
                "_index": self.index_name,
                "_id": embedding_entry.id,
                "_source": {
                    "embedding": embedding_entry.embedding,
                    "metadata": embedding_entry.metadata,
                },
            }
            for embedding_entry in embeddings]
        bulk(self.es_client, actions, refresh=refresh)

    def retrieve(self, embedding: [float], metadata: dict = None, *args, **kwargs) -> [EmbeddingEntry]:
        # fast retrieval and sort by score
        query = {
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {},
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {
                            "query_vector": embedding,
                        },
                    },
                },
            },
            "size": 10,
        }
        if metadata is not None:
            query["query"]["script_score"]["query"] = {
                "match": {
                    "metadata": metadata,
                },
            }
        response = self.es_client.search(index=self.index_name, body=query)
        return [
            EmbeddingEntry(
                hit["_id"],
                hit["_source"]["embedding"],
                hit["_source"]["metadata"],
            )
            for hit in response["hits"]["hits"]
        ]