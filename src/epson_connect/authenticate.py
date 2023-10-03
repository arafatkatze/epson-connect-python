import logging
from datetime import datetime, timedelta

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class AuthCtx:
    """
    Authentication context for the printer API.

    This class manages authentication to the API by obtaining and refreshing access tokens as required.
    """
    def __init__(
            self,
            base_url: str,
            printer_email: str,
            client_id: str,
            client_secret: str,
    ) -> None:
        """
        Initialize the authentication context.

        :param base_url: The base URL for the API.
        :param printer_email: Email of the printer for authentication.
        :param client_id: OAuth client ID.
        :param client_secret: OAuth client secret.
        """
        self._base_url = base_url
        self._printer_email = printer_email
        self._client_id = client_id
        self._client_secret = client_secret

        self._expires_at = datetime.now()
        self._access_token = ''
        self._refresh_token = ''
        self._subject_id = ''

        self._auth()

    def _auth(self):
        """
        Authenticate or re-authenticate with the API.

        If the token has expired or not obtained yet, this function will get a new one.
        If we already have an access token, this function will use the refresh token to get a new one.
        """
        method = 'POST'
        path = '/api/1/printing/oauth2/auth/token?subject=printer'

        if self._expires_at > datetime.now():
            return

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        auth = HTTPBasicAuth(self._client_id, self._client_secret)

        if self._access_token == '':
            data = {
                'grant_type': 'password',
                'username': self._printer_email,
                'password': '',
            }
        else:
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self._refresh_token,
            }

        try:
            body = self.send(method, path, data=data, headers=headers, auth=auth)
        except ApiError as e:
            raise AuthenticationError(e)

        error = body.get('error')
        if error:
            raise AuthenticationError(error)

        # First time authenticating, set refresh_token.
        if self._access_token == '':
            self._refresh_token = body['refresh_token']

        self._expires_at = datetime.now() + timedelta(seconds=int(body['expires_in']))
        self._access_token = body['access_token']
        self._subject_id = body['subject_id']

    def _deauthenticate(self):
        """
        De-authenticate from the API.

        This method sends a DELETE request to de-authenticate the current session.
        """
        method = 'DELETE'
        path = f'/api/1/printing/printers/{self._subject_id}'
        self.send(method, path)

    def send(self, method, path, data=None, json=None, headers=None, auth=None) -> dict:
        """
        Send a request to the API.

        :param method: HTTP method (e.g., GET, POST).
        :param path: API path.
        :param data: Data payload for the request.
        :param json: JSON payload for the request.
        :param headers: HTTP headers.
        :param auth: Authentication object.

        :return: Dictionary containing the response.
        """
        if not auth:
            self._auth()

        headers = headers or self.default_headers

        logger.debug(f'{method} {path} data={data} json={json} headers={headers} auth={bool(auth)}')

        resp = requests.request(
            method=method,
            url=self._base_url + path,
            headers=headers,
            data=data,
            json=json,
            auth=auth,
        )

        # Assume JSON and fall back to raw bytes.
        try:
            resp = resp.json()
        except Exception:
            resp = {'code': resp.content.decode()}

        logger.debug(f'resp={resp}')

        error = resp.get('code')
        if error:
            raise ApiError(error)

        return resp

    @property
    def default_headers(self):
        """
        Default headers for the API requests.

        This includes the current access token for authentication.

        :return: Dictionary of default headers.
        """
        return {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json',
        }

    @property
    def device_id(self):
        """
        Get the device (printer) ID from the current session.

        :return: Device ID (subject_id from the authentication response).
        """
        return self._subject_id


class AuthenticationError(RuntimeError):
    """
    Error raised when there are authentication specific exceptions.
    This can include failed authentication attempts, invalid tokens, etc.
    """


class ApiError(RuntimeError):
    """
    General error raised for any API errors after authentication has succeeded.
    This can include bad requests, server errors, etc.
    """
