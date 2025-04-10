import pytest
from unittest.mock import patch, Mock
from usdaQuery.usda_food_query import UsdaFoodQuery, NoResultsFound
from requests.exceptions import RequestException

@patch("usdaQuery.usda_food_query.requests.get")
def test_search_success(mock_get):
    mock_get.return_value = Mock(
        json=lambda: {"foods": [{"name": "apple"}]},
        raise_for_status=lambda: None
    )

    query = UsdaFoodQuery(api_key="dummy")
    result = query.search_food("apple")

    assert result == [{"name": "apple"}]

@patch("usdaQuery.usda_food_query.requests.get")
def test_search_no_results(mock_get):
    mock_get.return_value = Mock(
        json=lambda: {"foods": []},
        raise_for_status=lambda: None
    )

    query = UsdaFoodQuery(api_key="dummy")
    with pytest.raises(NoResultsFound):
        query.search_food("no_such_food")

@patch("usdaQuery.usda_food_query.requests.get")
def test_search_request_exception(mock_get):
    mock_get.side_effect = RequestException("network down")

    query = UsdaFoodQuery(api_key="dummy")
    result = query.search_food("apple")

    assert result is None  # vagy assert, amit elvársz

