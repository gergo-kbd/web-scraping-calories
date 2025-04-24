import requests

with open("api_key.txt", "r") as file:
        API_KEY = file.read().strip()

class UsdaFoodQuery:

    BASE_URL = "https://api.nal.usda.gov/fdc/v1/" #foods/search

    def __init__(self, api_key):
        self.api_key = api_key
        
    def search_food(self, query, page_size = 5, data_type=None):
        url = f"{self.BASE_URL}/foods/search"
        
        params = {
            "api_key": self.api_key,
            "query": query,
            "pageSize": page_size,
        }

        # "Branded", "Survey (FNDDS)", "Foundation"
        if data_type:
            if isinstance(data_type, list):
                params["dataType"] = data_type
            else:
                params["dataType"] = [data_type]
    
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if "foods" not in data or len(data["foods"]) == 0:
                raise NoResultsFound(f"No hit for '{query}'.")

            return data["foods"]

        except NoResultsFound as e:
            print("Search results:", e)
            raise
        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
        except Exception as e:
            print("General error:", e)
            raise

class NoResultsFound(Exception):
    #If there is no hit
    pass