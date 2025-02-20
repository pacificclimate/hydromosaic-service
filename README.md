# hydromosaic-service

This data service allows users to download a hydrological modeled timeseries of their choice, extracted from netCDF files. The API provides metadata about available timeseries organized by "outlet" - a point along a stream, river, or lake for which data is available. Metadata about timeseries is stored in a [custom database](https://github.com/pacificclimate/hydromosaic-db).

When the user has been guided by the front end map interface to find the ID of the timeseries they care about, this service extracts the data from a netCDF file and provides it in an idiosyncratic CSV format. Each CSV file contains two tables; one with metadata about the timeseries, and one with the actual timeseries data.

The name is a placeholder.

## Development

On a workstation, install and run with poetry. Set the `HMS_DSN` environment variable to the connection string for the database:

```bash
poetry install
export FLASK_APP=hms.asgi
export FLASK_APP=development
export HMS_DSN=postgresql://username:password@server:port/hydromosaic
poetry run uvicorn hms.asgi:connexion_app
```

A docker container is automatically built by a github action. The HMS_DSN environment variable should be set at runtime, and the docker should be granted access to volumes containing the netCDF files.