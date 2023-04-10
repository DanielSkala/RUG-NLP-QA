from abc import ABC, abstractmethod
from algorithm.models import Document
from datasets import load_dataset
from tqdm import tqdm


class DocumentOperator(ABC):
    @abstractmethod
    def parse(self, document, *args, **kwargs) -> any:
        pass


class PDFDocumentOperator(DocumentOperator):
    def parse(self, document, *args, **kwargs) -> any:
        paragraphs_dataset = load_dataset("GroNLP/ik-nlp-22_slp", 'paragraphs')
        
        text = paragraphs_dataset['train']['text']
        return text


if __name__ == '__main__':
    operator = PDFDocumentOperator()
    doc = Document(
        id='1',
        data='../Project plan.pdf'
    )
    text = operator.parse(doc)
