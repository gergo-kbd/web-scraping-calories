import requests
import json
from typing import List, Optional, Dict
import logging

class OpenFoodFactsAPIError(Exception):
    pass

class ProductNotFoundError(OpenFoodFactsAPIError):
    pass

   
class OpenFoodQuery:
    BASE_URL = "https://world.openfoodfacts.org/api/v2"

    def __init__(self, language: str = "en") -> None:
        self.language = language

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        
        url = f"{self.BASE_URL}{endpoint}"

        try:
            
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        
        except requests.exceptions.HTTPError as e:

            logging.error(f"API request failed to {url} with status code {response.status_code}: {e}")

            raise OpenFoodFactsAPIError(f"API request failed: {e}")
        
        except requests.exceptions.RequestException as e:

            logging.error(f"Netwrok error during request to {url}: {e}")

            raise OpenFoodFactsAPIError(f"API request failed: {e}")

    def get_product(self, barcode: str) -> Optional[Dict]:
       
        endpoint = f"/product/{barcode}.json"

        try:
            data = self._get(endpoint)
            if data["status"] == 1: # HIT
                return data["product"]
            
            elif data["status"] == 0: # NO HIT
                logging.warning(f"Product with barcode: {barcode} not found.")
                raise ProductNotFoundError(f"Product with barcode: {barcode} not found.")
            
            else: # other error
                logging.error(f"Unexpected API response for barcode {barcode}: {data}")
                raise OpenFoodFactsAPIError(f"Unexpected API response: {data}")
            
        except OpenFoodFactsAPIError as e:
            raise

    def search_products(
        self,
        search_term: str,
        page: int = 1,
        page_size: int = 20,
        sort_by: Optional[str] = None,
        tagtype_0: Optional[str] = None,
        tag_contains_0: Optional[str] = None,
    ) -> Dict:
        
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

        if sort_by:
            params["sort_by"] = sort_by
        
        if tagtype_0 and tag_contains_0:
            params["tagtype_0"] = tagtype_0
            params["tag_contains_0"] = tag_contains_0

        '''
        sort_by (Optional[str]): The field to sort the results by (e.g., "popularity").
                                 Check the API documentation for valid values.
        tagtype_0 (Optional[str]): The type of tag to filter by (e.g., "allergens").
                                   Check the API documentation for valid values.
        tag_contains_0 (Optional[str]): Whether the product contains the tag ("contains")
                                        or not ("does_not_contain").
                                        Check the API documentation for valid values.
        '''
        return self._get(endpoint, params)