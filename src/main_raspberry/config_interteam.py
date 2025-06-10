# config.py

# Valid player colors
VALID_PLAYERS = ["B", "W"]

# Valid board columns and rows
VALID_COLUMNS = ["A", "B", "C", "D", "E", "F", "G", "H"]
VALID_ROWS = [str(i) for i in range(1, 9)]

# Special move string
SPECIAL_MOVE = "NONE"

# Message codes (positive: action, negative: response)
CODES = {
    "INIT": 0,
    "MOVE": 1,
    "END": 2,
    "RESIGN": 3,
    "TIMEOUT": 4,
    "OK": -1,
    "INTERNAL_ERROR": -2,
    "ILLEGAL_MOVE": -3,
    "FORMAT_ERROR": -5,
    "MOVE_LOST": -6,
    "ABORT": -7
}
