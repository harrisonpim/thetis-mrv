FROM python:3.8-slim

RUN pip install --upgrade pip pip-tools
COPY requirements.* .
COPY pipeline/requirements.* .
RUN pip-compile requirements.* --output-file requirements.txt
RUN pip install -r requirements.txt

COPY pipeline/*.py /
