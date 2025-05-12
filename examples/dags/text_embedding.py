"""
Example DAG that demonstrates how to use the @task.embed decorator to create vector embeddings.
"""

import pendulum

from airflow.decorators import dag, task

@task
def get_texts() -> list[str]:
    """
    This task returns a list of texts to embed. In a real workflow, this
    task would get the texts from a database or API.
    """
    return [
        "The quick brown fox jumps over the lazy dog",
        "A fast orange fox leaps over a sleepy canine",
        "The weather is beautiful today",
    ]

@task.embed(
    model_name="all-MiniLM-L12-v2",  # default model
    encode_kwargs={"normalize_embeddings": True}  # optional kwargs for the encode method
)
def create_embeddings(text: str) -> list[float]:
    """
    This task creates embeddings for the given text. The decorator handles
    the model initialization and encoding.
    """
    return text

@task
def store_embeddings(embeddings: list[list[float]]):
    """
    This task stores the embeddings. In a real workflow, this task would
    store the embeddings in a vector database.
    """
    print(f"Storing {len(embeddings)} embeddings")

@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
)
def text_embedding():
    texts = get_texts()
    embeddings = create_embeddings.expand(text=texts)
    store_embeddings(embeddings)

text_embedding()
