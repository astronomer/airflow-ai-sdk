"""
DAG that detects file types using AI and processes them accordingly.

This DAG demonstrates:
1. AI-powered file type detection based on extension and content
2. Dynamic branching based on detected file type
3. File format conversions to CSV
4. CSV analysis with summary statistics
"""

from datetime import datetime, timedelta
import json
import csv
import os
from typing import Literal

import airflow_ai_sdk as ai_sdk
from airflow.decorators import task, dag
from airflow.models import DagRun
from airflow.exceptions import AirflowSkipException


class FileTypeDetection(ai_sdk.BaseModel):
    """Schema for file type detection output"""
    file_type: Literal["json", "csv", "tsv", "xlsx", "unknown"]
    confidence: float
    delimiter: str | None = None
    detected_issues: list[str] = []
    recommendation: str


class CSVAnalysis(ai_sdk.BaseModel):
    """Schema for CSV analysis output"""
    columns: list[str]
    row_count: int
    column_stats: dict[str, dict]
    data_quality_issues: list[str]
    summary: str


@task.llm(
    model="gpt-4o-mini",
    result_type=FileTypeDetection,
    system_prompt="""You are a file type detection expert. Analyze the provided file path and content sample to determine:
1. The inferred file type (json, csv, tsv, xlsx, or unknown)
2. Your confidence level (0-1)
3. For CSV/TSV files, detect the delimiter (comma, tab, pipe, etc.)
4. Any issues (e.g., misnamed files, encoding problems, malformed data)
5. A recommendation for processing

Consider both the file extension AND the actual content. Files may be misnamed.
For CSV-like files, check for different delimiters: comma (,), tab (\\t), pipe (|), semicolon (;)."""
)
def detect_file_type(file_path: str) -> FileTypeDetection:
    """Detect file type using AI based on extension and content sample"""
    # Initialize variables
    sample_lines = []
    content_sample = ""

    # Read first few lines of the file
    try:
        with open(file_path, encoding='utf-8') as f:
            # Read up to 1KB or 20 lines, whichever comes first
            bytes_read = 0
            for i, line in enumerate(f):
                if i >= 20 or bytes_read >= 1024:
                    break
                sample_lines.append(line)
                bytes_read += len(line.encode('utf-8'))
            content_sample = ''.join(sample_lines)
    except Exception as e:
        content_sample = f"Error reading file: {str(e)}"

    # Prepare data for LLM
    analysis_data = {
        "file_path": file_path,
        "file_name": os.path.basename(file_path),
        "extension": os.path.splitext(file_path)[1],
        "content_sample": content_sample[:1000],  # Limit sample size
        "sample_lines": len(sample_lines)
    }

    return json.dumps(analysis_data)


@task.branch
def route_file(detection_result: dict) -> str:
    """Route file to appropriate processing task based on detection"""
    if detection_result['confidence'] < 0.8:
        raise AirflowSkipException("Low confidence in file type detection")

    if detection_result['file_type'] == 'unknown':
        raise AirflowSkipException("Unknown file type")

    file_type = detection_result['file_type']

    # Route based on file type
    if file_type == 'json':
        return 'translate_json'
    elif file_type == 'xlsx':
        return 'translate_xlsx'
    else:  # csv, tsv, or any delimiter
        return 'translate_csv'


@task
def translate_json(file_path: str) -> str:
    """Convert JSON file to CSV format"""
    output_path = file_path.replace('.json', '_converted.csv').replace('.txt', '_converted.csv')

    with open(file_path) as f:
        data = json.load(f)

    # Handle nested JSON structures
    if isinstance(data, dict) and len(data) == 1:
        # If single key with list value, extract the list
        key = list(data.keys())[0]
        if isinstance(data[key], list):
            data = data[key]

    # Flatten nested structures if needed
    if isinstance(data, list) and data:
        # Extract all unique keys from all records
        all_keys = set()
        flattened_data = []

        for record in data:
            flattened_record = {}
            for key, value in record.items():
                if isinstance(value, dict):
                    # Flatten nested dicts
                    for sub_key, sub_value in value.items():
                        flattened_record[f"{key}_{sub_key}"] = sub_value
                else:
                    flattened_record[key] = value
            flattened_data.append(flattened_record)
            all_keys.update(flattened_record.keys())

        # Write to CSV
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            writer.writerows(flattened_data)

    print(f"Converted JSON to CSV: {output_path}")
    return output_path


@task
def translate_csv(file_path: str, **context) -> str:
    """Standardize CSV file with non-standard delimiter to comma-separated"""
    detection = context['ti'].xcom_pull(task_ids='detect_file_type')
    delimiter = detection.get('delimiter', '\t') or '\t'  # Default to tab if not detected

    output_path = file_path.replace('.tsv', '_converted.csv').replace('.txt', '_converted.csv')
    if not output_path.endswith('_converted.csv'):
        output_path = output_path.replace('.csv', '_converted.csv')

    with open(file_path) as infile, open(output_path, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter=delimiter)
        writer = csv.writer(outfile)

        for row in reader:
            writer.writerow(row)

    print(f"Converted delimiter '{delimiter}' to standard CSV: {output_path}")
    return output_path


@task
def translate_xlsx(file_path: str, **context) -> str:
    """Convert Excel file to CSV format"""
    try:
        import openpyxl
    except ImportError:
        raise ImportError("openpyxl is required for Excel file processing")

    output_path = file_path.replace('.xlsx', '_converted.csv')

    # Load the workbook
    wb = openpyxl.load_workbook(file_path, read_only=True)

    # Get the first sheet (or active sheet)
    sheet = wb.active

    # Write to CSV
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in sheet.iter_rows(values_only=True):
            writer.writerow(row)

    wb.close()
    print(f"Converted Excel to CSV: {output_path}")
    return output_path


@task.llm(
    model="gpt-4o-mini",
    result_type=CSVAnalysis,
    system_prompt="""Analyze the CSV file and provide:
1. List of column names
2. Total row count
3. For each column, provide statistics:
   - Data type (string, numeric, date, mixed)
   - For numeric: min, max, mean, missing count
   - For string: unique values count, most common value, missing count
   - For dates: earliest, latest, missing count
4. Data quality issues (missing values, inconsistent formats, outliers)
5. A brief summary of what the data represents"""
)
def process_csv(file_path: str, **context) -> CSVAnalysis:
    """Analyze CSV file and generate summary statistics"""
    # Handle both direct CSV files and converted files
    if 'translate_' in context['ti'].task_id:
        # This was called after a translation task
        file_path = context['ti'].xcom_pull()

    # Read CSV and analyze
    with open(file_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return json.dumps({"error": "Empty CSV file", "file_path": file_path})

    # Prepare analysis data
    analysis = {
        "file_path": file_path,
        "columns": list(rows[0].keys()),
        "row_count": len(rows),
        "sample_rows": rows[:5],  # First 5 rows as sample
        "column_samples": {}
    }

    # Get sample values for each column
    for column in analysis["columns"]:
        values = [row.get(column, '') for row in rows]
        unique_values = list(set(values))[:10]  # First 10 unique values
        analysis["column_samples"][column] = {
            "sample_values": unique_values,
            "total_values": len(values),
            "unique_count": len(set(values)),
            "empty_count": sum(1 for v in values if not v)
        }

    return json.dumps(analysis)


# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    'infer_file_type',
    default_args=default_args,
    description='Detect file types and process them accordingly',
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=['ai-sdk', 'file-processing', 'llm'],
    params={
        'file_path': '/usr/local/airflow/dags/data/misnamed_file.txt'
    }
)
def detect_file_type_dag():
    """
    Main DAG definition with file type detection and processing workflow.

    Configure the file path in the DAG run configuration:
    {
        "file_path": "/path/to/your/file"
    }
    """

    @task
    def get_file_path(dag_run: DagRun) -> str:
        """Get file path from DAG run configuration"""
        file_path = dag_run.conf.get('file_path')
        if not file_path:
            # Default to a sample file for testing
            file_path = os.path.join(
                os.path.dirname(__file__),
                'data',
                'misnamed_file.txt'  # This is actually a CSV with pipe delimiter
            )
        return file_path

    # Get file path
    file_path = get_file_path()

    # Detect file type
    detection = detect_file_type(file_path)

    # Route based on detection
    routing = route_file(detection)

    # Translation tasks (only instantiated when branching leads to them)
    json_task = translate_json(file_path)
    csv_task = translate_csv(file_path)
    xlsx_task = translate_xlsx(file_path)

    # Single process_csv task that accepts input from any translation task
    # Use trigger_rule to ensure it runs when at least one upstream succeeds
    @task(trigger_rule="none_failed_min_one_success")
    def process_csv_wrapper(**context) -> CSVAnalysis:
        """Process CSV file from whichever translation task ran"""
        # Check which upstream task actually ran and get its output
        ti = context['ti']
        for task_id in ['translate_json', 'translate_csv', 'translate_xlsx']:
            result = ti.xcom_pull(task_ids=task_id)
            if result:  # This task actually ran and produced output
                return process_csv.function(result, **context)
        raise ValueError("No translation task produced output")

    final_process = process_csv_wrapper()

    # Set up routing dependencies
    routing >> [json_task, csv_task, xlsx_task]
    [json_task, csv_task, xlsx_task] >> final_process


# Instantiate the DAG
dag = detect_file_type_dag()
