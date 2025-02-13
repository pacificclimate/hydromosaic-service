# hydromosaic-service

At present, this data server returns a small set of canned data. It is intended to support development of the front end for phase 2 of SCIP, by providing a preview of the eventual data format. It will hopefully be replaced by a server that returns real data fairly quickly.

The name is a placeholder.

## Development

On a workstation, install and run with poetry:

```bash
poetry install
export FLASK_APP=hms.asgi
export FLASK_APP=development
poetry run uvicorn hms.asgi:connexion_app
```

A docker container is automatically built by a github action. The dummy server accesses no files nor databases, and so has no environmental configuration. You should be able to just run it.