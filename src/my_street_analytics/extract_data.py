import requests
import json
import urllib.request
import os
from google.cloud import storage


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
        response = requests.get(url, stream=True)

        destination_blob_name = f"{file_root_destination}/{year}.xlsx"

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(response.raw)
