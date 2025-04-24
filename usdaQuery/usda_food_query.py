import requests

#BASE_URL = "https://api.nal.usda.gov/fdc/v1/" #foods/search

with open("api_key.txt", "r") as file:
        API_KEY = file.read().strip()

class UsdaFoodQuery:

    BASE_URL = "https://api.nal.usda.gov/fdc/v1/" #foods/search

    def __init__(self, api_key):
        self.api_key = api_key
        
    def search_food(self, query, page_size = 5):
        url = f"{self.BASE_URL}/foods/search"
        
        params = {
            "api_key": self.api_key,
            "query": query,
            "pageSize": page_size,
        }
    
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
        try:
            print("Response JSON: response.json())") #response.json())
        except Exception:
            print("Cannot read json from the response.")
            raise
        
        except NoResultsFound as e:
            print("Search results:", e)
            raise

        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            return None  # ha ezt várod a tesztben

        except Exception as e:
            print("General error:", e)
            raise

class NoResultsFound(Exception):
    #If there is no hit
    pass



'''
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        data = response.json()

        if "foods" not in data:
            raise Exception(f"Response has no 'foods' field: {data}")

        return data["foods"]
'''
