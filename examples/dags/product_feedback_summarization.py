"""
This shows how to use the SDK to build a simple product feedback summarization workflow.
"""

from typing import Any, Literal

import pendulum
from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException

import airflow_ai_sdk as ai_sdk


@task
def get_product_feedback() -> list[str]:
    """
    This task returns a mocked list of product feedback. In a real workflow, this
    task would get the product feedback from a database or API.
    """
    return [
        "I absolutely love Apache Airflow’s intuitive user interface and its robust DAG visualization capabilities. The scheduling and task dependency features are a joy to work with and greatly enhance my workflow efficiency. I would love to see an auto-scaling feature for tasks in future releases to further optimize performance.",
        "The overall experience with Apache Airflow has been disappointing due to its steep learning curve and inconsistent documentation. Many features seem underdeveloped, and the UI often feels clunky and unresponsive. It would be great if future updates included a revamped interface and clearer setup guides.",
        "Apache Airflow shines with its flexible Python-based task definitions and comprehensive logging system, making it a standout tool in workflow management. The integration capabilities are top-notch and have streamlined my data pipelines remarkably. I do hope that upcoming versions will include enhanced real-time monitoring features to further improve user experience.",
        "My experience with Apache Airflow has been largely negative, primarily because of the frequent performance lags and the overwhelming complexity of the configuration process. The lack of clear error messages only adds to the frustration. I wish the development team would simplify the setup process and incorporate more user-friendly error reporting mechanisms.",
        "I am very impressed with Apache Airflow’s modular design and its extensive library of operators, which together make it a powerful tool for orchestrating complex workflows. The overall stability during routine operations is commendable, and the community support is excellent. However, a feature for customizable dashboards would be a welcome addition in future updates.",
        "Using Apache Airflow has been a challenging experience due to its unintuitive interface and the slow performance during high-load periods. The limited documentation on advanced features makes troubleshooting a real hassle. I strongly recommend that future versions include comprehensive tutorials and performance optimizations to address these issues.",
        "Apache Airflow offers a remarkable level of flexibility with its DAG management and integration capabilities, which I find very useful. The platform consistently performs well in orchestrating multi-step data processes, and I appreciate its strong community backing. A potential enhancement could be the introduction of an in-built scheduling calendar for a more streamlined planning process.",
        "I have encountered numerous issues with Apache Airflow, including a clunky UI and recurring glitches that disrupt workflow execution. The error handling is inadequate, making it difficult to pinpoint problems during failures. It would be beneficial if the next update focused on enhancing UI stability and implementing a more robust error recovery system."
        "This is a review that is about something random"
    ]

class ProductFeedbackSummary(ai_sdk.BaseModel):
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]
    feature_requests: list[str]


@task.llm(model="gpt-4o-mini", result_type=ProductFeedbackSummary, system_prompt="Extract the summary, sentiment, and feature requests from the product feedback.",)
def summarize_product_feedback(feedback: str | None = None) -> ProductFeedbackSummary:
    """
    This task summarizes the product feedback. You can add logic here to transform the input
    before summarizing it.
    """
    # if the feedback doesn't mention Airflow, skip it
    if "Airflow" not in feedback:
        raise AirflowSkipException("Feedback does not mention Airflow")

    return feedback


@task
def upload_summaries(summaries: list[dict[str, Any]]):
    """
    This task prints the summaries. In a real workflow, this task would upload the summaries to a database or API.
    """
    from pprint import pprint
    for summary in summaries:
        pprint(summary)

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)
def product_feedback_summarization():
    feedback = get_product_feedback()
    summaries = summarize_product_feedback.expand(feedback=feedback)
    upload_summaries(summaries)

dag = product_feedback_summarization()

if __name__ == "__main__":
    dag.test()