"""
Example DAG that routes support tickets to the correct department using the llm_branch decorator.
"""

import pendulum
from airflow.decorators import dag, task
from airflow.models.dagrun import DagRun


def mask_pii(ticket_content: str) -> str:
    """
    This function masks PII in the ticket content. You could do this one of a few ways...
    - Use regexes / string replacements to mask PII
    - Use a pretrained model via an API (e.g. HuggingFace)
    - Use a custom model run locally on the machine
    """
    return ticket_content

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
    """
    This task routes the support ticket to the correct department based on the priority of the ticket. It also does
    PII masking on the ticket content before sending it to the LLM.
    """
    ticket_content = dag_run.conf.get("ticket")

    # mask PII in the ticket content
    ticket_content = mask_pii(ticket_content)

    return ticket_content

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

dag = support_ticket_routing()

if __name__ == "__main__":
    dag.test(run_conf={"ticket": "Hi, our production deployment just went down because it ran out of memory. Please help."})
