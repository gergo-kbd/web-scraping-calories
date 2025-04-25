from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class FoodNutrient:
    name: str
    amount: float
    unit: str

@dataclass
class FoodItem:
    fdc_id: int
    description: str
    data_type: str
    category: Optional[str]
    nutrients: Dict[str, FoodNutrient]


    @staticmethod
    def from_dict(food_dict: Dict) -> List["FoodItem"]:
        food_items = food_dict.get("foods", [])
        result = []

        for food_item in food_items:
            nutrients = {
                n["nutrientName"]: FoodNutrient(
                    name = n["nutrientName"],
                    amount = n.get("value", 0.0),
                    unit = n.get("unitName", "")
                )
                for n in food_item.get("foodNutrients", [])
            }

        result.append(
            FoodItem(
            fdc_id=food_item.get("fdcId", 0),
            description=food_item.get("description", "Unknown Description"),
            data_type=food_item.get("dataType", "Unknown DataType"),
            category=food_item.get("foodCategory", None),
            nutrients=nutrients
            )
        )
        return result
'''
nutrients = {
            n["nutrientName"]: FoodNutrient(
                name=n["nutrientName"],
                amount=n.get("value", 0.0),
                unit=n.get("unitName", "")
            )
            for n in food_item.get("foodNutrients", [])
        }
'''