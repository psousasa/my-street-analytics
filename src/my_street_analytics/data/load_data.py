import requests
import json
import urllib.request
import os

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
