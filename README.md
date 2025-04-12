# python_storageObject
The StorageObject class is a thread-safe, in-memory storage solution that manages key-value pairs using Python’s built-in dictionary. It incorporates a reentrant lock (RLock) to prevent race conditions during concurrent access, ensuring data consistency even when multiple threads read or modify the data simultaneously. Designed for scenarios like caching, shared state management, and session handling, StorageObject provides a clear and concise API that maintains thread safety while efficiently managing concurrent data operations.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

You can integrate StorageObject into your project by following these steps:

1. **Clone or Download the Repository:**

    ```bash
    git clone https://github.com/Mogduz/python_storageObject.git
    cd python_storageObject
    ```

2. **Install in Development Mode:**

    Use pip to install the package in editable mode so that changes to the source code are immediately available:

    ```bash
    pip install -e .
    ```
   
   Alternatively, if the package is published on PyPI, you can install it directly:

    ```bash
    pip install storageObject
    ```

## Usage

1. **Basic Operations:**

    Import the `StorageObject` class and create an instance to perform basic operations:
    ```python
    from storageobject import StorageObject

    # Create an instance of StorageObject
    storage = StorageObject()

    # Set a value for a key
    storage.set('user', 'Alice')

    # Retrieve the value for a key
    value = storage.get('user')
    print(value)  # Output: Alice

    # Check if a key exists
    if storage.has('user'):
        print("Key 'user' exists.")

    # Remove a key-value pair
    storage.remove('user')
    ```

2. **Batch Operations:**
    You can perform operations on multiple keys at once using the batch methods:
    ```python
    # Set multiple key-value pairs
    data = {'a': 1, 'b': 2, 'c': 3}
    store.set_many(data)

    # Retrieve multiple values as a list
    values_list = store.get_many(['a', 'b', 'c'])
    print(values_list)  # Output: [1, 2, 3]

    # Retrieve multiple values as a dictionary
    values_dict = store.get_many(['a', 'b', 'c'], withKeys=True)
    print(values_dict)  # Output: {'a': 1, 'b': 2, 'c': 3}

    # Remove multiple key-value pairs
    store.remove_many(['a', 'b'])
    ```

## API Reference

### Constructor
- StorageObject()

    Creates a new instance with an internally managed dictionary and a reentrant lock.

### Methods
- `set(key: str, value: any) -> None`

    Assigns the given value to the specified key.

- `has(key: str) -> bool`

    Checks whether the specified key exists in the storage.

- `get(key: str, default: any = None) -> any`

    Retrieves the value for the given key, returning the default value if the key is not found.

- `remove(key: str) -> None`
    
    Removes the key-value pair if the key exists.

- `set_many(mapping: dict[str, any]) -> None`

    Sets multiple key-value pairs at once using the provided dictionary.

- `get_many(keys: list[str], defaults: any = None, withKeys: bool = False) -> list | dict`

    Retrieves values for a list of keys. Returns a list if withKeys is False, otherwise returns a dictionary mapping keys to their values.

- `remove_many(keys: list[str]) -> None`

    Removes multiple key-value pairs based on the provided list of keys.

### Properties

- `_lock`

    Provides access to the internal reentrant lock for thread safety.

- `_data`

    Provides access to the internal dictionary holding all key-value pairs.

## Examples


Here's a complete example demonstrating the usage of `StorageObject`:

```python
from storageobject import StorageObject

def main():
    # Create a storage instance
    store = StorageObject()

    # Set individual key-value pairs
    store.set('name', 'Bob')
    store.set('age', 30)

    # Set multiple values at once
    store.set_many({'city': 'New York', 'country': 'USA'})

    # Retrieve and print individual values
    print("Name:", store.get('name'))
    print("Age:", store.get('age'))

    # Retrieve multiple values as a dictionary
    data = store.get_many(['name', 'city'], withKeys=True)
    print("Data (as dict):", data)

    # Remove a key-value pair and verify removal
    store.remove('age')
    print("Age after removal:", store.get('age', 'Not Found'))

if __name__ == "__main__":
    main()        
```

## Running Tests
Unit tests are provided to ensure StorageObject functions correctly. To run the tests, navigate to the project's root directory and execute:
```bash
python -m unittest discover -s tests
```
Make sure you execute this command from the root directory so that the package is properly located in the PYTHONPATH.

## Contributing
Contributions are welcome! To contribute:

1. Fork the repository.

2. Create a new branch for your changes (e.g., git checkout -b feature/new-feature).

3. Commit and push your changes.

4. Open a pull request with a detailed description of your modifications.

For any questions or support, please open an issue in the repository.

## License
This project is licensed under the MIT License.