import requests
from requests.adapters import HTTPAdapter, Retry
from typing import Literal

# Constants
API_URL = "https://challenge.crossmint.io/api"
CANDIDATE_ID = "95d446bf-5b0b-4805-bd71-d9e131343ba0"
PHASE_1_GRID_SIZE = 10
PHASE_2_GRID_SIZE = 30
# since phase 2 grid is not perfectly centered, there is an offset
PHASE_2_GRID_OFFSET = 4

# Unofficial "types"
SOLOON_COLOR = Literal["blue", "red", "purple", "white"]
COMETH_DIRECTION = Literal["up", "down", "left", "right"]

# Retry session to mitigate 429 Responses when querying the POST /polyanet endpoint
# (No "Retry-after" param in response headers, so using exponential backoff)
# Docs: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429], allowed_methods=["POST"])
s.mount("https://", HTTPAdapter(max_retries=retries))


def create_polyanet_at(row: int, column: int) -> None:
    """Sends a POST request to Challenge API to create polyanet at given row/column coordinates.

    Keyword arguments-
    row: position on y axis of polyanet grid.
    column: position on x axis of polyanet grid.

    """
    endpoint = f"{API_URL}/polyanets"
    body = {"candidateId": CANDIDATE_ID, "row": row, "column": column}
    response = s.post(endpoint, json=body)
    if response.status_code != 200:
        print(f"POST request for '/polyanet' failed: {response.text}")


def create_soloon_at(row: int, column: int, color: SOLOON_COLOR) -> None:
    """Sends a POST request to Challenge API to create soloon at given row/column coordinates, with
    given color.

    Keyword arguments-
    row: position on y axis of polyanet grid.
    column: position on x axis of polyanet grid.
    color: color of soloon entity.

    """
    endpoint = f"{API_URL}/soloons"
    body = {"candidateId": CANDIDATE_ID, "row": row, "column": column, "color": color}
    response = s.post(endpoint, json=body)
    if response.status_code != 200:
        print(f"POST request for '/polyanet' failed: {response.text}")


def create_cometh_at(row: int, column: int, direction: COMETH_DIRECTION) -> None:
    """Sends a POST request to Challenge API to create cometh at given row/column coordinates, with
    given direction.

    Keyword arguments-
    row: position on y axis of polyanet grid.
    column: position on x axis of polyanet grid.
    direction: direction of cometh entity.

    """
    endpoint = f"{API_URL}/comeths"
    body = {"candidateId": CANDIDATE_ID, "row": row, "column": column, "direction": direction}
    response = s.post(endpoint, json=body)
    if response.status_code != 200:
        print(f"POST request for '/polyanet' failed: {response.text}")


def create_polyanet_across() -> None:
    """Creates the X-shape polyanet grid for Phase 1 of the Challenge."""
    for i in range(2, 9):
        create_polyanet_at(i, i)
        create_polyanet_at(PHASE_1_GRID_SIZE - i, i)


# Goal map endpoint: https://challenge.crossmint.io/api/map/95d446bf-5b0b-4805-bd71-d9e131343ba0/goal


def create_crossmint_logo() -> None:
    """Creates the Phase 2 grid in the shape of the Crossmint logo."""
    # TODO
    # planets are symmetrical over x and y axis
    # 7 comets going left, 6 going the other directions
    # 6 red moons, 7 purple/white, 8 blue


def main() -> None:
    # Phase 1
    create_polyanet_across()


if __name__ == "__main__":
    main()
