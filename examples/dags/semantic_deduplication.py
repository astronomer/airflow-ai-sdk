"""
Example DAG that performs semantic deduplication using embeddings.
"""

import math
from typing import Iterable

import pendulum
try:
    from airflow.sdk import dag, task
except ImportError:
    from airflow.decorators import dag, task


@task
def get_records() -> list[str]:
    """
    Return example records containing near-duplicate sentences.
    """
    return [
        "The quick brown fox jumps over the lazy dog",
        "A fast brown fox leaps over a sleepy dog",
        "The weather is beautiful today",
        "It is a beautiful day today",
        "An unrelated sentence about databases",
    ]


@task.embed(
    model_name="all-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)
def embed_record(text: str) -> list[float]:
    # The decorator will return the vector; we simply pass through the text
    return text


def cosine_similarity(vec_a: Iterable[float], vec_b: Iterable[float]) -> float:
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for a, b in zip(vec_a, vec_b):
        dot += a * b
        norm_a += a * a
        norm_b += b * b
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / math.sqrt(norm_a * norm_b)


@task
def deduplicate(originals: list[str], vectors: list[list[float]], threshold: float = 0.9) -> list[dict]:
    """
    Simple semantic deduplication via cosine similarity thresholding.
    Returns canonical records and groups of duplicates.
    """
    kept: list[dict] = []
    used = set()
    for i, vec_i in enumerate(vectors):
        if i in used:
            continue
        group = [originals[i]]
        used.add(i)
        for j in range(i + 1, len(vectors)):
            if j in used:
                continue
            sim = cosine_similarity(vec_i, vectors[j])
            if sim >= threshold:
                group.append(originals[j])
                used.add(j)
        kept.append({"canonical": originals[i], "group": group})
    return kept


@task
def publish(groups: list[dict]):
    from pprint import pprint
    pprint(groups)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=False,
)
def semantic_deduplication():
    records = get_records()
    vectors = embed_record.expand(text=records)
    groups = deduplicate(records, vectors)
    publish(groups)


dag = semantic_deduplication()

