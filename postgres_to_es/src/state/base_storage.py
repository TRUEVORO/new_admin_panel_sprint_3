from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """
    An abstract state storage.

    Allows the state to be stored and retrieved.
    The method of storing the state can vary depending on the final implementation.
    For example, it is possible to store information in a database or in a distributed file storage.
    """

    @abstractmethod
    def save_state(self, key: str, value: str) -> None:
        """Save state in storage."""

        raise NotImplementedError

    @abstractmethod
    def retrieve_state(self, key: str) -> str | None:
        """Retrieve state from storage."""

        raise NotImplementedError
