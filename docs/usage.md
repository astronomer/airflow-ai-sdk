# Basic Usage

## Installation

Install the SDK with any optional dependencies you need:

```bash
pip install airflow-ai-sdk[openai,duckduckgo]
```

Available optional dependencies are defined in the [pyproject.toml](https://github.com/astronomer/airflow-ai-sdk/blob/main/pyproject.toml#L17) file. You can also install optional dependencies from [Pydantic AI](https://ai.pydantic.dev/install/) directly.

## Task Decorators

### LLM Tasks with @task.llm

```python
from airflow.decorators import dag, task
import pendulum
import airflow_ai_sdk as ai_sdk

@task.llm(
    model="gpt-4o-mini",  # model name
    result_type=str,       # return type
    system_prompt="You are a helpful assistant."  # system prompt for the LLM
)
def process_with_llm(input_text: str) -> str:
    # This function transforms Airflow task input into LLM input
    return input_text

@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1),
    catchup=False,
)
def simple_llm_dag():
    result = process_with_llm("Summarize the benefits of using Airflow with LLMs.")

simple_llm_dag()
```

### Structured Output with Pydantic Models

```python
from typing import Literal
import airflow_ai_sdk as ai_sdk

class TextAnalysis(ai_sdk.BaseModel):
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]
    key_points: list[str]

@task.llm(
    model="gpt-4o-mini",
    result_type=TextAnalysis,
    system_prompt="Analyze the provided text."
)
def analyze_text(text: str) -> TextAnalysis:
    return text
```

### Agent Tasks with @task.agent

```python
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

research_agent = Agent(
    "o3-mini",  # model name
    system_prompt="You are a research agent that finds information from the web.",
    tools=[duckduckgo_search_tool()]  # tools the agent can use
)

@task.agent(agent=research_agent)
def research_topic(topic: str) -> str:
    return topic
```

### Branching Tasks with @task.llm_branch

```python
@task.llm_branch(
    model="gpt-4o-mini",
    system_prompt="Classify the text based on its priority.",
    allow_multiple_branches=False  # only select one branch
)
def classify_priority(text: str) -> str:
    return text

@task
def handle_high_priority(text: str):
    print(f"Handling high priority: {text}")

@task
def handle_medium_priority(text: str):
    print(f"Handling medium priority: {text}")

@task
def handle_low_priority(text: str):
    print(f"Handling low priority: {text}")

@dag(...)
def priority_routing_dag():
    result = classify_priority("This is an urgent request")

    high_task = handle_high_priority(result)
    medium_task = handle_medium_priority(result)
    low_task = handle_low_priority(result)

    classify_priority >> [high_task, medium_task, low_task]
```

### Embedding Tasks with @task.embed

```python
@task.embed(
    model_name="all-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True}
)
def create_embeddings(text: str) -> list[float]:
    return text

@dag(...)
def embedding_dag():
    texts = ["First text", "Second text", "Third text"]
    embeddings = create_embeddings.expand(text=texts)
    # Now use embeddings for semantic search, clustering, etc.
```

## Error Handling

You can use Airflow's built-in error handling features with these tasks:

```python
@task.llm(
    model="gpt-4o-mini",
    result_type=str,
    system_prompt="Answer the question.",
    retries=3,  # retry 3 times if the task fails
    retry_delay=pendulum.duration(seconds=30),  # wait 30 seconds between retries
)
def answer_question(question: str) -> str:
    return question
```
