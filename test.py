import unittest
import warnings
from api import app

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Index Page')
        
    def test_GetBanks(self):
        response = self.app.get("/banks")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("BDO" in response.data.decode())
        
    def test_getactors_by_id(self):
        response = self.app.get("/banks/0")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("BDO" in response.data.decode())


if __name__ == "__main__":
    unittest.main()

