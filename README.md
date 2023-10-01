# Epson Connect
The Epson Connect Library offers a comprehensive interface to the Epson Connect API. With this library, users can seamlessly control Epson printers and scanners through the Epson cloud service.


NB: This library is very much still in beta.

## Getting Started

## Installation of the library

```bash 
pip install epson-connect
```


## Prerequisites
Ensure that you have the required credentials:

- Printer Email
- Client ID
- Client Secret
These can be obtained from the Epson Connect API registration portal. 

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

### Deployment
When you're ready to build and publish your library:


```
poetry build
poetry publish
```
