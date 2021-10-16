<p align="center">
  <h2 align="center">ICON Metrics Service</h2>
</p>

[![loopchain](https://img.shields.io/badge/ICON-API-blue?logoColor=white&logo=icon&labelColor=31B8BB)](https://shields.io) [![GitHub Release](https://img.shields.io/github/release/geometry-labs/icon-metrics.svg?style=flat)]() ![](https://github.com/geometry-labs/icon-metrics/workflows/push-main/badge.svg?branch=main) [![codecov](https://codecov.io/gh/geometry-labs/icon-metrics/branch/main/graph/badge.svg)](https://codecov.io/gh/geometry-labs/icon-metrics) ![](https://img.shields.io/docker/pulls/geometrylabs/icon-metrics-api.svg) ![](https://img.shields.io/github/license/geometry-labs/icon-metrics)

Off chain indexer for the ICON Blockchain serving **metrics** for the [icon-explorer](https://github.com/geometry-labs/icon-explorer). Service is broken up into API and worker components that are run as individual docker containers. Events are derived from various bespoke JSON RPC / REST calls against the nodes across the ecosystem and a prometheus DB and persisted in a postgres database.

### Endpoints

TODO: Links and table

### Deployment

Service can be run in the following ways:

1. Independently from this repo with docker compose:
```bash
docker-compose -f docker-compose.db.yml -f docker-compose.yml up -d
# Or alternatively
make up
```

2. With the whole stack from the main [icon-explorer]() repo.

Run `make help` for more options.

### Development

For local development, you will want to run the `docker-compose.db.yml` as you develop. To run the tests,

```bash
make test
```

### License

Apache 2.0
