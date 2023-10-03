.. epson_connect documentation master file, created by
   sphinx-quickstart on [date].
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Epson Connect
=============

Welcome to the Epson Connect documentation! Here, you will find details on modules and functions provided by the `epson_connect` package.

.. note:: This library is very much still in beta.

Getting Started
---------------

Installation of the Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install epson-connect

Prerequisites
~~~~~~~~~~~~~

Ensure that you have the required credentials:

- Printer Email
- Client ID
- Client Secret

These can be obtained from the Epson Connect API registration portal.

Usage
-----

You can initialize the client using direct parameters:

.. code-block:: python

   import epson_connect

   ec = epson_connect.Client(
       printer_email='...',
       client_id='...',
       client_secret='...',
   )

Alternatively, you can set up environment variables and initialize the client without parameters:

.. code-block:: bash

   # export EPSON_CONNECT_API_PRINTER_EMAIL=<an email address for the device>
   # export EPSON_CONNECT_API_CLIENT_ID=<client id>
   # export EPSON_CONNECT_API_CLIENT_SECRET=<client secret>

.. code-block:: python

   ec = epson_connect.Client()

Printing
--------

.. code-block:: python

   job_id = ec.printer.print('./path/to/file.pdf')

Scanning
--------

.. code-block:: python

   destinations = ec.scanner.list()
   print(destinations)

Tests
-----

.. code-block:: bash

   tox

Deployment
----------

When you're ready to build and publish your library:

.. code-block:: bash

   poetry build
   poetry publish

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/epson_connect

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
