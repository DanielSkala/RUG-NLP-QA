from algorithm.emb_factory import ESEmbeddingFactory
from algorithm.models import EmbeddingEntry

es_client_params = {
    "hosts": "http://localhost:9200",
    "timeout": 30,
}


class TestESEmbeddingFactory:
    def test_create_index_if_not_exists(self):
        index_name = "test_index"
        embedding_size = 128
        es_embedding_factory = ESEmbeddingFactory(es_client_params, index_name, embedding_size)
        assert es_embedding_factory.es_client.indices.exists(index=index_name)

    def test_store(self):
        # generate random embedding entries
        embedding_entries = []
        for i in range(10):
            embedding_entries.append(EmbeddingEntry(str(i), [i for _ in range(128)], {}))

        index_name = "test_index"
        embedding_size = 128
        es_embedding_factory = ESEmbeddingFactory(es_client_params, index_name, embedding_size)
        es_embedding_factory.store(embedding_entries)
        assert es_embedding_factory.es_client.count(index=index_name)["count"] == 10

    def test_retrieve(self):
        # create two vectors with cosine similarity 1
        embedding_entries = [
            EmbeddingEntry("0", [1 for _ in range(128)], {}),
            EmbeddingEntry("1", [1 for _ in range(128)], {}),
        ]
        index_name = "test_index"
        embedding_size = 128
        es_embedding_factory = ESEmbeddingFactory(es_client_params, index_name, embedding_size)
        es_embedding_factory.store(embedding_entries)
        retrieved_embedding_entries = es_embedding_factory.retrieve([1 for _ in range(128)])
        assert len(retrieved_embedding_entries) == 2
        assert retrieved_embedding_entries[0].id == "0"
        assert retrieved_embedding_entries[1].id == "1"
        assert retrieved_embedding_entries[0].embedding == [1 for _ in range(128)]
        assert retrieved_embedding_entries[1].embedding == [1 for _ in range(128)]
        assert retrieved_embedding_entries[0].metadata == {}
        assert retrieved_embedding_entries[1].metadata == {}


if __name__ == "__main__":
    test = TestESEmbeddingFactory()
    test.test_create_index_if_not_exists()
    test.test_store()
    test.test_retrieve()
