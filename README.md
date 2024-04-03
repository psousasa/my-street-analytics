# My Street Analytics - DE Zoomcamp 2024 Capstone

## Problem description

My municipal government has a Mobile App - Na Minha Rua ("In My Street") - that I have always found very useful and interesting. **Useful** because you can eventually cut unnecessary costs in active vigilance from authorities, replacing them by the people who actually live there, granting responsability and sense of place. **Interesting** since there is a fine line between a responsible citizen, dutifuly reporting what is wrong, and one that reports what **he thinks** is wrong.

Jokes aside, I found this to be a good opportunity to test my perception of how the city behaves (party zones vs residential) and how that behaviour evolves throughout the year (I'm thinking increased littering on Christmas, New Year's Eve and City Celebrations).

This App produces a simple data set. Each entry contains a date, event category and sub category, and approximate location within the Municipal Parish's subsection.

## Dataset

Since it is a Government app, its data is governed by EU directives and (at least usage data) needs to be made available. It can be found in [EU's Database](https://data.europa.eu/data/datasets/ocorrencias-na-minha-rua?locale=en) or in [Lisbon's Municipal Hall website](https://lisboaaberta.cm-lisboa.pt/index.php/pt/dados/conjuntos-de-dados). It consists of one Excel file per year since 2017-2023.


## Technologies

- IaC: Terraform
- Container: Docker
- Data Lake: Google Cloud Storage
- Data Warehouse: Google Cloud BigQuery
- Batch Orchestration: Make
- Anlytics Engineering: dbt

## Data pipeline

1. Extract: 
	- Download Excel files from Web and transform into CSV.
	- Upload CSV files to bucket in GCS.
    - Create an external table in BigQuery based on the CSV files within the bucket.

2. Transform:
	- Ingest data into staging table.
    - Transform the data into a dimensional model
    - Build fact tables.

3. Load:
    - Create views and Reports.


### Data Model
### Staging


**Partitioning**

- By Category, since it would allows to filter out and target specific ones.

**Clustering**

- By date would be the most useful since we are not filtering on it and might want to plot timeseries.

_**Note on Clustering and Partitioning:** Being a small dataset, these were implemented to meet evaluation metrics._

## Folder structure

- `data/`: sample dataset, mappings and data web endpoints.
- `dbt/`: dbt models to build Data Warehouse.
- `docker/`: Dockerfile to run extraction implemented in Python.
- `src/`: Python files for extraction.
- `terraform/`: Terraform to setup Google Cloud resources.

_**Note on src:** This folder structure was chosen with a fully fledged Python Module in mind, not a single script._


## Instructions

### Prerequisites

- Google Cloud Platform:
	- An empty project.
	- Service account with Storage and BigQuery permissions.
	- Service account key stored locally.

- Terraform installed (v1.7.4 was used).
- Source environment variables:
    1. Create copy of sample.env named dev.env in same directory.
    2. Fill in variables.
    3. Source the dev.env file. Note that you should use this terminal window to run the pipeline:

```
$ source dev.env"
```

### Pipeline execution

1. Run `make setup` to create the Google Cloud Infra (GCS bucket and BigQuery DataSet) using Terraform and build the Docker containers.

2. Run `make start` to run the Docker containers.

3. Run `make extract` to extract the files using python.

4. Run `make transform` to run dbt models - transform and load.

### Dashboard


Using Google Data Studio, a dashboard showing node types and number of comments and blogs in a timeline.

You can access the dashboard [here](https://lookerstudio.google.com/reporting/7146e196-3ce8-4b3c-9bc6-70eef2ae1ad1).

![dashboard](dw_dll.png)

## FAQ

- Error when making Prefect blocks: `httpx.ConnectError: All connection attempts failed`?
	- Try `make stop && make start`, and check if you can run the code inside a bash shell: `docker compose run cli /bin/bash` (`python blocks/make_blocks.py`).

## Next steps

- Add tests to dbt
- Add tests to python
- Enable scheduling
- Enable partial loading
- Improve DB Model
