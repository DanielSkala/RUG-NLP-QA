from dataclasses import dataclass


@dataclass
class Document:
    id: str
    data: str


@dataclass
class TextEntry:
    id: str
    text: str
    metadata: dict


@dataclass
class EmbeddingEntry:
    id: str
    embedding: list
    metadata: dict
