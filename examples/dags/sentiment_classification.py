from typing import Literal
from airflow.decorators import dag, task
import pendulum
from airflow.models.dagrun import DagRun


@task.llm(
    model="gpt-4o-mini",
    result_type=Literal["positive", "negative", "neutral"],
    system_prompt="Classify the sentiment of the given text.",
)
def process_with_llm(dag_run: DagRun) -> str:
    input_text = dag_run.conf.get("input_text")

    # can do pre-processing here (e.g. PII redaction)
    return input_text


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1),
    catchup=False,
    params={"input_text": "I'm very happy with the product."},
)
def sentiment_classification():
    process_with_llm()


sentiment_classification()
