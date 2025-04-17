import unittest
import threading
from storageObject.storageobject import StorageObject

class TestStorageObject(unittest.TestCase):
    def setUp(self):
        self.store = StorageObject()

    def test_set_and_get(self):
        self.store.set('foo', 123)
        self.assertTrue(self.store.has('foo'))
        self.assertEqual(self.store.get('foo'), 123)

    def test_override_value(self):
        self.store.set('foo', 1)
        self.assertEqual(self.store.get('foo'), 1)
        self.store.set('foo', 2)
        self.assertEqual(self.store.get('foo'), 2)

    def test_store_none_and_default_logic(self):
        self.store.set('none_key', None)
        self.assertTrue(self.store.has('none_key'))
        self.assertIsNone(self.store.get('none_key', 'def'))

    def test_get_default(self):
        self.assertFalse(self.store.has('missing'))
        self.assertIsNone(self.store.get('missing'))
        self.assertEqual(self.store.get('missing', 'def'), 'def')

    def test_special_keys(self):
        for key in ['', ' ', 'ßümlaut', 'キー🔑']:
            self.store.set(key, key + '_val')
            self.assertTrue(self.store.has(key))
            self.assertEqual(self.store.get(key), key + '_val')

    def test_set_many_and_get_many(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        self.store.set_many(data)
        self.assertEqual(self.store.get('a'), 1)
        self.assertEqual(self.store.get('b'), 2)

        # expect list of values for each key, missing yields None
        result = self.store.get_many(['a', 'x'])
        self.assertEqual(result, [1, None])

        # empty list yields empty list
        self.assertEqual(self.store.get_many([]), [])

    def test_set_many_empty(self):
        before = self.store.get_many([])
        self.store.set_many({})
        self.assertEqual(self.store.get_many([]), before)

    def test_get_many_duplicates(self):
        self.store.set('dup', 42)
        result = self.store.get_many(['dup', 'dup'])
        self.assertEqual(result, [42, 42])

    def test_get_many_with_none_keys(self):
        result = self.store.get_many(None)
        self.assertEqual(result, [])

    def test_mutable_values_reference(self):
        lst = [1, 2]
        self.store.set('list', lst)
        got = self.store.get('list')
        self.assertIs(got, lst)
        got.append(3)
        self.assertEqual(self.store.get('list'), [1, 2, 3])

    def test_unhashable_key_errors(self):
        for method in (self.store.has, self.store.get, self.store.remove):
            with self.assertRaises(TypeError):
                method([])

    def test_remove(self):
        self.store.set('key', 'value')
        self.assertTrue(self.store.has('key'))
        self.store.remove('key')
        self.assertFalse(self.store.has('key'))
        self.store.remove('no_such_key')

    def test_concurrent_unique_keys(self):
        def worker(i):
            self.store.set(f'k{i}', i)
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(100)]
        for t in threads: t.start()
        for t in threads: t.join()
        for i in range(100):
            self.assertTrue(self.store.has(f'k{i}'))
            self.assertEqual(self.store.get(f'k{i}'), i)

    def test_concurrent_mixed_operations(self):
        def setter():
            for i in range(50):
                self.store.set(f'mix{i}', i)
        def remover():
            for i in range(50):
                self.store.remove(f'mix{i}')
        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=setter))
            threads.append(threading.Thread(target=remover))
        for t in threads: t.start()
        for t in threads: t.join()

        result = self.store.get_many([f'mix{i}' for i in range(50)])
        for val in result:
            self.assertTrue(val is None or isinstance(val, int))

if __name__ == '__main__':
    unittest.main()