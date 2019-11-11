import unittest
from caches import FileCache, NullCache
import os


class TestFileCache(unittest.TestCase):
    test_file_cache_path = "test_file_cache"
    test_file_with_data_path = os.path.join("tests", "data", "file_cache_with_data")

    def setUp(self):
        self.delete_cache_file_is_exists()

    def tearDown(self):
        self.delete_cache_file_is_exists()

    def delete_cache_file_is_exists(self):
        if os.path.exists(self.test_file_cache_path):
            os.remove(self.test_file_cache_path)

    def test_create_file_cache(self):
        FileCache(self.test_file_cache_path)
        self.assertTrue(os.path.isfile(self.test_file_cache_path))

    def test_file_cache_is_empty_when_created(self):
        cache = FileCache(self.test_file_cache_path)
        self.assertEqual(len(cache), 0)

    def test_store_element(self):
        cache = FileCache(self.test_file_cache_path)
        cache.store("url1")
        self.assertEqual(len(cache), 1)
        self.assertTrue("url1" in cache)

    def test_cache_contains_data_from_file_when_created(self):
        cache = FileCache(self.test_file_with_data_path)
        self.assertTrue("old url 1" in cache)
        self.assertTrue("another old url" in cache)

    def test_cache_is_emptied_when_clear_is_called(self):
        cache = FileCache(self.test_file_with_data_path)
        self.assertGreater(len(cache), 0)

        cache.clear()
        self.assertEqual(len(cache), 0)

    def test_cache_is_persisted_on_file_when_save_is_called(self):
        path = self.test_file_cache_path
        new_elements = ["test url 1", "test url 2", "test url 3"]
        cache = FileCache(path)

        self.store_elements_in_cache(cache, new_elements)
        cache.save()
        self.assert_cache_file_contains_elements(new_elements, path)

    def assert_cache_file_contains_elements(self, new_lines, path):
        with open(path) as f:
            file_lines = [line.strip() for line in f.readlines()]
            self.assertEqual(new_lines, file_lines)

    def store_elements_in_cache(self, cache, new_lines):
        for line in new_lines:
            cache.store(line)


class TestNullCache(unittest.TestCase):
    def setUp(self):
        self.cache = NullCache()

    def test_is_created_empty(self):
        self.assertEqual(len(self.cache), 0)

    def test_is_always_empty(self):
        self.cache.store("element")
        self.assertEqual(len(self.cache), 0)


if __name__ == '__main__':
    unittest.main()