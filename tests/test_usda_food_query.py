import unittest
from unittest.mock import patch
#from usda_food_query import UsdaFoodQuery, NoResultsFound
from usdaQuery.usda_food_query import *

class TestUsdaFoodQuery(unittest.TestCase):

    def setUp(self):
        self.api_key = "fake_api_key"
        self.query = UsdaFoodQuery(api_key=self.api_key)

    @patch("usdaQuery.usda_food_query.requests.get")
    def test_search_food_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "foods": [
                {"description": "Banana", "fdcId": 123},
                {"description": "Apple", "fdcId": 456}
            ]
        }

        result = self.query.search_food("banana")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["description"], "Banana")

    @patch("usdaQuery.usda_food_query.requests.get")
    def test_search_food_no_results(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "foods": []
        }

        with self.assertRaises(NoResultsFound):
            self.query.search_food("nonexistentfood")

    @patch("usdaQuery.usda_food_query.requests.get")
    def test_search_food_request_exception(self, mock_get):
        mock_get.side_effect = Exception("API down")

        with self.assertRaises(Exception):
            self.query.search_food("banana")
