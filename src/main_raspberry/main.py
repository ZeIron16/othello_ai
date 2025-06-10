import pygame
import pygame_menu
import time
import os
from server import Server, Client
from threading import Thread
from board import Board
from gui import Gui
from config_ui import (WIDTH, HEIGHT, BLACK, WHITE, LANGUAGES, THEMES, TRANSLATIONS, DEFAULT_LANGUAGE, 
                       DEFAULT_THEME, HUMAN, COMPUTER, EXTERN, AUDIO_OPTIONS)
from menu_harrypotter import show_harry_potter_house_selector
from client import ask_move_AI, init_AI, play_against_AI, end_AI_game, ask_move_audio
from menu_end_game import show_default_end_screen, show_end_screen


EXTERN_PORT = 4321

server_ip = None
our_ip = None

server_thread = None
server_running = False

def notation_to_coords(notation):
    col_letter = notation[0].upper()
    row_number = int(notation[1])
    col = ord(col_letter) - ord('A')  # 'A' -> 0, 'B' -> 1, ...
    row = row_number - 1              # '1' -> 0, '2' -> 1, ...
    return (row, col)

def coords_to_notation(row, col):
    col_letter = chr(ord('A') + col)  # 0 -> 'A', 1 -> 'B', ...
    row_number = row + 1              # 0 -> '1', 1 -> '2', ...
    return f"{col_letter}{row_number}"

def new_show_winner(winner, theme, gui, whites, blacks):
    if theme == "Harry_Potter":
        #For Harry Potter, determine the winning house
        winner_house = None
        player1_house = getattr(gui, 'house1', None)
        player2_house = getattr(gui, 'house2', None)
        
        if winner == BLACK:
            winner_house = player1_house
        elif winner == WHITE:
            winner_house = player2_house
        
        show_end_screen(gui.screen, winner_house, player1_house=player1_house, player2_house=player2_house,
                        blacks=blacks, whites=whites, on_play_again=main, on_quit=lambda: exit())
    else:
        #For basic theme
        show_default_end_screen(gui.screen, winner, blacks=blacks, whites=whites, on_play_again=main, on_quit=lambda: exit())

def start_game(p1, p2, theme, audio):
    print(audio)
    print(f"Starting game: {p1} vs {p2} with theme {theme}")

    board = Board()
    gui = Gui(theme)
    gui.show_game()

    current_player = BLACK
    whites, blacks, _ = board.count_stones()
    gui.update(board.board, blacks, whites, current_player)
    
    if p1 == "computer":
        init_AI('B')
    elif p2 == "computer":
        init_AI('W')
    
    # Start the game loop
    if p1 == "extern" or p2 == "extern":
        run_game_loop_online(gui, board, current_player, [p1, p2], theme)
    else :
        run_game_loop(gui, board, current_player, [p1, p2], theme, audio)

def run_game_loop(gui, board, current_player, types, theme, audio):
    whites, blacks, _ = board.count_stones()
    while not board.game_over():
        valid_moves = board.get_valid_moves(current_player)
        if valid_moves:
            gui.update(board.board, blacks, whites, current_player, valid_moves)
            if types[current_player] == "human":
                if audio == False:
                    move = gui.get_mouse_input(valid_moves)
                    move2 = coords_to_notation(move[0], move[1])
                    if (current_player == 0 and types[1] == "computer") or (current_player == 1 and types[0] == "computer"):
                        play_against_AI(move2)
                else:
                    move = ask_move_audio(board.convert_board(), 'B' if current_player == BLACK else 'W')
                    move = notation_to_coords(move)
                    move2 = coords_to_notation(move[0], move[1])
                    if (current_player == 0 and types[1] == "computer") or (current_player == 1 and types[0] == "computer"):
                        play_against_AI(move2)
            else:
                move = ask_move_AI()
                move = notation_to_coords(move)
            print(move, coords_to_notation(move[0], move[1]))
            if board.apply_move(move, current_player):
                current_player = WHITE if current_player == BLACK else BLACK
                whites, blacks, _ = board.count_stones()
                gui.update(board.board, blacks, whites, current_player)
        else:
            current_player = WHITE if current_player == BLACK else BLACK
    
    if "computer" in types:
        end_AI_game()
    winner = WHITE if whites > blacks else (BLACK if blacks > whites else None)
    #Display the end game screen depending on the theme
    new_show_winner(winner, theme, gui, whites, blacks)
    

def run_game_loop_online(gui, board, current_player, types, theme):
    """Updated game loop with proper protocol handling and bug fixes"""
    global server_ip
    print(server_ip)
    server_instance = None
    client_instance = None
    game_state = "initializing"  #Game state (initializing, playing, aborted or finished)
    timeout_duration = 60
    is_server = False
    is_client = False
    historic = []
    next_packet = None

    #---------------------------- Setup server or client ----------------------------
    if types[0] == EXTERN:
        #Server is always BLACK
        is_server = True
        server_instance = Server(our_ip)
        def start_server_thread(server_instance):
            global server_thread, server_running
            if server_running:
                server_instance.stop()
                if server_thread and server_thread.is_alive():
                    server_thread.join(timeout=1)
                server_running = False
            
            #Start new server thread
            try:
                server_thread = Thread(target=server_instance.start, daemon=True)
                server_thread.start()
                server_running = True
                print(f"Server started at {our_ip}")
            except Exception as e:
                print(f"Failed to start server thread: {e}")
                server_running = False
        start_server_thread(server_instance)

    elif types[1] == EXTERN:
        #Client is always WHITE
        is_client = True
        try:
            client_instance = Client(server_ip, EXTERN_PORT)
        except Exception as e:
            print(f"Erreur with client: {e}")
            return

    #Init the client: say init code '0' to server and wait for first move, test if it is valid
    if is_client:
        print("Sending initialization message")
        max_init_attempts = 3
        init_success = False
        for init_attempt in range(max_init_attempts):
            try:
                response = client_instance.send_request("0")
                print(f"Response: {response}")
                
                if not response:
                    response = client_instance.send_request("4")
                    time.sleep(2)
                    continue
                
                #Handle response if it s the fist move
                response_str = response if isinstance(response, str) else str(response)
                if response_str.startswith("1|"):
                    parts = response_str.split("|")
                    if len(parts) == 3 and parts[2] == "B":
                        move_notation = parts[1]
                        print(f"Move received: {move_notation}")
                        try:
                            move_coords = notation_to_coords(move_notation)
                            print(f"Trying applying the move")                            
                            valid_black_moves = board.get_valid_moves(BLACK)
                            if move_coords in valid_black_moves:
                                if board.apply_move(move_coords, BLACK):
                                    whites, blacks, _ = board.count_stones()
                                    historic.append(move_notation)
                                    if types[1 - current_player] == "computer":
                                        move_str = "" + move_notation[0] + move_notation[1]
                                        play_against_AI(move_str)
                                    game_state = "playing"
                                    gui.update(board.board, blacks, whites, current_player)
                                    current_player = WHITE
                                    init_success = True
                                    break
                                else:
                                    print(f"Invalid move {move_notation}")
                                    response = client_instance.send_request("-3")
                                    time.sleep(2)
                                    continue
                            else:
                                print(f"Invalid move {move_notation}")
                                response = client_instance.send_request("-3")
                                time.sleep(2)
                                continue
                                    
                        except Exception as e:
                            print(f"Invalid move {move_notation}")
                            response = client_instance.send_request("-3")
                            time.sleep(2)
                            continue
                    else:
                        print(f"Invalid move {move_notation}")
                        response = client_instance.send_request("-5")
                        time.sleep(2)
                        continue
                            
                elif response_str.startswith("-"): #Error code from server
                    error_code = response_str
                    print(f"Error {error_code} from server")
                    if error_code == "-3":
                        response = client_instance.send_request("-7")
                    elif error_code == "-5":
                        time.sleep(2)
                        continue
                else:
                    response = client_instance.send_request("-5")
                    time.sleep(2)
                    continue
                        
            except Exception as e:
                print("Fail to init: ", e)
                time.sleep(2)
                continue
        
        if not init_success:
            return

    #Init the server: wait for client to connect and send init code '0', then send for first move
    elif is_server:
        print("Waiting for initialization")
        try:
            #Wait for "0"
            init_msg = server_instance.accept_and_respond()
            print(f"Message received: {init_msg}")
            
            #Handle message
            init_str = init_msg if isinstance(init_msg, str) else (init_msg[0] if isinstance(init_msg, list) and len(init_msg) > 0 else str(init_msg))
            if init_str.strip() == "0":
                #Compute the first move
                valid_moves = board.get_valid_moves(BLACK)
                if valid_moves:
                    #Handle AI
                    if types[BLACK] == "computer":
                        print("Calcul du premier coup par l'IA...")
                        first_move = ask_move_AI()  # NOW this happens after client connects
                        first_move_str = "" + first_move[0] + first_move[1]
                        print(f"IA a choisi le coup : {first_move}")
                    #Handle Human
                    else:
                        gui.update(board.board, 0, 0, BLACK, valid_moves)
                        print("Server (BLACK) - Select your first move")
                        move_coords = gui.get_mouse_input(valid_moves)
                        first_move = coords_to_notation(move_coords[0], move_coords[1])
                    
                    #Apply the first move
                    move_coords = notation_to_coords(first_move)
                    if board.apply_move(move_coords, BLACK):
                        time.sleep(3)
                        if types[BLACK] == "computer":
                            response = f"1|{first_move_str}|B"
                        else:
                            response = f"1|{first_move}|B"
                        server_instance.send_response(response)
                        print(f"First move sent: {response}")
                        whites, blacks, _ = board.count_stones()
                        historic.append(first_move)
                        current_player = WHITE
                        game_state = "playing"
                    else:
                        print("Error")
                        server_instance.send_response("-2")  #Internal error
                        return
                else:
                    print("Is there really no first move? Idts")
                    server_instance.send_response("-2") #Internal error
                    return
            else:
                server_instance.send_response("-5")
                return
        except Exception as e:
            print(f"Initialization Error: {e}")
            return

    whites, blacks, _ = board.count_stones()
    
    def is_game_over():
        black_moves = board.get_valid_moves(BLACK)
        white_moves = board.get_valid_moves(WHITE)
        return len(black_moves) == 0 and len(white_moves) == 0
    
    #---------------------------- Rest of the game (loop) ----------------------------
    while not board.game_over() and game_state == "playing":
        #Check for game over condition at the start of each iteration
        if is_game_over():
            print("Game over - no valid moves for either player")
            game_state = "finished"
            break
            
        valid_moves = board.get_valid_moves(current_player)
        print(valid_moves)
        print(historic)
        
        if valid_moves:
            gui.update(board.board, blacks, whites, current_player, valid_moves)
            
            #-------------- Local human player --------------
            if types[current_player] == "human":
                print(f"Player {'NOIR' if current_player == BLACK else 'BLANC'} - Human")
                gui.update(board.board, blacks, whites, current_player, valid_moves)
                
                start_time = time.time()
                move_coords = None
                while time.time() - start_time < 60: #Timeout
                    pygame.event.clear()
                    pygame.event.post(pygame.event.Event(pygame.ACTIVEEVENT, gain=1, state=1))
                    pygame.display.flip()
                    move_coords = gui.get_mouse_input(valid_moves)
                    if move_coords is not None:
                        break
                    time.sleep(0.1)
                    
                if move_coords is None:
                    print("Intern Timeout")
                    continue

                move_notation = coords_to_notation(move_coords[0], move_coords[1])
                
                #Apply move locally
                if board.apply_move(move_coords, current_player):
                    whites, blacks, _ = board.count_stones()
                    historic.append(move_notation)
                    gui.update(board.board, blacks, whites, current_player)
                    print(f"Coup appliqué localement : {move_notation}")
                    
                    #Send move to remote player
                    color = 'B' if current_player == BLACK else 'W'
                    move_packet = f"1|{move_notation}|{color}"
                    
                    try: #Differenciate server and client
                        if is_server:
                            server_instance.send_response(move_packet)
                        elif is_client:
                            next_packet = client_instance.send_request(move_packet)
                        
                        print(f"Move sent: {move_packet}")
                        current_player = WHITE if current_player == BLACK else BLACK
                        
                        #Check if game is over after switching players
                        if is_game_over():
                            print("Game over - no valid moves for either player")
                            whites, blacks, _ = board.count_stones()
                            winner_code = "B" if blacks > whites else ("W" if whites > blacks else "NONE")
                            end_packet = f"2|{winner_code}"
                            try:
                                if is_server:
                                    server_instance.send_response(end_packet)
                                elif is_client:
                                    next_packet = client_instance.send_request(end_packet)
                                print(f"End game message sent: {end_packet}")
                            except Exception as e:
                                print(f"Error sending end game message: {e}")
                            game_state = "finished"
                            break
                        
                    except Exception as e: #Prevent crash if error
                        print(f"Error while sending move: {e}")
                        game_state = "aborted"
                        break
                else:
                    print("Error applying move")
                    if is_server:
                        server_instance.send_response("-3")
                    elif is_client:
                        next_packet = client_instance.send_request("-3")
                    continue

            #-------------- Local AI player --------------
            elif types[current_player] == "computer":
                move_notation = ask_move_AI(historic[-1] if historic else "")
                if move_notation == 0:
                    print("Was in critical section")
                    move_notation = ask_move_AI(historic[-1] if historic else "")
                move_str = "" + move_notation[0] + move_notation[1]
                move_coords = notation_to_coords(move_notation)
                
                #Apply move locally first
                if board.apply_move(move_coords, current_player):
                    whites, blacks, _ = board.count_stones()
                    historic.append(move_notation)

                    gui.update(board.board, blacks, whites, current_player)
                    print(f"Coup appliqué localement : {move_notation}")
                    
                    #Send move to remote player
                    color = 'B' if current_player == BLACK else 'W'
                    move_packet = f"1|{move_str}|{color}"
                    
                    try:
                        if is_server:
                            server_instance.send_response(move_packet)
                        elif is_client:
                            next_packet = client_instance.send_request(move_packet)
                        
                        print(f"Move sent: {move_packet}")
                        current_player = WHITE if current_player == BLACK else BLACK
                        
                        #Check if game is over after switching players
                        if is_game_over():
                            print("Game over - no valid moves for either player")
                            whites, blacks, _ = board.count_stones()
                            winner_code = "B" if blacks > whites else ("W" if whites > blacks else "NONE")
                            end_packet = f"2|{winner_code}"
                            try:
                                if is_server:
                                    server_instance.send_response(end_packet)
                                elif is_client:
                                    next_packet = client_instance.send_request(end_packet)
                                print(f"End game message sent: {end_packet}")
                            except Exception as e:
                                print(f"Error sending end game message: {e}")
                            game_state = "finished"
                            break
                        
                    except Exception as e:
                        print(f"Error while sending move: {e}")
                        game_state = "aborted"
                        break
                else:
                    print("Error applying move")
                    if is_server:
                        server_instance.send_response("-3")
                    elif is_client:
                        next_packet = client_instance.send_request("-3")
                    continue

            #-------------- Remote player --------------
            elif types[current_player] == EXTERN:
                print(f"Waiting for remote player ({'NOIR' if current_player == BLACK else 'BLANC'})")
                try:
                    #Get the message from remote player --------------
                    if is_server:
                        message = server_instance.accept_and_respond()
                    elif is_client:
                        max_timeout_attempts = 10
                        timeout_wait = 2
                        message = None
                        
                        if next_packet is None:
                            for timeout_attempt in range(max_timeout_attempts):
                                try:
                                    print(f"Ask move (try {timeout_attempt + 1}/{max_timeout_attempts})")
                                    response = client_instance.send_request("4")
                                    
                                    if response and response != "4":
                                        message = response
                                        break
                                    elif response == "4":  #Server Timeout
                                        print("Server Timeout")
                                        time.sleep(timeout_wait)
                                        continue
                                    else: 
                                        print("Empty response")
                                        time.sleep(timeout_wait)
                                        continue
                                        
                                except Exception as e:
                                    print(f"Error with try {timeout_attempt + 1}: {e}")
                                    if timeout_attempt < max_timeout_attempts - 1:
                                        time.sleep(timeout_wait)
                                    else:
                                        print("Unable to receive move")
                                        game_state = "aborted"
                                        break
                            
                            if message is None and game_state != "aborted":
                                print("Timeout")
                                game_state = "aborted"
                                break
                        else:
                            message = next_packet
                            next_packet = None  #Clear after using
                    
                    if game_state == "aborted":
                        break
                    
                    #Handle message --------------
                    message_str = message if isinstance(message, str) else (message[0] if isinstance(message, list) and len(message) > 0 else str(message))
                    print(f"Message reçu du joueur distant : {message_str}")
                    
                    if message_str.startswith("1"):
                        parts = message_str.split("|")
                        if len(parts) == 3:
                            move_notation = parts[1]
                            if move_notation == "NONE":
                                print("Remote player sent 'NONE' move, skipping turn")
                                current_player = WHITE if current_player == BLACK else BLACK
                                continue
                            player_color = parts[2]
                            expected_color = 'B' if current_player == BLACK else 'W'
                            
                            if player_color != expected_color:
                                error_msg = "-3"
                                if is_server:
                                    server_instance.send_response(error_msg)
                                elif is_client:
                                    next_packet = client_instance.send_request(error_msg)
                                print(f"Wrong colour")
                                continue
                            
                            #Validate and apply the move
                            try:
                                move_coords = notation_to_coords(move_notation)
                                if move_coords in valid_moves:
                                    if board.apply_move(move_coords, current_player):
                                        historic.append(move_notation)
                                        if types[1 - current_player] == "computer":
                                            move_str = "" + move_notation[0] + move_notation[1]
                                            play_against_AI(move_str)
                                        whites, blacks, _ = board.count_stones()
                                        print(f"Coup reçu et appliqué : {move_notation}")
                                        gui.update(board.board, blacks, whites, current_player)

                                        current_player = WHITE if current_player == BLACK else BLACK
                                        
                                        #Check if game is over after switching players
                                        if is_game_over():
                                            print("Game over - no valid moves for either player")
                                            #Send end game message since we detected the end
                                            whites, blacks, _ = board.count_stones()
                                            winner_code = "B" if blacks > whites else ("W" if whites > blacks else "NONE")
                                            end_packet = f"2|{winner_code}"
                                            try:
                                                if is_server:
                                                    server_instance.send_response(end_packet)
                                                elif is_client:
                                                    next_packet = client_instance.send_request(end_packet)
                                                print(f"End game message sent: {end_packet}")
                                            except Exception as e:
                                                print(f"Error sending end game message: {e}")
                                            game_state = "finished"
                                            break
                                    else:
                                        error_msg = "-3"
                                        if move_notation == historic[-1]:
                                            error_msg = "-7"
                                        if is_server:
                                            server_instance.send_response(error_msg)
                                        elif is_client:
                                            next_packet = client_instance.send_request(error_msg)
                                        print(f"Invalid move: {move_notation}")
                                        continue
                                else:
                                    error_msg = "-3"
                                    if is_server:
                                        server_instance.send_response(error_msg)
                                    elif is_client:
                                        next_packet = client_instance.send_request(error_msg)
                                    print(f"Invalid move2: {move_notation}")
                                    continue
                            except Exception as e:
                                error_msg = "-3"
                                if is_server:
                                    server_instance.send_response(error_msg)
                                elif is_client:
                                    next_packet = client_instance.send_request(error_msg)
                                print(f"Error with the move: {e}")
                                continue
                        else:
                            error_msg = "-5"
                            if is_server:
                                server_instance.send_response(error_msg)
                            elif is_client:
                                next_packet = client_instance.send_request(error_msg)
                            print("Invalid format")
                            continue
                    
                    elif message_str.startswith("2"):
                        #End game
                        parts = message_str.split("|")
                        if len(parts) == 2:
                            declared_winner = parts[1]
                            actual_winner = "B" if blacks > whites else ("W" if whites > blacks else "NONE")
                            if declared_winner == actual_winner:
                                ack_msg = "-1"
                                if is_server:
                                    server_instance.send_response(ack_msg)
                                elif is_client:
                                    next_packet = client_instance.send_request(ack_msg)
                                
                                winner = BLACK if declared_winner == "B" else (WHITE if declared_winner == "W" else None)
                                print(f"Game ended: {declared_winner} won!")
                                game_state = "finished"
                                break
                            else:
                                error_msg = "-5"
                                if is_server:
                                    server_instance.send_response(error_msg)
                                elif is_client:
                                    next_packet = client_instance.send_request(error_msg)
                                print("Disagreement on the winner")
                                game_state = "aborted"
                                break
                        else:
                            error_msg = "-5"
                            if is_server:
                                server_instance.send_response(error_msg)
                            elif is_client:
                                next_packet = client_instance.send_request(error_msg)
                            print("Invalid format")
                            continue
                        
                    elif message_str.startswith("3"):
                        #Surrendering
                        print("Surrendered")
                        try:
                            if is_server:
                                #BLACK (server) won
                                server_instance.send_response("-1")  #Acknowledgement 
                                winner = BLACK
                            elif is_client:
                                #WHITE (client) won
                                next_packet = client_instance.send_request("-1")  #Acknowledge
                                winner = WHITE
                            
                            print(f"Game ended by surrender. {'BLACK' if winner == BLACK else 'WHITE'} won")
                            game_state = "finished"
                            break
                        except Exception as e:
                            print(f"Error handling surrender: {e}") #Internal error
                            error_code = "-2"
                            if is_server:
                                server_instance.send_response(error_code)
                            elif is_client:
                                next_packet = client_instance.send_request(error_code)
                            game_state = "aborted"
                            break
                        
                    elif message_str.startswith("-7"):
                        #Abort game message
                        print("Aborted request")
                        try:
                            if is_server:
                                server_instance.send_response("-1")  #Acknowledgement
                            elif is_client:
                                next_packet = client_instance.send_request("-1")  #Acknowledgement
                            
                            game_state = "aborted"
                            break
                        except Exception as e:
                            print(f"Error handling abort: {e}") #Internal error (again)
                            error_code = "-2"
                            if is_server:
                                server_instance.send_response(error_code)
                            elif is_client:
                                next_packet = client_instance.send_request(error_code)
                            game_state = "aborted"
                            break

                    elif message_str.startswith("-6"):
                        #Move lost (how is it possible to loose a move locally (-_-) ?)
                        print("Move lost by other player")
                        if len(historic) > 0:
                            last_move = historic[-1]
                            last_color = 'B' if len(historic) % 2 == 1 else 'W'
                            repeat_msg = f"1|{last_move}|{last_color}"
                            try:
                                if is_server:
                                    server_instance.send_response(repeat_msg)
                                elif is_client:
                                    next_packet = client_instance.send_request(repeat_msg)
                                print(f"Repeated move: {repeat_msg}")
                            except Exception as e:
                                print(f"Error repeating move: {e}")
                                game_state = "aborted"
                                break
                        else:
                            #Not possible before moves (even if that case is not supposed to happen)
                            error_msg = "-5"
                            if is_server:
                                server_instance.send_response(error_msg)
                            elif is_client:
                                next_packet = client_instance.send_request(error_msg)
                            print("No move to repeat")

                    elif message_str.startswith("-2"):
                        #Internal error from opponent
                        print("Internal error from opponent")
                        if is_server:
                            winner = BLACK  #Server is BLACK
                        elif is_client:
                            winner = WHITE  #Client is WHITE  
                        
                        game_state = "finished"
                        print(f"Game ended due to opponent's internal error. {'BLACK' if winner == BLACK else 'WHITE'} won")
                        break

                    else:
                        error_msg = "-5"
                        if is_server:
                            server_instance.send_response(error_msg)
                        elif is_client:
                            next_packet = client_instance.send_request(error_msg)
                        print(f"Invalid message: {message_str}")
                        continue
                    
                except Exception as e:
                    print(f"Error when receiving move: {e}")
                    game_state = "aborted"
                    break
        else:
            #No valid moves, skip turn
            skip_packet = "1|NONE|B" if current_player == BLACK else "1|NONE|W"
            try:
                if types[current_player] != EXTERN:
                    print(f"No valid moves for {'BLACK' if current_player == BLACK else 'WHITE'}, sending skip notification")
                    if is_server:
                        server_instance.send_response(skip_packet)
                    elif is_client:
                        next_packet = client_instance.send_request(skip_packet)
                else:
                    #If remote player should skip, we need to wait for their NONE move
                    print(f"Waiting for remote player to send skip notification")
                    try:
                        if is_server:
                            message = server_instance.accept_and_respond()
                        elif is_client:
                            #Use same timeout logic as for regular moves
                            max_timeout_attempts = 10
                            timeout_wait = 2
                            message = None
                            
                            if next_packet is None:
                                for timeout_attempt in range(max_timeout_attempts):
                                    try:
                                        response = client_instance.send_request("4")
                                        if response and response != "4":
                                            message = response
                                            break
                                        elif response == "4":
                                            time.sleep(timeout_wait)
                                            continue
                                        else:
                                            time.sleep(timeout_wait)
                                            continue
                                    except Exception as e:
                                        if timeout_attempt < max_timeout_attempts - 1:
                                            time.sleep(timeout_wait)
                                        else:
                                            print("Timeout waiting for skip notification")
                                            game_state = "aborted"
                                            break
                            else:
                                message = next_packet
                                next_packet = None
                        
                        if game_state == "aborted":
                            break
                            
                        #Handle skip
                        message_str = message if isinstance(message, str) else str(message)
                        if message_str.startswith("1|NONE|"):
                            print("Received skip notification from remote player")
                        else:
                            print(f"Expected skip notification, got: {message_str}")
                    except Exception as e:
                        print(f"Error waiting for skip notification: {e}")
                        game_state = "aborted"
                        break
                
                #Update the current player
                current_player = WHITE if current_player == BLACK else BLACK
                continue
            except Exception as e:
                print(f"Error sending skip turn notification: {e}")
                game_state = "aborted"
                break

    #---------------------------- End game handling ----------------------------
    #Ensure we have final stone counts
    whites, blacks, _ = board.count_stones()
    
    if game_state == "playing":
        print("Warning: Game loop ended but game_state is still 'playing'")
        whites, blacks, _ = board.count_stones()
        winner = BLACK if blacks > whites else (WHITE if whites > blacks else None)
        game_state = "finished"
    
    elif game_state == "finished":
        whites, blacks, _ = board.count_stones()
        if 'winner' not in locals():
            winner = BLACK if blacks > whites else (WHITE if whites > blacks else None)
        if is_server:
            server_instance.send_response("-1")
        elif is_client:
            next_packet = client_instance.send_request("-1")

        print(f"Game finished. Final score: BLACK={blacks}, WHITE={whites}")
        
    elif game_state == "aborted":
        print("Game was aborted due to error or timeout")
        winner = None
    
    #Cleanup and show results
    try:
        if server_instance:
            server_instance.stop()
            print("Server stopped")
    except Exception as e:
        print(f"Error stopping server: {e}")
    
    try:
        if game_state == "aborted":
            new_show_winner(None, theme, gui, whites, blacks)
        else:
            new_show_winner(winner, theme, gui, whites, blacks)
    except Exception as e:
        print(f"Error showing winner screen: {e}")
    
    print(f"Game loop ended with state: {game_state}")


        
def receive_with_timeout(connection):
    """Receive message with timeout handling"""
    if hasattr(connection, 'accept_and_respond'):
        return connection.accept_and_respond()
    else:
        return connection.receive()


def update_language(selected, menu, widgets):
    lang = selected[0][1]
    texts = TRANSLATIONS[lang]
    
    #Update widgets that exist
    if 'player1' in widgets:
        widgets['player1'].set_title(texts['player1'])
    if 'player2' in widgets:
        widgets['player2'].set_title(texts['player2'])
    if 'language' in widgets:
        widgets['language'].set_title(texts['language'])
    if 'theme' in widgets:
        widgets['theme'].set_title(texts['theme'])
    if 'play' in widgets:
        widgets['play'].set_title(texts['play'])
    if 'quit' in widgets:
        widgets['quit'].set_title(texts['quit'])
    if 'audio' in widgets:
        widgets['audio'].set_title(texts['audio'])

    #Update server IP field
    if 'server_ip' in widgets:
        current_value = widgets['server_ip'].get_value()
        menu.remove_widget(widgets['server_ip'])

        player1_is_online = widgets['player1'].get_value()[0][1] == EXTERN
        player2_is_online = widgets['player2'].get_value()[0][1] == EXTERN
        if player1_is_online:
            callback = on_server_ip_change1
        elif player2_is_online:
            callback = on_server_ip_change2
        else:
            callback = on_server_ip_change1

        widgets['server_ip'] = menu.add.text_input(
            texts['server_ip'] + ": ",
            default=current_value,
            onchange=callback
        )

    #Update translated options
    if 'player1' in widgets and 'player2' in widgets:
        player1_index = widgets['player1'].get_index()
        player2_index = widgets['player2'].get_index()
        translated_options = [
            (texts['human'], HUMAN),
            (texts['computer'], COMPUTER),
            (texts['online'], EXTERN)
        ]
        widgets['player1'].update_items(translated_options)
        widgets['player1'].set_value(player1_index)
        widgets['player2'].update_items(translated_options)
        widgets['player2'].set_value(player2_index)

    if 'audio' in widgets:
        audio_index = widgets['audio'].get_index()
        texts = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
        translated_audio_options = [
            (texts['audio_on'], AUDIO_OPTIONS[0][1]),
            (texts['audio_off'], AUDIO_OPTIONS[1][1])
        ]
        
        widgets['audio'].update_items(translated_audio_options)
        widgets['audio'].set_value(audio_index)

    #Update theme selector
    if 'theme' in widgets:
        theme_index = widgets['theme'].get_index()
        translated_themes = [
            (texts['theme_normal'], 'Normal'),
            (texts['theme_harry_potter'], 'Harry_Potter')
        ]
        widgets['theme'].update_items(translated_themes)
        widgets['theme'].set_value(theme_index)


def on_server_ip_change2(value):
    global server_ip
    server_ip = value

def on_server_ip_change1(value):
    global our_ip
    our_ip = value


#--- MAIN MENU ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
    global server_running, server_thread    # |
    server_running = False                  # | Reset server state
    server_thread = None                    # |

    #--- Load background image ---
    background_image = None
    for ext in ['png', 'jpg', 'jpeg', 'bmp']:
        image_path = f'assets/menu_bg.{ext}'
        if os.path.exists(image_path):
            try:
                background_image = pygame.image.load(image_path).convert_alpha()
                background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                break
            except pygame.error as e:
                print(f"Error loading background image: {e}")
                continue

    #--- Load the logo of the window ---
    icon_image = None
    for ext in ['png', 'jpg', 'jpeg', 'bmp']:
        icon_path = f'assets/Logo_ot.{ext}'
        if os.path.exists(icon_path):
            try:
                icon_image = pygame.image.load(icon_path)
                pygame.display.set_icon(icon_image)
                break
            except pygame.error as e:
                print(f"Erreur lors du chargement de l'icône : {e}")

    pygame.display.set_caption("OthelloMora")

    #-----------------------------------

    current_audio = False
    current_language = [DEFAULT_LANGUAGE]
    current_theme = DEFAULT_THEME
    t = TRANSLATIONS[current_language[0]]

    current_theme_str = [DEFAULT_THEME]

    common_theme_settings = {
        'background_color': (0, 0, 0, 0),
        'title_background_color': (0, 0, 0, 0),
        'title_font_shadow': False,
        'widget_background_color': (0, 0, 0, 0),
        'selection_color': (255, 215, 0)
    }

    #Harry Potter theme
    harry_potter_theme = pygame_menu.Theme(**common_theme_settings)
    harry_potter_theme.title_font = os.path.join('assets', 'fonts', 'HARRYP__.TTF')
    harry_potter_theme.title_font_color = (255, 255, 255)
    harry_potter_theme.widget_font = os.path.join('assets', 'fonts', 'HARRYP__.TTF')
    harry_potter_theme.widget_font_color = (255, 215, 0)
    harry_potter_theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    default_theme = pygame_menu.themes.THEME_DARK.copy()
    for key, value in common_theme_settings.items():
        setattr(default_theme, key, value)
    
    #Use NotoSansCJK for Chinese (modified for both cases to increase coherence)
    chinese_font_path = os.path.join('assets', 'fonts', 'NotoSansCJK-Regular.ttc')
    if current_language[0] == 'zh' and os.path.exists(chinese_font_path):
        default_theme.title_font = chinese_font_path
        default_theme.widget_font = chinese_font_path
    else:
        default_theme.title_font = os.path.join('assets', 'fonts', 'NotoSansCJKsc-Regular.ttf')
        default_theme.widget_font = os.path.join('assets', 'fonts', 'NotoSansCJKsc-Regular.ttf')
    
    default_theme.title_font_color = (255, 255, 255)
    default_theme.widget_font_color = (255, 255, 255)

    selected_theme = harry_potter_theme if current_theme_str[0] == "Harry_Potter" else default_theme

    #--- Menu with background function ---
    def background_function():
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((0, 0, 0))
        

    menu = pygame_menu.Menu(
        '',
        WIDTH, HEIGHT, theme=selected_theme
    )

    widgets = {}

    #Make IP selection appear and sepend on the player number
    def on_player_change(useless1, useless2):   #Need 2 arguments
        player1_is_online = widgets['player1'].get_value()[0][1] == EXTERN
        player2_is_online = widgets['player2'].get_value()[0][1] == EXTERN

        if player1_is_online or player2_is_online:
            if 'server_ip' not in widgets:
                default_ip = ""
                callback = on_server_ip_change1 if player1_is_online else on_server_ip_change2
                widgets['server_ip'] = menu.add.text_input(
                    TRANSLATIONS[current_language[0]]['server_ip'] + ": ",
                    default=default_ip,
                    onchange=callback
                )
        else:
            if 'server_ip' in widgets:
                menu.remove_widget(widgets['server_ip'])
                del widgets['server_ip']

    #Player selectors
    translated_player_options = [
        (t['human'], HUMAN),
        (t['computer'], COMPUTER),
        (t['online'], EXTERN)
    ]
    widgets['player1'] = menu.add.selector(
        t['player1'] + ' :', translated_player_options,
        onchange=on_player_change)
    
    widgets['player2'] = menu.add.selector(
        t['player2'] + ' :', translated_player_options,
        onchange=on_player_change)

    #Audio selector
    widgets['audio'] = menu.add.selector(
        t['audio'] + ' :', AUDIO_OPTIONS,
        default=[i for i, a in enumerate(AUDIO_OPTIONS) if a[1] == current_audio][0]
    )

    #Language selector
    widgets['language'] = menu.add.selector(
        t['language'] + ' :', LANGUAGES,
        default=[i for i, l in enumerate(LANGUAGES) if l[1] == current_language[0]][0],
        onchange=lambda val, _: update_language(val, menu, widgets)
    )

    #Theme selector
    widgets['theme'] = menu.add.selector(
        t['theme'] + ' :', THEMES,
        default=[i for i, th in enumerate(THEMES) if th[1] == current_theme][0]
    )

    #Buttons
    def on_play_pressed():
        player1 = widgets['player1'].get_value()[0][1]
        player2 = widgets['player2'].get_value()[0][1]
        theme = widgets['theme'].get_value()[0][1]
        current_theme_str[0] = theme

        if theme == "Harry_Potter":
            def on_houses_selected(h1, h2):
                gui = Gui(theme)
                gui.house1 = h1
                gui.house2 = h2
                gui.load_pieces()
                gui.show_game()
                board = Board()
                current_player = BLACK
                whites, blacks, _ = board.count_stones()
                gui.update(board.board, blacks, whites, current_player)

                if player1 == "computer":
                    init_AI('B')
                elif player2 == "computer":
                    init_AI('W')

                if player1 == "extern" or player2 == "extern":
                    run_game_loop_online(gui, board, current_player, [player1, player2], theme)
                else:
                    run_game_loop(gui, board, current_player, [player1, player2], theme, bool(1 - widgets['audio'].get_value()[1]))

            menu.disable()
            show_harry_potter_house_selector(screen, on_houses_selected, on_cancel=main)
        else:
            start_game(player1, player2, theme, bool(1 - widgets['audio'].get_value()[1]))

    widgets['play'] = menu.add.button(t['play'], on_play_pressed)
    widgets['quit'] = menu.add.button(t['quit'], pygame_menu.events.EXIT)

    #--- Main loop ---
    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        
        # Draw background first
        background_function()
        
        # Update and draw menu
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)
        
        # Handle events
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()