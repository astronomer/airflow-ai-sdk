"""
This shows how to use the SDK to build a simple GitHub change summarization workflow.
"""

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
    This task summarizes the commits.
    """
    # don't need to do any translation
    return "\n".join(commits)

@task
def send_summaries(summaries: str):
    """
    This task prints the summaries. In a real workflow, this task would send the summaries to a chat channel.
    """
    print(summaries)

@dag(
    schedule="@weekly",
    start_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=False,
)
def github_changelog():
    commits = get_recent_commits()
    summaries = summarize_commits(commits=commits)
    send_summaries(summaries)

dag = github_changelog()

if __name__ == "__main__":
    dag.test()
