FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install pip-tools
COPY requirements.* .
COPY api/requirements.in requirements.in
RUN pip-compile requirements.* --output-file requirements.txt
RUN pip install -r requirements.txt

COPY api/app /app
