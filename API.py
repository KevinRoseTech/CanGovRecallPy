import requests

class RecallsAPI:
    BASE_URL = "http://healthycanadians.gc.ca/recall-alert-rappel-avis/api"

    @staticmethod
    def search_recalls(search_text, language='en', category=None, limit=5, offset=0):
        """
        Search the recalls database based on provided criteria.

        :param search_text: The text string to search the database for
        :param language: The language of the search results ('en' for English, 'fr' for French)
        :param category: The category to filter the search by
        :param limit: The maximum number of results to return
        :param offset: The offset from the start of the results
        :return: A dictionary containing the search results
        """
        # Construct the search URL with query parameters
        search_url = f"{RecallsAPI.BASE_URL}/search?search={search_text}&lang={language}&lim={limit}&off={offset}"
        if category:
            search_url += f"&cat={category}"

        # Make the GET request
        response = requests.get(search_url)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                print("Failed to decode JSON response.")
        else:
            print(f"Failed to fetch search results: {response.status_code}")
        return {}

# Example usage:
if __name__ == "__main__":
    results = RecallsAPI.search_recalls("peanuts", category="1")
    print(results)
