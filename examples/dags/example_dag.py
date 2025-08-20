from airflow.decorators import dag, task


@task.llm(model="gpt-4o-mini", system_prompt="Do some robot stuff", output_type=str)
def do_stuff() -> str:
    return "do stuff"


@dag
def example_dag():
    do_stuff()


example_dag()
