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

from threading import RLock
from typing import Any, Dict, Iterable

class StorageObject:
    """Thread-safe in-memory storage for key-value pairs."""
    def __init__(self) -> None:
        """Initialize the storage with an empty dict and a reentrant lock."""
        self._data: Dict[str, Any] = {}
        self._lock: RLock = RLock()

    def set(self, key: str, value: Any) -> None:
        """Store a value under the given key.
        
        Parameters
        ----------
        key : str
            The key under which to store the value.
        value : Any
            The value to store.
        """
        with self._lock:
            self._data[key] = value

    def set_many(self, data: Dict[str, Any]) -> None:
        """Store multiple key-value pairs at once.
        
        Parameters
        ----------
        data : Dict[str, Any]
            Dictionary of key-value pairs to store.
        """
        with self._lock:
            for key, value in data.items():
                self._data[key] = value

    def has(self, key: str) -> bool:
        """Check if a key exists in storage.
        
        Parameters
        ----------
        key : str
            The key to check for presence.
        
        Returns
        -------
        bool
            True if the key exists, False otherwise.
        """
        with self._lock:
            return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve the value for a given key, or default if not found.
        
        Parameters
        ----------
        key : str
            The key whose value to retrieve.
        default : Any, optional
            Value to return if key is missing, by default None.
        
        Returns
        -------
        Any
            Value stored under key, or default.
        """
        with self._lock:
            return self._data.get(key, default)

    def get_many(
        self,
        keys: Iterable[str],
        default: Any = None
    ) -> Dict[str, Any]:
        """Retrieve multiple values for given keys.

        Parameters
        ----------
        keys : Iterable[str]
            Iterable of keys to retrieve.
        default : Any, optional
            Value to return for missing keys, by default None.

        Returns
        -------
        Dict[str, Any]
            Dictionary mapping keys to their values or default.
        """
        with self._lock:
            return {key: self._data.get(key, default) for key in keys}

    def remove(self, key: str) -> None:
        """Remove a key and its value from storage if present.
        
        Parameters
        ----------
        key : str
            The key to remove.
        """
        with self._lock:
            self._data.pop(key, None)