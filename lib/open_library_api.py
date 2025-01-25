import requests
import json


class Search:
    BASE_URL = "https://openlibrary.org/search.json"

    def _format_query(self, search_term, fields, limit):
        """Helper method to format the query parameters."""
        search_term_formatted = search_term.replace(" ", "+")
        fields_formatted = ",".join(fields)
        return f"{self.BASE_URL}?title={search_term_formatted}&fields={fields_formatted}&limit={limit}"

    def get_search_results(self):
        """Fetch search results as plain content."""
        try:
            URL = self._format_query("the lord of the rings", ["title", "author_name"], 1)
            response = requests.get(URL)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.content
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def get_search_results_json(self):
        """Fetch search results and return them as JSON."""
        try:
            URL = self._format_query("the lord of the rings", ["title", "author_name"], 1)
            response = requests.get(URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_user_search_results(self, search_term, limit=1):
        """Fetch search results for a user-specified query."""
        try:
            URL = self._format_query(search_term, ["title", "author_name"], limit)
            response = requests.get(URL)
            response.raise_for_status()
            data = response.json()

            if not data.get("docs"):  # Check if no results are found
                return f"No results found for '{search_term}'."

            # Format the first result for display
            title = data["docs"][0].get("title", "Unknown Title")
            author = data["docs"][0].get("author_name", ["Unknown Author"])[0]
            return f"Title: {title}\nAuthor: {author}"
        except requests.RequestException as e:
            return f"An error occurred: {e}"


# Uncomment below lines to test the methods
# results = Search().get_search_results()
# print(results)

# results_json = Search().get_search_results_json()
# print(json.dumps(results_json, indent=1))

# Prompt user for input and fetch results
search_term = input("Enter a book title: ")
result = Search().get_user_search_results(search_term)
print("\nSearch Result:\n")
print(result)
