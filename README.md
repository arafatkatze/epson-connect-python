# Epson Connect
[![CI/CD](https://github.com/arafatkatze/epson-api-python/actions/workflows/cicd.yml/badge.svg)](https://github.com/arafatkatze/epson-api-python/actions/workflows/cicd.yml) [![Documentation Status](https://readthedocs.org/projects/epson-connect-api/badge/?version=latest)](https://epson-connect-api.readthedocs.io/en/main/?badge=latest)

The Epson Connect Library offers a comprehensive interface to the Epson Connect API. With this library, users can seamlessly control Epson printers and scanners through the Epson cloud service.



## Getting Started

## Installation of the library

```bash 
pip3 install epson-connect
```


## Prerequisites
Ensure that you have the required credentials:

- Printer Email
- Client ID
- Client Secret

These can be obtained from the Epson Connect API registration portal. For more detailed steps you can refer to the medium blogs from Epson.

## Usage
You can initialize the client using direct parameters:


```python
import epson_connect

ec = epson_connect.Client(
    printer_email='...',
    client_id='...',
    client_secret='...',
)
```

Alternatively, you can set up environment variables and initialize the client without parameters:


```
# export EPSON_CONNECT_API_PRINTER_EMAIL=<an email address for the device>
# export EPSON_CONNECT_API_CLIENT_ID=<client id>
# export EPSON_CONNECT_API_CLIENT_SECRET=<client secret>
```

```python
ec = epson_connect.Client()
```

## Printing
```
job_id = ec.printer.print('./path/to/file.pdf')
```

## Scanning

```python
destinations = ec.scanner.list()
print(destinations)
```

### Tests

```
tox
```
This repository uses Github Workflows to run a CI CD pipeline it's defined in `.github/workflows/cicd.yml`

### Deployment
When you're ready to build and publish your library:


```
poetry build
poetry publish
```
