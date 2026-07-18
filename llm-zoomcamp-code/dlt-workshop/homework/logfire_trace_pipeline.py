import os
from pathlib import Path

import dlt
import requests
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / '.env', override=True)


@dlt.source
def logfire_traces_source():
    read_token = os.getenv('LOGFIRE_READ_TOKEN')
    if not read_token:
        raise RuntimeError('LOGFIRE_READ_TOKEN is not set')

    base_url = 'https://logfire-eu.pydantic.dev/v1/query'
    headers = {
        'Authorization': f'Bearer {read_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    payload = {
        'sql': """
        SELECT
            *
        FROM records
        LIMIT 50
        """
    }

    response = requests.get(base_url, headers=headers, params=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict):
        if 'rows' in data:
            rows = data['rows']
        elif 'columns' in data and data.get('columns'):
            rows = []
            columns = data['columns']
            row_count = max(len(column.get('values', [])) for column in columns) if columns else 0
            for idx in range(row_count):
                row = {}
                for column in columns:
                    values = column.get('values', [])
                    row[column['name']] = values[idx] if idx < len(values) else None
                rows.append(row)
            
        else:
            rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        rows = [data]

    yield dlt.resource(rows, name='records')


def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name='logfire_trace_pipeline',
        destination='duckdb',
        dataset_name='agent_traces',
    )
    load_info = pipeline.run(logfire_traces_source())
    print(load_info)
    return load_info


if __name__ == '__main__':
    run_pipeline()
