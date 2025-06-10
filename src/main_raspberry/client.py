from socket import *
import socket
from config_intrateam import BUFFER_SIZE, AI_PORT, AUDIO_PORT, TIMEOUT
import logging
import time

def send_message(message: str, dest_ip, dest_port):
    try:
        logging.info(f"Connecting to {dest_ip}:{dest_port}")
        with socket.socket(AF_INET, SOCK_STREAM) as cl_socket:
            cl_socket.settimeout(TIMEOUT)
            cl_socket.connect((dest_ip, dest_port))
            logging.info(f"Sending message: {message}")
            cl_socket.sendall(message.encode())
            l = []
            while True:
                try:
                    resp_part = cl_socket.recv(BUFFER_SIZE)
                    if not resp_part:
                        break
                    l.append(resp_part)
                    if len(resp_part) < BUFFER_SIZE:
                        break
                except socket.timeout:
                    logging.warning("Timeout")
                    break

            resp = b''.join(l).decode()
            logging.info(f"Received from server: {resp}")
            return resp

    except socket.timeout:
        logging.error(f"{dest_ip}:{dest_port} - Timeout")
    except Exception as e:
        logging.error(f"Error in sending message: {e}")
    return ""

def print_board(board):
    str = ""
    for i in board:
        for j in i:
            str += j + " "
        str += "\n"
    print(str)


def is_valid_move(move, board, colour):
    dic = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    y = int(move[1]) - 1
    x = dic[move[0]]
    
    if not (0 <= y < 8 and 0 <= x < 8):
        return False
    
    if board[y][x] != '.':
        return False
    
    opp = 'W' if colour == 'B' else 'B'
    directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1), (1, -1),  (1, 0),  (1, 1)]
    
    for dy, dx in directions:
        cy, cx = y + dy, x + dx
        if not (0 <= cy < 8 and 0 <= cx < 8 and board[cy][cx] == opp):
            continue
        
        cy += dy
        cx += dx
        while 0 <= cy < 8 and 0 <= cx < 8 and board[cy][cx] == opp:
            cy += dy
            cx += dx
        
        if 0 <= cy < 8 and 0 <= cx < 8 and board[cy][cx] == colour:
            return True
    
    return False


def update_board(move, board, colour):
    dic = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    y = int(move[1]) - 1
    x = dic[move[0]]
    
    board[y][x] = colour
    
    opp = 'W' if colour == 'B' else 'B'
    directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1), (1, -1),  (1, 0),  (1, 1)]

    for dy, dx in directions:
        cy, cx = y + dy, x + dx
        flips = []
        
        while 0 <= cy < 8 and 0 <= cx < 8 and board[cy][cx] == opp:
            flips.append((cy, cx))
            cy += dy
            cx += dx
        if 0 <= cy < 8 and 0 <= cx < 8 and board[cy][cx] == colour:
            for fy, fx in flips:
                board[fy][fx] = colour

'''
Old function to try to play with the AI server

def play_game_with_AI():
    board = []
    for i in range(8):
        board.append(['.','.','.','.','.','.','.','.'])
    board[3][3], board[3][4], board[4][3], board[4][4]  = 'W', 'B', 'B', 'W'
    print_board(board)

    while True:
        colour = input("Enter your colour (B/W): ")
        if colour not in ['B', 'W']:
            print("Invalid colour. Please enter 'B' or 'W'.")
        else:
            message_colour = f"5|{colour}  |"
            resp = send_message(message_colour, AI_PORT)
            if resp[0] == '4':
                print("Unknown error")
            break
    if colour == 'B':
        current_colour = 'B'
        while True:
            if current_colour == 'B':
                move = input("Enter your move (e.g., D3): ")
                if move.lower() == 'exit':
                    message_kill = f"6|  |"
                    send_message(message_kill, AI_PORT)
                    break

                move_l = []
                move_l.append(move[0])
                move_l.append(move[1])
                if not is_valid_move(move_l, board, current_colour):
                    print("Invalid move")
                    continue

                message_1 = f"5|{move}|"
                resp1 = send_message(message_1, AI_PORT)
                if resp1[0] == '4':
                    print("Unknown error")
                    break
                if resp1[0] == '1':
                    update_board(move_l, board, current_colour)
                    print_board(board)  # Fixed: was missing the board argument
                    current_colour = 'W'
                time.sleep(3)

            else:
                message_2 = "0|  |"
                resp2 = send_message(message_2, AI_PORT)
                if resp2[0] != '5':
                    print("Error in receiving bot's move... Trying again")
                    time.sleep(3)
                    continue
                move = []
                move.append(resp2[2])
                move.append(resp2[3])
                update_board(move, board, current_colour)
                print_board(board)
                current_colour = 'B'
                time.sleep(3)
    else:
        current_colour = 'B'
        while True:
            if current_colour == 'W':
                move = input("Enter your move (e.g., D3): ")
                if move.lower() == 'exit':
                    message_kill = f"6|  |"
                    send_message(message_kill, AI_PORT)
                    break

                move_l = []
                move_l.append(move[0])
                move_l.append(move[1])
                if not is_valid_move(move_l, board, current_colour):
                    print("Invalid move")
                    continue

                message_1 = f"5|{move}|"
                resp1 = send_message(message_1, AI_PORT)
                if resp1[0] == '4':
                    print("Unknown error")
                    break
                if resp1[0] == '1':
                    update_board(move_l, board, current_colour)
                    print_board(board)  # Fixed: was missing the board argument
                    current_colour = 'B'
                time.sleep(3)

            else:
                message_2 = "0|  |"
                resp2 = send_message(message_2, AI_PORT)
                if resp2[0] != '5':
                    print("Error in receiving bot's move... Trying again")
                    time.sleep(3)
                    continue
                move = []
                move.append(resp2[2])
                move.append(resp2[3])
                update_board(move, board, current_colour)
                print_board(board)
                current_colour = 'W'
                time.sleep(3)
'''

def init_AI(colour):
    """Init the AI server with the wanted colour"""
    while True:
        if colour not in ['B', 'W']:
            print("Invalid colour. Please enter 'B' or 'W'.")
        else:
            message_colour = f"5|{colour}  |"
            resp = send_message(message_colour, 'localhost', AI_PORT)
            if resp[0] == '4':
                print("Unknown error")
            break

def ask_move_AI(last_move=""):
    """Send a message with header 0 to the AI server"""
    time.sleep(3)
    counter = 0
    while True:
        message_2 = "0|  |"
        if counter > 2:
            print("Entering in critical section - Trying to take back synchronization")
            play_against_AI(last_move)
            return 0

        resp2 = send_message(message_2, 'localhost', AI_PORT)
        if resp2[0] != '5':
            print("Error in receiving bot's move... Trying again")
            time.sleep(3)
            counter += 1
        else:
            break
    move = []
    move.append(resp2[2])
    move.append(resp2[3])
    return move


def play_against_AI(move):
    """Send a message with header 5 and a move to the AI server"""
    time.sleep(3)
    while True:
        message_1 = f"5|{move}|"
        print("Message to AI: ", message_1)
        resp1 = send_message(message_1, 'localhost', AI_PORT)
        if resp1[0] == '4':
            print("Unknown error")
            break
        if resp1[0] == '1':
            break
        time.sleep(3)


def end_AI_game():
    """Close the game with AI"""
    message_kill = f"6|  |"
    send_message(message_kill, 'localhost', AI_PORT)


def validate_audio_move(move, board, colour):
    if is_valid_move(move, board, colour):
        send_message("1|  |", 'localhost', AUDIO_PORT)
        return True
    else:
        send_message("4|  |", 'localhost', AUDIO_PORT)
        print("Incorrect move")
        return False


def ask_move_audio(board, colour):
    """Same as for ask_move_AI with the audio server"""
    while True:
        message = "0|  |"
        resp = send_message(message, 'localhost', AUDIO_PORT)

        if resp[0] != '5':
            time.sleep(3)
        else:
            if validate_audio_move([resp[2], resp[3]], board, colour):
                break
            else:
                time.sleep(3)
                
    move = [resp[2], resp[3]]
    return move


if __name__ == "__main__":
    """------ Test ------"""
    logging.basicConfig(level=logging.INFO)
    board = []
    for i in range(8):
        board.append(['.','.','.','.','.','.','.','.'])
    board[3][3], board[3][4], board[4][3], board[4][4]  = 'W', 'B', 'B', 'W'
    move = ask_move_audio(board, 'B')
    

