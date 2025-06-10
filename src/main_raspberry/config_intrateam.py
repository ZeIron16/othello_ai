HOST = 'localhost'
PORT = 4321
AI_PORT = 12345
AUDIO_PORT = 12346  
BUFFER_SIZE = 4096
TIMEOUT = 60

# Board
BOARD_COLUMNS = [chr(i) for i in range(ord('A'), ord('H') + 1)]  # ['A', 'B', ..., 'H']
BOARD_ROWS = [str(i) for i in range(1, 9)]  # ['1', '2', ..., '8']


# Intra-group communication header
INTRA_GROUP_CODES = {
    "ASK_POSITION": 0,
    "INTRA_STATUS_OK": 1,
    "INTRA_INVALID_MOVE": 2,
    "INTRA_TIME_OUT": 3,
    "INTRA_WRONG_FORMAT": 4,
    "INTRA_MOVE": 5,
    "INTRA_END_GAME": 6,
    "INTRA_RESIGN": 7,
    "INTRA_OFFER_DRAW": 8,
    "INTRA_REQUEST_UNDO": 9,
    "INTRA_RESPONSE_REQUEST": 10
}