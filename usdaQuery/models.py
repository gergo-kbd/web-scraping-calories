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
    nutrients: List[FoodNutrient]


    @staticmethod
    def from_dict(food_dict: Dict) -> "FoodItem":
        food_item = food_dict.get("foods", [])[0]

        nutrients = {
            n["nutrientName"]: FoodNutrient(
                name=n["nutrientName"],
                amount=n.get("value", 0.0),
                unit=n.get("unitName", "")
            )
            for n in food_item.get("foodNutrients", [])
        }

        
        return FoodItem(
            fdc_id=food_item.get("fdcId", 0),
            description=food_item.get("description", "Unknown Description"),
            data_type=food_item.get("dataType", "Unknown DataType"),
            category=food_item.get("foodCategory", None),
            nutrients=nutrients
        )