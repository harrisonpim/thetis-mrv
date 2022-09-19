# Getting started

## Populating a `.env` file

You'll need to fill out a set of postgres credentials in the `.env` file. You should be able to use any remote db, but the defaults for the locally running postgres container are as follows:
```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=database
```

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

### Returning data from the database

Take a look at the docs at `localhost/docs`

### Inference

You can make predictions about the `shipType` attribute using standard reporting data using the `/predict` endpoint. To see the data being fed to the model, you can use the `/encode` endpoint.
