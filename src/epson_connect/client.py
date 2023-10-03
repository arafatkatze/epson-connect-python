import os

from .authenticate import AuthCtx
from .printer import Printer
from .scanner import Scanner


class Client:
    """
    Client for the Epson Connect API.
    
    This class provides a higher-level interface to interact with the Epson Connect services,
    including authentication, printer management, and scanning operations.
    """
    EC_BASE_URL = 'https://api.epsonconnect.com'

    def __init__(self, base_url='', printer_email='', client_id='', client_secret='') -> None:
        """
        Initialize the Epson Connect client.

        :param base_url: The base URL for the Epson Connect API. Defaults to the official Epson Connect API URL.
        :param printer_email: Email of the printer used for authentication.
        :param client_id: OAuth client ID for the Epson Connect API.
        :param client_secret: OAuth client secret for the Epson Connect API.

        If any of the parameters are not provided, the method will attempt to fetch them from environment variables.
        """
        base_url = base_url or self.EC_BASE_URL

        printer_email = printer_email or os.environ.get('EPSON_CONNECT_API_PRINTER_EMAIL')
        if not printer_email:
            raise ClientError('Printer Email can not be empty')

        client_id = client_id or os.environ.get('EPSON_CONNECT_API_CLIENT_ID')
        if not client_id:
            raise ClientError('Client ID can not be empty')

        client_secret = client_secret or os.environ.get('EPSON_CONNECT_API_CLIENT_SECRET')
        if not client_secret:
            raise ClientError('Client Secret can not be empty')

        self._auth_ctx = AuthCtx(base_url, printer_email, client_id, client_secret)

    def deauthenticate(self):
        """
        De-authenticate from the Epson Connect API.

        This method ends the current session and invalidates the access token.
        """
        self._auth_ctx._deauthenticate()

    @property
    def printer(self):
        """
        Get the Printer interface for the current session.

        :return: An instance of the Printer class.
        """
        return Printer(self._auth_ctx)

    @property
    def scanner(self):
        """
        Get the Scanner interface for the current session.

        :return: An instance of the Scanner class.
        """
        return Scanner(self._auth_ctx)


class ClientError(ValueError):
    """
    Error raised for client-specific exceptions.

    This includes cases like missing credentials, misconfigured environment, etc.
    """
