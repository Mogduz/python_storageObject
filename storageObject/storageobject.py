import threading

"""
File: storageobject.py
Author: Mogduz
Created: 2025-04-12
Description: 
    The StorageObject class provides a thread-safe in-memory storage mechanism that encapsulates
    a Python dictionary. It is designed to support basic operations for setting, retrieving, and 
    removing key-value pairs in a concurrent environment. The class uses a reentrant lock to ensure 
    thread safety, preventing race conditions when multiple threads access or modify the storage 
    simultaneously. In addition to single-item operations, StorageObject also supports batch 
    operations for setting, retrieving, and removing multiple items at once. This makes it a versatile 
    and robust component for use in applications that require shared state or caching mechanisms 
    in multi-threaded scenarios.
Version: 1.0
License: MIT License
"""

class StorageObject:
    # Initializes the StorageObject instance with an empty dictionary and a reentrant lock
    def __init__(self) -> None:
        """
        Initializes the StorageObject instance.

        Creates an empty dictionary to hold key-value pairs and a reentrant lock 
        to ensure thread safety during operations.
        """
        self._data_: dict = dict()
        self._lock_: threading.RLock = threading.RLock()  # Reentrant lock for thread safety

    # Sets a value for a given key in the storage
    def set(self, key: str, value: any) -> None:
        """
        Sets a value for the specified key.

        Args:
            key: The key for which the value should be set.
            value: The value to associate with the key.

        Returns:
            None
        """
        with self._lock:
            self._data[key] = value

    # Checks whether a key exists in the storage
    def has(self, key: str) -> bool:
        """
        Checks if the specified key exists in the storage.

        Args:
            key: The key to check for existence.

        Returns:
            True if the key is present in the storage, False otherwise.
        """
        with self._lock:
            return key in self._data

    # Retrieves the value associated with a given key, returning default if not present
    def get(self, key: str, default: any = None) -> any:
        """
        Retrieves the value for the given key.

        Args:
            key: The key whose value should be returned.
            default: The value to return if the key is not found (default is None).

        Returns:
            The value associated with the key if it exists; otherwise, the default value.
        """
        with self._lock:
            if self.has(key=key):
                return self._data.get(key, default)
            return default

    # Removes a key-value pair from the storage if it exists
    def remove(self, key: str) -> None:
        """
        Removes the key-value pair for the specified key.

        If the key exists, it is removed; otherwise, no action is taken.

        Args:
            key: The key of the key-value pair to remove.

        Returns:
            None
        """
        with self._lock:
            if self.has(key=key):
                del self._data[key]

    # Sets multiple key-value pairs from a given mapping
    def set_many(self, mapping: dict[str, any]) -> None:
        """
        Sets multiple key-value pairs at once.

        Inserts all key-value pairs from the provided mapping.
        This is equivalent to calling the 'set' method for each key-value pair under one lock.

        Args:
            mapping: A dictionary containing key-value pairs to add to the storage.

        Returns:
            None
        """
        with self._lock:
            for key, value in mapping.items():
                self._data[key] = value

    # Retrieves values for multiple keys either as a list or dictionary based on the 'withKeys' parameter
    def get_many(self, keys: list[str], defaults: any = None, withKeys: bool = False) -> list | dict:
        """
        Retrieves the values for multiple keys.

        Args:
            keys: A list of keys whose values should be retrieved.
            defaults: The default value to use if a key is not found.
            withKeys: If True, returns a dictionary mapping each key to its value;
                      if False, returns a list of values.

        Returns:
            A list or dictionary of the retrieved key-value pairs.
        """
        if withKeys:
            result: dict = dict()
        else:
            result: list = list()

        if isinstance(keys, list) and keys:
            with self._lock:
                for key in keys:
                    if withKeys:
                        result[key] = self.get(key=key, default=defaults)
                    else:
                        result.append(self.get(key=key, default=defaults))
        return result

    # Removes multiple key-value pairs from the storage for a list of keys
    def remove_many(self, keys: list[str]) -> None:
        """
        Removes multiple key-value pairs based on the provided list of keys.

        For each key in the list, the key-value pair is removed if it exists.

        Args:
            keys: A list of keys corresponding to the key-value pairs to remove.

        Returns:
            None
        """
        if isinstance(keys, list) and keys:
            with self._lock:
                for key in keys:
                    if self.has(key=key):
                        self.remove(key=key)

    # Getter for the internal reentrant lock to ensure thread safety
    @property
    def _lock(self) -> threading.RLock:
        """
        Provides access to the internal reentrant lock.

        Returns:
            The reentrant lock used for ensuring thread safety.
        """
        return self._lock_

    # Getter for the internal storage dictionary containing key-value pairs
    @property
    def _data(self) -> dict:
        """
        Provides access to the internal storage dictionary.

        Returns:
            The dictionary containing all key-value pairs.
        """
        return self._data_
