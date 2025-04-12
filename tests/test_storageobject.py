import unittest
import threading
from storageObject import StorageObject

class TestStorageObject(unittest.TestCase):
    """Test suite for the StorageObject class."""

    def setUp(self):
        """Set up a new StorageObject instance for each test."""
        self.storage = StorageObject()

    def test_set_and_get(self):
        """Test that setting a key-value pair allows retrieving the correct value."""
        self.storage.set("key1", "value1")
        self.assertEqual(self.storage.get("key1"), "value1")

    def test_get_default(self):
        """Test that get returns the default value for non-existent keys."""
        self.assertIsNone(self.storage.get("nonexistent"))
        self.assertEqual(self.storage.get("nonexistent", "default"), "default")

    def test_has(self):
        """Test that has correctly detects whether a key exists."""
        self.assertFalse(self.storage.has("key1"))
        self.storage.set("key1", "value1")
        self.assertTrue(self.storage.has("key1"))

    def test_remove(self):
        """Test that remove deletes a key-value pair."""
        self.storage.set("key1", "value1")
        self.assertTrue(self.storage.has("key1"))
        self.storage.remove("key1")
        self.assertFalse(self.storage.has("key1"))

    def test_set_many_and_get_many(self):
        """Test that setting and retrieving multiple key-value pairs works correctly."""
        mapping = {"key1": 1, "key2": 2, "key3": 3}
        self.storage.set_many(mapping)
        # Test get_many without keys: should return a list in the same order as provided keys.
        values = self.storage.get_many(["key1", "key2", "key3"])
        self.assertEqual(values, [1, 2, 3])
        # Test get_many with withKeys=True: should return a dictionary.
        values_dict = self.storage.get_many(["key1", "key2", "key3"], withKeys=True)
        self.assertEqual(values_dict, mapping)

    def test_remove_many(self):
        """Test that remove_many deletes the specified keys."""
        mapping = {"key1": 1, "key2": 2, "key3": 3, "key4": 4}
        self.storage.set_many(mapping)
        self.storage.remove_many(["key1", "key3"])
        self.assertFalse(self.storage.has("key1"))
        self.assertFalse(self.storage.has("key3"))
        self.assertTrue(self.storage.has("key2"))
        self.assertTrue(self.storage.has("key4"))

    def test_thread_safety(self):
        """
        Test thread safety by performing multiple concurrent set and get operations.

        This test runs several threads that each perform a series of set and get operations.
        It verifies that all operations complete successfully without data corruption.
        """
        num_threads = 10
        iterations = 100

        def worker(thread_id):
            for i in range(iterations):
                key = f"key-{thread_id}-{i}"
                self.storage.set(key, i)
                # Retrieve and verify the value immediately
                self.assertEqual(self.storage.get(key), i)

        threads = []
        for thread_id in range(num_threads):
            t = threading.Thread(target=worker, args=(thread_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Verify that all keys were correctly set across all threads.
        for thread_id in range(num_threads):
            for i in range(iterations):
                key = f"key-{thread_id}-{i}"
                self.assertEqual(self.storage.get(key), i)

if __name__ == '__main__':
    unittest.main()
