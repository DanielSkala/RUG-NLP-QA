from abc import ABC, abstractmethod
from algorithm.models import TextEntry


class AnswerStrategy(ABC):

    @abstractmethod
    def formulate_answer(self, query: str, entries: [TextEntry], *args, **kwargs) -> str:
        pass
