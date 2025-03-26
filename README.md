# airflow-ai-sdk

This repository contains an SDK for working with LLMs from Apache Airflow, based on [Pydantic AI](https://ai.pydantic.dev). It allows users to call LLMs and orchestrate agent calls directly within their Airflow pipelines using decorator-based tasks. The SDK leverages the familiar Airflow `@task` syntax with extensions like `@task.llm`, `@task.llm_branch`, and `@task.agent`.

To get started, check out the [examples repository here](https://github.com/astronomer/ai-sdk-examples), which offers a full local Airflow instance with the AI SDK installed and 5 example pipelines. If you already have Airflow running, you can also install the package with any optional dependencies you need:

```bash
pip install airflow-ai-sdk[openai,duckduckgo]
```

Note that installing the package with no optional dependencies will install the slim version of the package, which does not include any LLM models or tools. The available optional packages are listed [here](https://github.com/astronomer/airflow-ai-sdk/blob/main/pyproject.toml#L17). While this SDK offers the optional dependencies for convenience sake, you can also install the optional dependencies from [Pydantic AI](https://ai.pydantic.dev/install/) directly.

Table of Contents:

- [Features](#features)
- [Motivation](#motivation)
- [Examples](#examples)
  - [LLM calls from a DAG (summarize Airflow's commits)](#llm-calls-from-a-dag-summarize-airflow-s-commits)
  - [LLM calls with structured outputs using `@task.llm` (user feedback -> sentiment and feature requests)](#llm-calls-with-structured-outputs-using-taskllm-user-feedback---sentiment-and-feature-requests)
  - [Agent calls with `@task.agent` (deep research agent)](#agent-calls-with-taskagent-deep-research-agent)
  - [Changing dag control flow with `@task.llm_branch` (support ticket routing)](#changing-dag-control-flow-with-taskllmbranch-support-ticket-routing)
- [Future Work](#future-work)

## Features

- **LLM tasks with `@task.llm`:** Define tasks that call language models (e.g. GPT-3.5-turbo) to process text.
- **Agent tasks with `@task.agent`:** Orchestrate multi-step AI reasoning by leveraging custom tools.
- **Automatic output parsing:** Use function type hints (including Pydantic models) to automatically parse and validate LLM outputs.
- **Branching with `@task.llm_branch`:** Change the control flow of a DAG based on the output of an LLM.
- **Model support:** Support for [all models in the Pydantic AI library](https://ai.pydantic.dev/models/) (OpenAI, Anthropic, Gemini, Ollama, Groq, Mistral, Cohere, Bedrock)

## Design Principles

We follow the taskflow pattern of Airflow with three decorators:

- `@task.llm`: Define a task that calls an LLM. Under the hood, this creates a Pydantic AI `Agent` with no tools.
- `@task.agent`: Define a task that calls an agent. You can pass in a Pydantic AI `Agent` directly.
- `@task.llm_branch`: Define a task that branches the control flow of a DAG based on the output of an LLM. Enforces that the LLM output is one of the downstream task_ids.

The function supplied to each decorator is a translation function that converts the Airflow task's input into the LLM's input. If you don't want to do any translation, you
can just return the input unchanged.

## Motivation

AI workflows are becoming increasingly common as organizations look for pragmatic ways to get value out of LLMs. As with
any workflow, it's important to have a flexible and scalable way to orchestrate them.

Airflow is a popular choice for orchestrating data pipelines. It's a powerful tool for managing the dependencies
between tasks and for scheduling and monitoring them, and has been trusted by data teams everywhere for 10+ years. It comes "batteries included" with a rich set of capabilities:

- **Flexible scheduling:** run tasks on a fixed schedule, on-demand, or based on external events
- **Dynamic task mapping:** easily process multiple inputs in parallel with full error handling and observability
- **Branching and conditional logic:** change the control flow of a DAG based on the output of certain tasks
- **Error handling:** built-in support for retries, exponential backoff, and timeouts
- **Resource management:** limit the concurrency of tasks with Airflow Pools
- **Monitoring:** detailed logs and monitoring capabilities
- **Scalability:** designed for production workflows

This SDK is designed to make it easy to integrate LLM workflows into your Airflow pipelines. It allows you to do anything from simple LLM calls to complex agentic workflows.

## Examples

See the full set of examples in the [examples/dags](examples/dags) directory.

### LLM calls from a DAG (summarize Airflow's commits)

This example shows how to use the `@task.llm` decorator as part of an Airflow DAG. In the `@task.llm` decorator, we can
specify a model and system prompt. The decorator allows you to transform the Airflow task's input into the LLM's input.

See full example: [github_changelog.py](examples/dags/github_changelog.py)

```python
import os

import pendulum

from airflow.decorators import dag, task

from github import Github

@task
def get_recent_commits(data_interval_start: pendulum.DateTime, data_interval_end: pendulum.DateTime) -> list[str]:
    """
    This task returns a mocked list of recent commits. In a real workflow, this
    task would get the recent commits from a database or API.
    """
    print(f"Getting commits for {data_interval_start} to {data_interval_end}")
    gh = Github(os.getenv("GITHUB_TOKEN"))
    repo = gh.get_repo("apache/airflow")
    commits = repo.get_commits(since=data_interval_start, until=data_interval_end)
    return [f"{commit.commit.sha}: {commit.commit.message}" for commit in commits]

@task.llm(
    model="gpt-4o-mini",
    result_type=str,
    system_prompt="""
    Your job is to summarize the commits to the Airflow project given a week's worth
    of commits. Pay particular attention to large changes and new features as opposed
    to bug fixes and minor changes.

    You don't need to include every commit, just the most important ones. Add a one line
    overall summary of the changes at the top, followed by bullet points of the most
    important changes.

    Example output:

    This week, we made architectural changes to the core scheduler to make it more
    maintainable and easier to understand.

    - Made the scheduler 20% faster (commit 1234567)
    - Added a new task type: `example_task` (commit 1234568)
    - Added a new operator: `example_operator` (commit 1234569)
    - Added a new sensor: `example_sensor` (commit 1234570)
    """
)
def summarize_commits(commits: list[str] | None = None) -> str:
    """
    This task summarizes the commits. You can add logic here to transform the input
    before it gets passed to the LLM.
    """
    # don't need to do any translation
    return "\n".join(commits)

@task
def send_summaries(summaries: str):
    ...

@dag(
    schedule="@weekly",
    start_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=False,
)
def github_changelog():
    commits = get_recent_commits()
    summaries = summarize_commits(commits=commits)
    send_summaries(summaries)

github_changelog()
```

### LLM calls with structured outputs using `@task.llm` (user feedback -> sentiment and feature requests)

This example demonstrates how to use the `@task.llm` decorator to call an LLM and return a structured output. In this
case, we're using a Pydantic model to validate the output of the LLM. We recommend using the `airflow_ai_sdk.BaseModel`
class to define your Pydantic models in case we add more functionality in the future.

See full example: [product_feedback_summarization.py](examples/dags/product_feedback_summarization.py)

```python
import pendulum

from typing import Literal, Any

from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException

import airflow_ai_sdk as ai_sdk

from include.pii import mask_pii

@task
def get_product_feedback() -> list[str]:
    """
    This task returns a mocked list of product feedback. In a real workflow, this
    task would get the product feedback from a database or API.
    """
    ...

class ProductFeedbackSummary(ai_sdk.BaseModel):
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]
    feature_requests: list[str]

@task.llm(
    model="gpt-4o-mini",
    result_type=ProductFeedbackSummary,
    system_prompt="""
    You are a helpful assistant that summarizes product feedback.
    """
)
def summarize_product_feedback(feedback: str | None = None) -> ProductFeedbackSummary:
    """
    This task summarizes the product feedback. You can add logic here to transform the input
    before summarizing it.
    """
    # if the feedback doesn't mention Airflow, skip it
    if "Airflow" not in feedback:
        raise AirflowSkipException("Feedback does not mention Airflow")

    # mask PII in the feedback
    feedback = mask_pii(feedback)

    return feedback


@task
def upload_summaries(summaries: list[dict[str, Any]]):
    ...

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)
def product_feedback_summarization():
    feedback = get_product_feedback()
    summaries = summarize_product_feedback.expand(feedback=feedback)
    upload_summaries(summaries)

product_feedback_summarization()
```

### Agent calls with `@task.agent` (deep research agent)

This example shows how to build an AI agent that can autonomously invoke external tools (e.g., a knowledge base search) when answering a user question.

See full example: [deep_research.py](examples/dags/deep_research.py)

```python
import pendulum
import requests

from airflow.decorators import dag, task
from airflow.models.dagrun import DagRun
from airflow.models.param import Param

from bs4 import BeautifulSoup

from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

# custom tool to get the content of a page
def get_page_content(url: str) -> str:
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

    return distillation_agent.run_sync(soup.get_text())

deep_research_agent = Agent(
    "o3-mini",
    system_prompt="""
    You are a deep research agent who is very skilled at distilling information from the web. You are given a query and your job is to generate a research report.

    You can search the web by using the `duckduckgo_search_tool`. You can also use the `get_page_content` tool to get the contents of a page.

    Keep going until you have enough information to generate a research report. Assume you know nothing about the query or contents, so you need to search the web for relevant information.

    Do not generate new information, only distill information from the web.
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
    ...

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

deep_research()
```

### Changing dag control flow with `@task.llm_branch` (support ticket routing)

This example demonstrates how to use the `@task.llm_branch` decorator to change the control flow of a DAG based on the output of an LLM. In this case, we're routing support tickets based on the severity of the ticket.

See full example: [support_ticket_routing.py](examples/dags/support_ticket_routing.py)

```python
import pendulum
from airflow.decorators import dag, task
from airflow.models.dagrun import DagRun

@task.llm_branch(
    model="gpt-4o-mini",
    system_prompt="""
    You are a support agent that routes support tickets based on the priority of the ticket.

    Here are the priority definitions:
    - P0: Critical issues that impact the user's ability to use the product, specifically for a production deployment.
    - P1: Issues that impact the user's ability to use the product, but not as severely (or not for their production deployment).
    - P2: Issues that are low priority and can wait until the next business day
    - P3: Issues that are not important or time sensitive

    Here are some examples of tickets and their priorities:
    - "Our production deployment just went down because it ran out of memory. Please help.": P0
    - "Our staging / dev / QA deployment just went down because it ran out of memory. Please help.": P1
    - "I'm having trouble logging in to my account.": P1
    - "The UI is not loading.": P1
    - "I need help setting up my account.": P2
    - "I have a question about the product.": P3
    """,
    allow_multiple_branches=True,
)
def route_ticket(dag_run: DagRun) -> str:
    return dag_run.conf.get("ticket")

@task
def handle_p0_ticket(ticket: str):
    print(f"Handling P0 ticket: {ticket}")

@task
def handle_p1_ticket(ticket: str):
    print(f"Handling P1 ticket: {ticket}")

@task
def handle_p2_ticket(ticket: str):
    print(f"Handling P2 ticket: {ticket}")

@task
def handle_p3_ticket(ticket: str):
    print(f"Handling P3 ticket: {ticket}")

@dag(
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    params={"ticket": "Hi, our production deployment just went down because it ran out of memory. Please help."}
)
def support_ticket_routing():
    ticket = route_ticket()

    handle_p0_ticket(ticket)
    handle_p1_ticket(ticket)
    handle_p2_ticket(ticket)
    handle_p3_ticket(ticket)

support_ticket_routing()
```
