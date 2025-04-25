import pytest
from usdaQuery.models import FoodItem, FoodNutrient

@pytest.fixture
def sample_food_list():
    return [
        {
            "fdcId": 123,
            "description": "Test Banana",
            "dataType": "Foundation",
            "foodCategory": "Fruits",
            "foodNutrients": [
                {
                    "nutrientName": "Protein",
                    "value": 0.74,
                    "unitName": "G"
                },
                {
                    "nutrientName": "Fat",
                    "value": 0.3,
                    "unitName": "G"
                }
            ]
        },
        {
            "fdcId": 456,
            "description": "Test Apple",
            "dataType": "Survey (FNDDS)",
            "foodCategory": "Apples",
            "foodNutrients": []
        }
    ]

def test_from_dict_parses_items_correctly(sample_food_list):
    food_items = FoodItem.from_dict(sample_food_list)

    assert len(food_items) == 2

    banana = food_items[0]
    assert banana.fdc_id == 123
    assert banana.description == "Test Banana"
    assert banana.data_type == "Foundation"
    assert "Protein" in banana.nutrients
    assert banana.nutrients["Protein"].amount == 0.74

    apple = food_items[1]
    assert apple.fdc_id == 456
    assert apple.description == "Test Apple"
    assert apple.nutrients == {}

def test_missing_optional_fields():
    minimal_food = [
        {
            "fdcId": 999,
            "description": "Minimal",
            "dataType": "Unknown",
            "foodNutrients": []
        }
    ]
    food_items = FoodItem.from_dict(minimal_food)
    assert len(food_items) == 1
    item = food_items[0]
    assert item.category is None
    assert item.nutrients == {}

def test_handles_missing_nutrient_values_gracefully():
     input_data = [
        {
            "fdcId": 111,
            "description": "Weird Food",
            "dataType": "Foundation",
            "foodCategory": "Misc",
            "foodNutrients": [
                {"nutrientName": "Fiber"}  # no value, no unitName
            ]
        }
    ]
     
     result = FoodItem.from_dict(input_data)
     nutrient = result[0].nutrients["Fiber"]
     assert nutrient.amount == 0.0
     assert nutrient.unit == ""