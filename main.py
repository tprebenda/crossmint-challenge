import requests
from requests.adapters import HTTPAdapter, Retry

# Constants
API_URL = "https://challenge.crossmint.io/api"
CANDIDATE_ID = "95d446bf-5b0b-4805-bd71-d9e131343ba0"
PHASE_1_GRID_SIZE = 10
PHASE_2_GRID_SIZE = 30

# Retry session to mitigate 429 Responses when querying the POST /polyanet endpoint
# (No "Retry-after" param in response headers, so using exponential backoff)
# Docs: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429], allowed_methods=["POST"])
s.mount("https://", HTTPAdapter(max_retries=retries))


def post_polyanet(row: int, column: int) -> None:
    """Sends a POST request to Challenge API to create polyanet at given row/column coordinates.

    Keyword arguments-
    row (int): position on y axis of polyanet grid.
    column (int): position on x axis of polyanet grid.

    """
    endpoint = f"{API_URL}/polyanets"
    body = {"candidateId": CANDIDATE_ID, "row": row, "column": column}
    response = s.post(endpoint, json=body)
    if response.status_code != 200:
        print(f"POST request for '/polyanet' failed: {response.text}")


def create_polyanet_across() -> None:
    """Creates the X-shape polyanet grid for Phase 1 of the Challenge."""
    for coordinate in range(2, 9):
        post_polyanet(coordinate, coordinate)
        post_polyanet(PHASE_1_GRID_SIZE - coordinate, coordinate)


# Goal map endpoint: https://challenge.crossmint.io/api/map/95d446bf-5b0b-4805-bd71-d9e131343ba0


def create_crossmint_logo() -> None:
    """Creates the Phase 2 grid in the shape of the Crossmint logo."""
    # TODO


def main():
    create_polyanet_across()


if __name__ == "__main__":
    main()
