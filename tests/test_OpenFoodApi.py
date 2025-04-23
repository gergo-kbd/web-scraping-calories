import pytest
from unittest.mock import patch, Mock
from OpenFoodApi.OpenFoodQuery import *

@pytest.fixture
def api():
    return OpenFoodQuery

def test_get_product_success(api):
    mock_response = {
        "status": 1,
        "product": {
            "product_name": "Test Product",
            "code": "1234567890123"
        }
    }

    with patch("OpenFoodApi.OpenFoodQuery.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response
        
        product = api.get_product("1234567890123")
        assert product["product_name"] == "Test Product"

def test_get_product_not_found(api):
    mock_response = {
        "status": 0
    }

    with patch("OpenFoodApi.OpenFoodQuery.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response

        with pytest.raises(ProductNotFoundError):
            api.get_product("0000000000000")

def test_get_product_api_error(api):
    with patch("OpenFoodApi.OpenFoodQuery.requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")

        with pytest.raises(OpenFoodFactsAPIError):
            api.get_product("1234567890123")

def test_search_products(api):
    mock_response = {
        "products": [
            {"product_name": "Product A", "code": "111"},
            {"product_name": "Product B", "code": "222"}
        ]
    }

    with patch("OpenFoodApi.OpenFoodQuery.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response

        results = api.search_products("apple")
        assert "products" in results
        assert len(results["products"]) == 2