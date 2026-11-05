import unittest
from app import analyze
class Tests(unittest.TestCase):
    def test_healthy(self):
        self.assertTrue(analyze({"packages":[{"name":"requests","version":"2.32.0"}]})["healthy"])
    def test_duplicate_normalization(self):
        self.assertFalse(analyze({"packages":[{"name":"my_pkg","version":"1.0"},{"name":"my-pkg","version":"1.0"}]})["healthy"])
    def test_unpinned(self):
        self.assertFalse(analyze({"packages":[{"name":"requests","version":">=2"}]})["healthy"])
    def test_bad_schema(self):
        with self.assertRaises(ValueError): analyze({"packages":{}})
if __name__=="__main__": unittest.main()
