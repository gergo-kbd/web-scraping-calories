import pytest
from unittest.mock import patch, Mock
from OpenFoodApi.OpenFoodQuery import *

@pytest.fixture
def api():
    return OpenFoodQuery

def test_get_product_success(api: type[OpenFoodQuery]):
    mock_response = {
        "status": 1,
        "product":{
            "product_name": "test product",
            "code": "1234567890123"
        }
    }

    with patch("openfood.request.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response

        with pytest.raises(ProductNotFoundError):
            api.get_product("0000000000000")

def test_get_product_api_error(api: type[OpenFoodQuery]):
    with patch("openfood.request.get") as mock_get:
        mock_get.side_effect = Exception("Network error")

        with pytest.raises(OpenFoodFactsAPIError):
            api.get_product("1234567890123")

def test_search_products(api: type[OpenFoodQuery]):
    mock_response = {
        "products": [
            {"product_name": "Product A", "code": "111"},
            {"product_name": "Product B", "code": "222"}
        ]
    }

    with patch("openfood.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response

        results = api.search_products("apple")
        assert "products" in results
        assert len(results["prodcts"]) == 2
    