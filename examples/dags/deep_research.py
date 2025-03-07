"""
This shows how to use the SDK to build a deep research agent.
"""

import pendulum
import requests
from airflow.decorators import dag, task
from airflow.models.dagrun import DagRun
from airflow.models.param import Param
from bs4 import BeautifulSoup
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool


async def get_page_content(url: str) -> str:
    """
    Get the content of a page.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    distillation_agent = Agent(
        "gpt-4o-mini",
        system_prompt="""
        You are responsible for distilling information from a text. The summary will be used by a research agent to generate a research report.

        Keep the summary concise and to the point, focusing on only key information.
        """,
    )

    return await distillation_agent.run(soup.get_text())

deep_research_agent = Agent(
    "o3-mini",
    system_prompt="""
    You are a deep research agent who is very skilled at distilling information from the web. You are given a query and your job is to generate a research report.

    You can search the web by using the `duckduckgo_search_tool`. You can also use the `get_page_content` tool to get the contents of a page.

    Keep going until you have enough information to generate a research report. Assume you know nothing about the query or contents, so you need to search the web for relevant information.

    Find at least 8-10 sources to include in the research report. If you run out of sources, keep searching the web for more information with variations of the question.

    Do not use quotes in your search queries.

    Do not generate new information, only distill information from the web. If you want to cite a source, make sure you fetch the full contents because the summary may not be enough.
    """,
    tools=[duckduckgo_search_tool(), get_page_content],
)

@task.agent(agent=deep_research_agent)
def deep_research_task(dag_run: DagRun) -> str:
    """
    This task performs a deep research on the given query.
    """
    query = dag_run.conf.get("query")

    if not query:
        raise ValueError("Query is required")

    print(f"Performing deep research on {query}")

    return query


@task
def upload_results(results: str):
    print("Uploading results")
    print("-" * 100)
    print(results)
    print("-" * 100)

@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=False,
    params={
        "query": Param(
            type="string",
            default="How has the field of data engineering evolved in the last 5 years?",
        ),
    },
)
def deep_research():
    results = deep_research_task()
    upload_results(results)

dag = deep_research()

if __name__ == "__main__":
    dag.test(run_conf={"query": "How has the field of data engineering evolved in the last 5 years?"})
