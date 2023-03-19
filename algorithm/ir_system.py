from abc import ABC
from algorithm.caching_strategy import CachingStrategy
from algorithm.answer_strategy import AnswerStrategy
from algorithm.document_operator import DocumentOperator
from algorithm.models import Document


class IRSystem(ABC):

    def __init__(self,
                 caching_strategy: CachingStrategy,
                 answer_strategy: AnswerStrategy,
                 document_operator: DocumentOperator):
        self.caching_strategy = caching_strategy
        self.answer_strategy = answer_strategy
        self.document_operator = document_operator

    def index_document(self, document: Document, *args, **kwargs):
        parsed_obj = self.document_operator.parse(document.data, *args, **kwargs)
        text_entries = self.caching_strategy.cache(parsed_obj, *args, **kwargs)
        self.document_operator.store(text_entries, *args, **kwargs)

    def find(self, query: str, *args, **kwargs) -> str:
        entries = self.caching_strategy.find(query, *args, **kwargs)
        return self.answer_strategy.formulate_answer(query, entries, *args, **kwargs)


class BookIRSystem(IRSystem):

    def __init__(self, caching_strategy, answer_strategy, document_operator):
        super().__init__(caching_strategy, answer_strategy, document_operator)