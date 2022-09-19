FROM python:3.8

RUN pip install --upgrade pip pip-tools
COPY requirements.* .
COPY train/requirements.* .
RUN pip-compile requirements.* --output-file requirements.txt
RUN pip install -r requirements.txt

COPY train/*.py /
