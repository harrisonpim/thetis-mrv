# Getting started

## Jupyter notebooks

To start a jupyter server locally, run

```sh
docker compose up --build jupyter
```

## Downloading data

To download all existing datasets, run

```sh
docker compose up --build get-data
```

They'll be saved in `.xlsx` format in the `/data/raw` directory.


