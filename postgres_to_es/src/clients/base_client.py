from abc import ABC, abstractmethod

from pydantic import AnyUrl


class BaseClient(ABC):
    """Base class for client."""

    def __init__(self, dsn: AnyUrl, connection: any = None):
        """Initialization of base client."""

        self.dsn = dsn
        self._connection = connection

    @property
    def connection(self) -> any:
        """Get connection for client."""

        return self._connection if self._connection else self._reconnect()

    @abstractmethod
    def _reconnect(self) -> connection:
        """Reconnect to client if no connection exists."""

        raise NotImplementedError

    def close(self) -> None:
        """Close client connection."""

        if self.connection:
            self.connection.close()
