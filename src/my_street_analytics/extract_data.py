import requests
import json
import urllib.request
import os
from google.cloud import storage
from google.cloud import bigquery
import pandas as pd


def load_data(data_root):
    with open(f"{data_root}/source.json", "r") as f:
        data_source = json.loads(f.read())

    [
        urllib.request.urlretrieve(
            data_source[year], os.path.join(data_root, f"{year}.xlsx")
        )
        for year in data_source
    ]

def stream_data(data_root):
    with open(f"{data_root}/source.json", "r") as f:
        data_source = json.loads(f.read())

    for year in data_source:
        with requests.get(data_source[year], stream=True) as r:
            r.raise_for_status()

            with open(os.path.join(data_root, f"{year}.xlsx"), "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)


def create_gcp_client(credentials_path: str) -> storage.Client:
    # Initialize the storage client
    return storage.Client.from_service_account_json(credentials_path)

import json


def web_file_to_gcp_bucket(
    bucket_name: str,
    storage_client: storage.Client,
    file_root_destination: str,
    local_data_root: str,
):
    with open(f"{local_data_root}/source.json", "r") as f:
        data_source = json.loads(f.read())

    bucket = storage_client.get_bucket(bucket_name)

    for year, url in data_source.items():
        df = pd.read_excel(url)
        bucket.blob(f"{file_root_destination}/{year}.csv").upload_from_string(
            df.to_csv(index=False), "text/csv"
        )


def bq_external_table(
    project_id: str, bucket_name: str, files_root: str, dataset: str, table_name: str
) -> bigquery.table._EmptyRowIterator:

    client = bigquery.Client(project=project_id)
    sql = f"""
            CREATE OR REPLACE EXTERNAL TABLE `{dataset}.{table_name}`
            OPTIONS (
                format = 'CSV',
                uris = ['gs://{bucket_name}/{files_root}/*.csv'])
                """

    query_job = client.query(sql)

    return query_job.result()
