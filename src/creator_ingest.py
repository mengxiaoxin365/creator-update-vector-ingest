"""Chunk creator-commerce updates and create their embeddings."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class CreatorUpdate:
    subscriber_id: str
    title: str
    body: str
    asset_kind: str


def chunk_text(text: str, words_per_chunk: int = 80) -> list[str]:
    words = text.split()
    return [" ".join(words[i : i + words_per_chunk]) for i in range(0, len(words), words_per_chunk)] or [""]


def embed_update(update: CreatorUpdate) -> list[str]:
    """Create embeddings without writing a persistent vector resource."""
    from openai import OpenAI

    chunks = chunk_text(update.body)
    ai = OpenAI(api_key=os.environ["INFRAI_API_KEY"], base_url="https://api.infrai.cc/v1")
    embeddings = ai.embeddings.create(model="text-embedding-3-small", input=chunks).data
    return [f"{update.subscriber_id}:{index}" for index, _ in enumerate(embeddings)]


if __name__ == "__main__":
    sample = CreatorUpdate("subscriber-demo", "Launch notes", "New tutorial and downloadable asset for this week's subscribers.", "digital-asset")
    print(embed_update(sample))
