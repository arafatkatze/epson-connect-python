from .authenticate import AuthCtx


class Scanner:
    """
    Scanner class for managing scan destinations in the Epson Connect API.

    This class provides methods to add, update, list, and remove scan destinations.
    """
    # Define valid destination types for the scanner
    VALID_DESTINATION_TYPES = {
        'mail',
        'url',
    }

    def __init__(self, auth_ctx: AuthCtx) -> None:
        """
        Initialize the Scanner object.

        :param auth_ctx: The authentication context which provides authenticated sessions to the API.
        """
        self._auth_ctx = auth_ctx
        self._path = f'/api/1/scanning/scanners/{self._auth_ctx.device_id}/destinations'
        self._destination_cache = {}

    def list(self):
        """
        Retrieve a list of scan destinations.

        :return: A list of registered scan destinations.
        """
        method = 'GET'
        return self._auth_ctx.send(method, self._path)

    def add(self, name, destination, type_='mail'):
        """
        Register a new scan destination.

        :param name: Alias name for the scan destination.
        :param destination: The actual destination (email or URL).
        :param type_: Type of the destination. Defaults to 'mail'. Can be 'mail' or 'url'.

        :return: Response dictionary containing details of the added destination.
        """
        method = 'POST'

        self._validate_destination(name, destination, type_)

        data = {
            'alias_name': name,
            'type': type_,
            'destination': destination,
        }

        resp = self._auth_ctx.send(method, self._path, json=data)
        self._destination_cache[resp['id']] = resp
        return resp

    def update(self, id_, name=None, destination=None, type_=None):
        """
        Update an existing scan destination.

        :param id_: ID of the scan destination to be updated.
        :param name: New alias name for the scan destination.
        :param destination: The new destination (email or URL).
        :param type_: New type of the destination. Can be 'mail' or 'url'.

        :return: Response dictionary containing details of the updated destination.
        """
        method = 'POST'

        dest_cache = self._destination_cache.get(id_)
        if dest_cache is None:
            raise ScannerError('Scan destination is not yet registered.')

        self._validate_destination(name, destination, type_)

        data = {
            'id': id_,
            'alias_name': name if name else dest_cache['alias_name'],
            'type': type_ if type_ else dest_cache['type'],
            'destination': destination if destination else dest_cache['destination'],
        }

        resp = self._auth_ctx.send(method, self._path, json=data)
        self._destination_cache[id_] = resp
        return resp

    def remove(self, id_):
        """
        Remove a scan destination.

        :param id_: ID of the scan destination to be removed.
        """
        method = 'DELETE'

        data = {
            'id': id_,
        }

        self._auth_ctx.send(method, self._path, json=data)
        del self._destination_cache[id_]

    def _validate_destination(self, name, destination, type_):
        """
        Internal method to validate scan destination details.

        :param name: Alias name for the scan destination.
        :param destination: The destination (email or URL).
        :param type_: Type of the destination. Can be 'mail' or 'url'.

        :raises ScannerError: If validation fails.
        """
        if len(name) < 1 or len(name) > 32:
            raise ScannerError('Scan destination name too long.')

        if len(destination) < 4 or len(destination) > 544:
            raise ScannerError('Scan destination too long.')

        if type_ not in self.VALID_DESTINATION_TYPES:
            raise ScannerError(f'Invalid scan destination type {type_}.')


class ScannerError(ValueError):
    """
    Error raised for scanner-specific exceptions.

    This includes cases like invalid destination type, name or destination length issues, etc.
    """
    pass
