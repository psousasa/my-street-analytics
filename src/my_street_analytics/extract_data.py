import requests
import json
import urllib.request
import os
from google.cloud import storage
from google.cloud import bigquery
import pandas as pd
from dotenv import load_dotenv, find_dotenv


def create_gcp_client(credentials_path: str) -> storage.Client:
    # Initialize the storage client
    return storage.Client.from_service_account_json(credentials_path)


def web_file_to_gcp_bucket(
    bucket_name: str,
    storage_client: storage.Client,
    file_root_destination: str,
    local_data_root: str,
):
    with open(f"{local_data_root}/source.json", "r") as f:
        data_source = json.loads(f.read())

    bucket = storage_client.get_bucket(bucket_name)

    cols = ["dt_registo", "area", "tipo", "Subseccao", "Freguesia", "Longitude_Subseccao", "Latitude_Subseccao"]
    for year, url in data_source.items():
        df = pd.read_excel(url)
        bucket.blob(f"{file_root_destination}/{year}.csv").upload_from_string(
            df[cols].to_csv(index=False), "text/csv"
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


if __name__ == '__main__':

    load_dotenv(find_dotenv("dev.env"))

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    bucket_name = os.getenv("TF_VAR_GCP_BUCKET")
    file_root_destination = os.getenv("GCS_BUCKET_ROOT")
    local_data_root = os.getenv("SOURCE_WEB_FILES")
    project_id = os.getenv("TF_VAR_GCP_PROJECT")
    dataset = os.getenv("TF_VAR_GCP_BQ_DATASET")
    table_name = os.getenv("GCP_EXTERNAL_TABLE")


    storage_client = create_gcp_client(
        credentials_path=credentials_path
    )

    web_file_to_gcp_bucket(bucket_name=bucket_name, storage_client=storage_client, file_root_destination=file_root_destination, local_data_root=local_data_root)

    bq_external_table(project_id=project_id, bucket_name=bucket_name, files_root=file_root_destination, dataset=dataset, table_name=table_name)
