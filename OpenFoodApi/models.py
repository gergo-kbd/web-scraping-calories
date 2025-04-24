from dataclasses import dataclass
from typing import Dict

@dataclass
class ProductInfo:
    name: str
    brand: str
    quantity: str
    kcal_per_100g: float
    proteins_100g: float
    carbohydrates_100g: float
    sugars_100g: float
    fat_100g: float
    saturated_fat_100g: float
    trans_fat_100g: float
    fiber_100g: float
    image_url: str

    @staticmethod
    def from_json(data: Dict) -> "ProductInfo":
        nutriments = data.get("nutriments", {})
        return ProductInfo(
            name = data.get("product_name", "N/A"),
            brand = data.get("brands", "N/A"),
            quantity = data.get("quantity", "N/A"),
            kcal_per_100g = nutriments.get('energy-kcal_100g', 'N/A'),
            proteins_100g = nutriments.get('proteins_100g', 'N/A'),
            carbohydrates_100g = nutriments.get('carbohydrates_100g', 'N/A'),
            sugars_100g = nutriments.get('sugars_100g', 'N/A'),
            fiber_100g = nutriments.get('fiber_100g', 'N/A'),
            fat_100g = nutriments.get('fat_100g', 'N/A'),
            saturated_fat_100g = nutriments.get('saturated-fat_100g', 'N/A'),
            trans_fat_100g = nutriments.get('trans-fat_100g', 'N/A'),
            image_url = data.get("image_front_small_url", "")
        )