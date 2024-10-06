import requests
from requests.adapters import HTTPAdapter, Retry

# Constants
_API_URL = "https://challenge.crossmint.io/api"
_CANDIDATE_ID = "95d446bf-5b0b-4805-bd71-d9e131343ba0"
_GRID_SIZE = 10

# Retry session to avoid 429 Responses when querying the POST /polyanet endpoint
s = requests.Session()
retries = Retry(total=5, backoff_factor=2, status_forcelist=[429], allowed_methods=["POST"])

s.mount("https://", HTTPAdapter(max_retries=retries))


def create_polyanet_across() -> None:
    """Creates the X-shape polyanet grid for Phase 1 of the Challenge."""
    for coordinate in range(2, 9):
        post_polyanet(coordinate, coordinate)
        post_polyanet(_GRID_SIZE - coordinate, coordinate)


def post_polyanet(row: int, column: int) -> None:
    """Sends a POST request to Challenge API to create polyanet at given row/column coordinates.

    Keyword arguments:
    row: position on y axis of polyanet grid.
    column: position on x axis of polyanet grid.

    """
    endpoint = f"{_API_URL}/polyanets"
    body = {"candidateId": _CANDIDATE_ID, "row": row, "column": column}
    response = s.post(endpoint, json=body)
    if response.status_code != 200:
        print(f"POST request for '/polyanet' failed: {response.text}")


def main():
    create_polyanet_across()


if __name__ == "__main__":
    main()
