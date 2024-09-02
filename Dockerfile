FROM apache/airflow:2.10.0

USER root 

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git


COPY dependencies /dependencies
COPY requirements.txt /requirements.txt

USER airflow

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
