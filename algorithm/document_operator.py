from abc import ABC, abstractmethod
from algorithm.models import Document
from datasets import load_dataset
from tqdm import tqdm
from PyPDF2 import PdfReader


class DocumentOperator(ABC):
    @abstractmethod
    def parse(self, document, *args, **kwargs) -> any:
        pass


class PDFDocumentOperator(DocumentOperator):
    def parse(self, document, *args, **kwargs) -> any:
        path = document.data
        # print(path)
        reader = PdfReader(path)  # path / ../'Project plan.pdf'
        text = [page.extract_text() for page in tqdm(reader.pages)]
        return text


class NLPDocumentOperator(DocumentOperator):
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
