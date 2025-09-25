"""
Example DAG that categorizes news articles using the llm decorator with structured output.
"""

from typing import Literal

import pendulum
try:
    from airflow.sdk import dag, task
except ImportError:
    from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException

import airflow_ai_sdk as ai_sdk


@task
def get_articles() -> list[dict]:
    """
    Return a small set of example news articles. In real usage, fetch from an API or database.
    """
    return [
        {
            "title": "Central bank signals potential rate cut in Q4",
            "body": "The central bank hinted that rate reductions may come later this year amid cooling inflation.",
        },
        {
            "title": "Championship final ends in dramatic penalty shootout",
            "body": "Fans were treated to a nail-biting finish as the underdogs clinched the title on penalties.",
        },
        {
            "title": "Tech giant unveils new AI chip for datacenters",
            "body": "The chip promises improved inference throughput and energy efficiency for enterprise workloads.",
        },
        {
            "title": "Blockbuster sequel tops weekend box office",
            "body": "The franchise returned to theaters with record-breaking ticket sales across major markets.",
        },
        {
            "title": "Senate advances bipartisan cybersecurity bill",
            "body": "Lawmakers moved forward with legislation aiming to bolster national cyber defenses.",
        },
    ]


class ArticleCategory(ai_sdk.BaseModel):
    category: Literal["politics", "technology", "sports", "finance", "entertainment", "other"]
    rationale: str


@task.llm(
    model="gpt-4o-mini",
    output_type=ArticleCategory,
    system_prompt=
    """
    You are a precise news desk editor. Classify the article into one category from this set:
    politics, technology, sports, finance, entertainment, other.

    Provide:
    - category: one of the allowed labels
    - rationale: one or two sentences explaining the choice

    Base your decision strictly on the provided title and body.
    """,
)
def categorize_article(article: dict | None = None) -> ArticleCategory:
    """
    Transform the article record into a concise prompt for the LLM.
    """
    if article is None:
        raise AirflowSkipException("No article provided")

    return f"Title: {article['title']}\nBody: {article['body']}"


@task
def publish_categories(categories: list[dict]):
    """
    Publish or store the categorized results. Here we simply print them.
    """
    from pprint import pprint
    pprint(categories)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=False,
)
def news_article_categorization():
    articles = get_articles()
    results = categorize_article.expand(article=articles)
    publish_categories(results)


dag = news_article_categorization()

