"""
Example DAG that generates parameterized SQL from natural language using the llm decorator.
"""

import pendulum
try:
    from airflow.sdk import dag, task
except ImportError:
    from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException

import airflow_ai_sdk as ai_sdk


class GeneratedSQL(ai_sdk.BaseModel):
    dialect: str
    sql: str
    notes: str


@task
def get_requests() -> list[dict]:
    """
    Return example analytics questions and table schemas.
    """
    return [
        {
            "dialect": "postgres",
            "schema": {
                "tables": {
                    "orders": {
                        "columns": [
                            {"name": "order_id", "type": "int"},
                            {"name": "customer_id", "type": "int"},
                            {"name": "order_date", "type": "timestamp"},
                            {"name": "total_amount", "type": "numeric"},
                        ]
                    },
                    "customers": {
                        "columns": [
                            {"name": "customer_id", "type": "int"},
                            {"name": "country", "type": "text"},
                        ]
                    },
                }
            },
            "request": "Total revenue by country for the last 30 days",
        },
        {
            "dialect": "snowflake",
            "schema": {
                "tables": {
                    "events": {
                        "columns": [
                            {"name": "user_id", "type": "varchar"},
                            {"name": "event_type", "type": "varchar"},
                            {"name": "event_time", "type": "timestamp"},
                        ]
                    }
                }
            },
            "request": "Daily active users for the last 14 days",
        },
    ]


@task.llm(
    model="gpt-4o-mini",
    output_type=GeneratedSQL,
    system_prompt=
    """
    You convert analytics requests plus a simplified schema into parameterized SQL for the given dialect.
    - Use safe identifiers and date handling idioms for the dialect.
    - Prefer parameterized filters (e.g., :start_date, :end_date) where applicable.
    - Return:
      - dialect: the input dialect
      - sql: a single valid query
      - notes: assumptions or caveats made
    """,
)
def generate_sql(payload: dict | None = None) -> GeneratedSQL:
    if payload is None:
        raise AirflowSkipException("No payload provided")

    return (
        "Dialect: "
        + payload["dialect"]
        + "\nSchema: "
        + str(payload["schema"]) 
        + "\nRequest: "
        + payload["request"]
    )


@task
def review_and_print(statements: list[dict]):
    from pprint import pprint
    pprint(statements)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=False,
)
def sql_generation():
    requests = get_requests()
    statements = generate_sql.expand(payload=requests)
    review_and_print(statements)


dag = sql_generation()

