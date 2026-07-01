from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:

    text: str
    reference: str
    book: str
    chapter: int
    start_verse: int
    end_verse: int

    @classmethod
    def from_document(cls, document: object) -> RetrievedChunk:
        raise NotImplementedError


class BibleRetriever:

    def __init__(self, top_k: int | None = None) -> None:
        raise NotImplementedError

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievedChunk]:
        raise NotImplementedError
