# ORBIDI Technical Test

This is a template for python projects.

## Dependencies

For this project, the following dependencies are required:
* Python 3.14+
* [Spatialite](https://www.gaia-gis.it/fossil/libspatialite/index)
* [gdal](https://gdal.org/en/stable/)

## Virtual Environment

Create a virtual Environment

```
virtualenv .venv -p pytthon 3.14
source .venv/bin/activate
```

## Run Locally

After creating the virtual env

```
python -m manage migrate
python -m manage runserver
```

And the site will be available at `http://localhost:8000/`.


## Tests

Using pytest for Tests

```
python -m pytest
```

## Formatting and Linting

Using pre-commit for linting and formatting

```
pre-commit install
pre-commit run --all-files
```
