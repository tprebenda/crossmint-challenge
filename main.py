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

# Literals
ASTRAL_ENTITY = Literal["polyanet", "soloon", "cometh"]
SOLOON_COLOR = Literal["blue", "red", "purple", "white"]
COMETH_DIRECTION = Literal["up", "down", "left", "right"]

# Retry session to mitigate 429 Responses when querying the POST /polyanet endpoint
# (No "Retry-after" param in response headers, so using exponential backoff)
# Docs: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429], allowed_methods=["POST"])
s.mount("https://", HTTPAdapter(max_retries=retries))


def generate_astral_entity(
    entity: ASTRAL_ENTITY,
    row: int,
    column: int,
    color: SOLOON_COLOR = None,
    direction: COMETH_DIRECTION = None,
) -> None:
    """
    Sends a POST request to Challenge API to create a polyanet, soloon, or cometh at given row/column
    coordinates in the grid.

        Parameters:
            entity: type of entity to create. Must be one of ["polyanet", "soloon", "cometh"].
            row: position on y axis of grid.
            column: position on x axis of grid.
            color: color to use for soloon creation. Must be one of ["blue", "red", "purple", "white"].
                Default: None
            direction: dirction to use for cometh creation. Must be one of \
            ["up", "down", "left", "right"]
                Default: None

        Returns:
            None

        Exceptions:
            ValueError raised when saloon color or cometh direction not provided when placing \
            those entities, or when both arguments are provided.
    """
    if (entity == "soloon" and not color) or (entity == "cometh" and not direction):
        raise ValueError(
            "Missing arguments for entity placement. Soloons must have a valid color, "
            + "and comeths must have a valid direction."
        )
    if color and direction:
        raise ValueError("Only one of 'color' and 'direction' should be provided")

    endpoint = f"{API_URL}/{entity}s"
    body = {"candidateId": CANDIDATE_ID, "row": row, "column": column}
    if color:
        body["color"] = color
    if direction:
        body["direction"] = direction
    response = s.post(endpoint, json=body)
    if response.status_code != 200:
        print(f"POST request to '/{entity}s' failed: {response.text}")


def create_polyanet_across() -> None:
    """Creates the X-shape polyanet grid for Phase 1 of the Challenge."""
    for i in range(2, 9):
        generate_astral_entity(entity="polyanet", row=i, column=i)
        generate_astral_entity(entity="polyanet", row=PHASE_1_GRID_SIZE - i, column=i)


# Goal map endpoint: https://challenge.crossmint.io/api/map/95d446bf-5b0b-4805-bd71-d9e131343ba0/goal


def create_crossmint_logo() -> None:
    """Creates the Phase 2 grid in the shape of the Crossmint logo."""
    # TODO
    # planets are symmetrical over x and y axis
    # 7 comets going left, 6 going the other directions
    # 6 red moons, 7 purple/white, 8 blue

    # NEED TO LOOK INTO MODULO VALUES...
    # Planets are usually in pairs of two, so something % 2??


def main() -> None:
    # Phase 1
    create_polyanet_across()


if __name__ == "__main__":
    main()
