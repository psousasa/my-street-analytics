FROM python:3.10

# Required for Python mysqlclient package
RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt
COPY ./src/my_street_analytics app/my_street_analytics

COPY ./dev.env dev.env
COPY ./data data

RUN python3 -m pip install -U -r requirements.txt

CMD [ "python", "app/my_street_analytics/extract_data.py"]
