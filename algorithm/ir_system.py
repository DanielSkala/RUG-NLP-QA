from abc import ABC
from algorithm.caching_strategy import CachingStrategy
from algorithm.answer_strategy import AnswerStrategy
from algorithm.models import Document


class IRSystem(ABC):

    def __init__(self,
                 caching_strategy: CachingStrategy,
                 answer_strategy: AnswerStrategy):
        self.caching_strategy = caching_strategy
        self.answer_strategy = answer_strategy

    def index_document(self, document: Document, *args, **kwargs):
        self.caching_strategy.cache(document)

    def find(self, doc_id: str, query: str, metadata: dict = None, *args, **kwargs) -> dict:
        entries = self.caching_strategy.find(doc_id, query, metadata)
        return {
            "resources": entries,
            "query": query,
            "answer": self.answer_strategy.formulate_answer(query, entries)
        }


class BookIRSystem(IRSystem):

    def __init__(self, caching_strategy, answer_strategy):
        super().__init__(caching_strategy, answer_strategy)
