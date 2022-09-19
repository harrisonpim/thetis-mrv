# Getting started

## Jupyter notebooks

To start a jupyter server locally, run

```sh
docker compose up --build jupyter
```

## Downloading data

To download and process all existing data, run

```sh
docker compose up --build pipeline
```

They'll be saved in `.xlsx` format in the `/data/raw` directory, and pushed into a postgres database, stores locally in `/data/postgres`.

## API

```sh
docker compose up --build api
```
