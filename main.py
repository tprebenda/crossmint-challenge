import requests
from requests.adapters import HTTPAdapter, Retry
from typing import Literal, get_args

# Constants
API_URL = "https://challenge.crossmint.io/api"
CANDIDATE_ID = "95d446bf-5b0b-4805-bd71-d9e131343ba0"
PHASE_1_GRID_SIZE = 10
PHASE_2_GRID_SIZE = 30
PHASE_2_GRID_CENTER = 13

# Literals
ASTRAL_ENTITY = Literal["polyanet", "soloon", "cometh"]
SOLOON_COLOR = Literal["blue", "red", "purple", "white"]
COMETH_DIRECTION = Literal["up", "down", "left", "right"]
DIAGONAL_DIRECTIONS = Literal["up-right", "up-left", "down-right", "down-left"]

# Retry session to mitigate 429 Responses when querying the POST/DELETE endpoints
# (No "Retry-after" param in response headers, so using exponential backoff)
# Docs: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429], allowed_methods=["POST", "DELETE"])
s.mount("https://", HTTPAdapter(max_retries=retries))


def create_polyanet_across() -> None:
    """Creates the X-shape polyanet grid for Phase 1 of the Challenge."""
    for i in range(2, 9):
        generate_entity(entity="polyanet", row=i, column=i)
        generate_entity(entity="polyanet", row=PHASE_1_GRID_SIZE - i, column=i)


def create_crossmint_logo() -> None:
    """Creates the Phase 2 grid in the shape of the Crossmint logo."""
    # TODO
    # planets are symmetrical over x and y axis
    # 7 comets going left, 6 going the other directions
    # 6 red moons, 7 purple/white, 8 blue

    # initial cross at center
    generate_entity(entity="polyanet", row=PHASE_2_GRID_CENTER, column=PHASE_2_GRID_CENTER)
    generate_entity(entity="polyanet", row=PHASE_2_GRID_CENTER - 1, column=PHASE_2_GRID_CENTER)
    generate_entity(entity="polyanet", row=PHASE_2_GRID_CENTER, column=PHASE_2_GRID_CENTER + 1)
    generate_entity(entity="polyanet", row=PHASE_2_GRID_CENTER + 1, column=PHASE_2_GRID_CENTER)
    generate_entity(entity="polyanet", row=PHASE_2_GRID_CENTER, column=PHASE_2_GRID_CENTER - 1)

    for direction in get_args(DIAGONAL_DIRECTIONS):
        generate_leaf_for_direction(direction)


def generate_entity(
    entity: ASTRAL_ENTITY,
    row: int,
    column: int,
    color: SOLOON_COLOR = None,
    direction: COMETH_DIRECTION = None,
) -> None:
    """
    Sends a POST request to Challenge API to create a polyanet, soloon, or cometh at given row + column
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
        raise ValueError("Only one of 'color' and 'direction' should be provided.")

    endpoint = f"{API_URL}/{entity}s"
    body = {"candidateId": CANDIDATE_ID, "row": row, "column": column}
    if color:
        body["color"] = color
    if direction:
        body["direction"] = direction
    response = s.post(endpoint, json=body)
    if response.status_code != 200:
        print(f"POST request to '/{entity}s' failed: {response.text}")


def delete_entity(
    entity: ASTRAL_ENTITY,
    row: int,
    column: int,
) -> None:
    """
    Sends a DELETE request to Challenge API to remove a polyanet, soloon, or cometh at given row + column
    coordinates.

        Parameters:
            entity: type of entity to create. Must be one of ["polyanet", "soloon", "cometh"].
            row: position on y axis of grid.
            column: position on x axis of grid.

        Returns:
            None
    """

    endpoint = f"{API_URL}/{entity}s"
    body = {"candidateId": CANDIDATE_ID, "row": row, "column": column}
    response = s.delete(endpoint, json=body)
    if response.status_code != 200:
        print(f"DELETE request to '/{entity}s' failed: {response.text}")


def generate_leaf_for_direction(direction: DIAGONAL_DIRECTIONS):
    offsets = [1, 2, 3, 4, 3, 3, 2, 2, 1, 1]
    offset_idx = 0
    diagonal_coordinate_generator = diagonal_coordinates_factory(direction)
    for i in range(1, 12):
        (diagonal_r, diagonal_c) = diagonal_coordinate_generator(i)
        # print(f"{diagonal_r}, {diagonal_c}")
        # final corner point
        if i == 11:
            generate_entity(entity="polyanet", row=diagonal_r, column=diagonal_c)
            break

        coords = get_polyanet_cords_for_direction(diagonal_r, diagonal_c, offsets, offset_idx, direction)
        # print(coords)
        for row, col in coords:
            generate_entity(entity="polyanet", row=row, column=col)
        offset_idx += 1


def get_polyanet_cords_for_direction(diagonal_r, diagonal_c, offsets, offset_idx, direction):
    offset = offsets[offset_idx]
    if direction == "up-right":
        if offset_idx < 3:
            coords = [
                (diagonal_r - offset, diagonal_c),
                (diagonal_r - offset - 1, diagonal_c),
                (diagonal_r, diagonal_c + offset),
                (diagonal_r, diagonal_c + offset + 1),
            ]
        else:
            coords = [
                (diagonal_r - offset, diagonal_c),
                (diagonal_r, diagonal_c + offset),
            ]
    elif direction == "up-left":
        if offset_idx < 3:
            coords = [
                (diagonal_r - offset, diagonal_c),
                (diagonal_r - offset - 1, diagonal_c),
                (diagonal_r, diagonal_c - offset),
                (diagonal_r, diagonal_c - offset - 1),
            ]
        else:
            coords = [(diagonal_r - offset, diagonal_c), (diagonal_r, diagonal_c - offset)]
    elif direction == "down-right":
        if offset_idx < 3:
            coords = [
                (diagonal_r + offset, diagonal_c),
                (diagonal_r + offset + 1, diagonal_c),
                (diagonal_r, diagonal_c + offset),
                (diagonal_r, diagonal_c + offset + 1),
            ]
        else:
            coords = [(diagonal_r + offset, diagonal_c), (diagonal_r, diagonal_c + offset)]
    else:
        if offset_idx < 3:
            coords = [
                (diagonal_r + offset, diagonal_c),
                (diagonal_r + offset - 1, diagonal_c),
                (diagonal_r, diagonal_c - offset),
                (diagonal_r, diagonal_c - offset - 1),
            ]
        else:
            coords = [(diagonal_r + offset, diagonal_c), (diagonal_r, diagonal_c - offset)]
    return coords


def get_up_right_diagonal_coords(idx: int):
    return (PHASE_2_GRID_CENTER - idx, PHASE_2_GRID_CENTER + idx)


def get_up_left_diagonal_coords(idx: int):
    return (PHASE_2_GRID_CENTER - idx, PHASE_2_GRID_CENTER - idx)


def get_down_right_diagonal_coords(idx: int):
    return (PHASE_2_GRID_CENTER + idx, PHASE_2_GRID_CENTER + idx)


def get_down_left_diagonal_coords(idx: int):
    return (PHASE_2_GRID_CENTER + idx, PHASE_2_GRID_CENTER - idx)


def diagonal_coordinates_factory(direction: DIAGONAL_DIRECTIONS):
    diagonal_funcs = {
        "up-right": get_up_right_diagonal_coords,
        "up-left": get_up_left_diagonal_coords,
        "down-right": get_down_right_diagonal_coords,
        "down-left": get_down_left_diagonal_coords,
    }
    return diagonal_funcs[direction]


# def test(diagonal_r, diagonal_c, offsets, offset_idx, direction):
#     direction_modifier = {
#         "up-right": (1, -1),
#         "up-left": (-1, -1),
#         "down-right": (1, 1),
#         "down-left": (-1, 1),
#     }
#     offset = offsets[offset_idx]
#     if direction == "up-right":
#         row_modifier, col_modifier = direction_modifier(direction)
#         if offset_idx < 3:
#             coords = [
#                 (diagonal_r + (offset * row_modifier), diagonal_c),
#                 (diagonal_r + ((offset + 1) * row_modifier), diagonal_c),
#                 (diagonal_r, diagonal_c + ((offset) * col_modifier)),
#                 (diagonal_r, diagonal_c + ((offset + 1) * col_modifier)),
#             ]
#         else:
#             coords = [
#                 (diagonal_r + (offset * row_modifier), diagonal_c),
#                 (diagonal_r, diagonal_c + (offset * col_modifier)),
#             ]
#     return coords


def main() -> None:
    # Phase 1
    # create_polyanet_across()

    # Phase 2
    create_crossmint_logo()


if __name__ == "__main__":
    main()
