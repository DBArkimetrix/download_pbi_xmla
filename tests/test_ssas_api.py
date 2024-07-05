# tests/test_ssas_api.py
import unittest
from download_pbi_xmla import ssas_api

class TestSSASAPI(unittest.TestCase):
    def test_set_conn_string(self):
        conn_string = ssas_api.set_conn_string("server", "db", "user", "pass")
        self.assertIn("Provider=MSOLAP", conn_string)

if __name__ == '__main__':
    unittest.main()
