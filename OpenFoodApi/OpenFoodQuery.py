import requests
import json
from typing import List, Optional, Dict


class OpenFoodQuery:
    BASE_URL = "https://world.openfoodfacts.org/api/v2"

    def __init__(self, language: str = "en") -> None:
        # lang for the API response
        self.language = language

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        
        url = f"{self.BASE_URL}{endpoint}"
        try:
            
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        
        except requests.exceptions.HTTPError as e:

            raise Exception(f"API request failed: {e}")
        
        except requests.exceptions.RequestException as e:

            raise Exception(f"Network error: {e}")

    def get_product(self, barcode: str) -> Optional[Dict]:
       
        endpoint = f"/product/{barcode}.json"
        data = self._get(endpoint)
        
        if data["status"] == 1:  # Product found
            return data["product"]
        else:
            return None

    def search_products(self, search_term: str, page: int = 1, page_size: int = 20) -> Dict:
        
        endpoint = "/cgi/search.pl"

        params = {
            "search_terms": search_term,
            "search_simple": 1,  # Use simple search
            "action": "process",
            "json": 1,
            "page": page,
            "page_size": page_size,
            "fields": "code,product_name,brands,quantity,nutriments,image_front_small_url", # Specify fields to return
            "lc": self.language  # Language code
        }
        return self._get(endpoint, params)