# Running this project on an M1 mac

Running the default postgres image on an m1 mac produces a SCRAM authentication error in `libpq`.

[This answer on stackoverflow](https://stackoverflow.com/a/70238851) points to a solution. Setting the `DOCKER_DEFAULT_PLATFORM` environment variable to `linux/amd4` will run the image via rosetta. To set the variable, run:

```sh
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```
