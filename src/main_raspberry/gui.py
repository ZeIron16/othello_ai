import pygame
import os
import time
import sys
from pygame.locals import *
from config_ui import BLACK, WHITE, EMPTY

class Gui:
    def __init__(self,theme="Normal"):
        pygame.init()
        self.background_img = None
        self.BOARD_SIZE = 400
        self.SCREEN_SIZE = (800, 600)
        self.BOARD_POS = (
            (self.SCREEN_SIZE[0] - self.BOARD_SIZE) // 2,
            (self.SCREEN_SIZE[1] - self.BOARD_SIZE) // 2 
            )
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.RESIZABLE)
        self.theme = theme
        self.original_screen_size = self.SCREEN_SIZE

        self.house1 = None
        self.house2 = None

        self.current_board = None
        self.current_blacks = 0
        self.current_whites = 0
        self.current_player_color = None
        self.current_valid_moves = None


        if theme == "Harry_Potter":
            font_path = os.path.join("assets", "fonts", "HARRYP__.TTF")
            self.font = pygame.font.Font(font_path, 22)
            self.score_font = pygame.font.Font(font_path, 50)
        else:
            self.font = pygame.font.SysFont("Arial", 22)
            self.score_font = pygame.font.SysFont("Arial", 50)

        # Chargement des images
        img_path = os.path.join("assets", theme)
        self.board_img = pygame.image.load(os.path.join(img_path, "board.bmp")).convert_alpha()
        self.tip_img = pygame.image.load(os.path.join(img_path, "tip.png")).convert_alpha()
        self.clear_img = pygame.image.load(os.path.join(img_path, "empty.bmp")).convert()

        if theme == "Harry_Potter":
            self.background_img = pygame.image.load(os.path.join("assets", "Harry_Potter", "background_game2.bmp")).convert()
            self.background_img = pygame.transform.scale(self.background_img, self.SCREEN_SIZE)

        # Chargement dynamique des pions selon le thème et les maisons
        self.black_img = None
        self.white_img = None
        self.load_pieces()

    def handle_resize(self, new_width, new_height):
        self.SCREEN_SIZE = (new_width, new_height)

        self.BOARD_POS = (
            (self.SCREEN_SIZE[0] - self.BOARD_SIZE) // 2,
            (self.SCREEN_SIZE[1] - self.BOARD_SIZE) // 2
        )

        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.RESIZABLE)

        if self.theme == "Harry_Potter" and self.background_img is not None:
            self.background_img = pygame.transform.scale(self.background_img, self.SCREEN_SIZE)
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        if self.current_board:
            self.update(self.current_board, self.current_blacks, self.current_whites,
                        self.current_player_color, self.current_valid_moves)
        else:
            self.show_game()

        return True

    def show_game(self):

        if self.background_img and (self.background_img.get_width() != self.SCREEN_SIZE[0] or self.background_img.get_height() != self.SCREEN_SIZE[1]):
            self.background_img = pygame.transform.scale(self.background_img, self.SCREEN_SIZE)
        
        if self.background_img:
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill((0, 0, 0))
        self.screen.blit(self.board_img, self.BOARD_POS)
        if self.theme == "Harry_Potter":
            title_font = pygame.font.Font(os.path.join("assets", "fonts", "HARRYP__.TTF"), 64)
        else:
            title_font = pygame.font.SysFont("Arial", 64)
        title_str = "Othellomora" if self.theme == "Harry_Potter" else "Othello"
        title_x = self.SCREEN_SIZE[0] // 2 -  title_font.size(title_str)[0] // 2
        title_y = 30  # Adjust vertically as needed

        shadow = title_font.render(title_str, True, (0, 0, 0))
        self.screen.blit(shadow, (title_x + 3, title_y + 3))

        title_text = title_font.render(title_str, True, (212, 175, 55))  # Rich gold color
        self.screen.blit(title_text, (title_x, title_y))
        pygame.display.flip()
    
    def put_stone(self, pos, color):
        if pos is None:
            return

        pos = (pos[1], pos[0])  # Flip for screen orientation

        if color == BLACK:
            img = self.black_img
        elif color == WHITE:
            img = self.white_img
        elif color == EMPTY:
            img = self.tip_img
        else:
            return  # Skip unknown values

        x = pos[0] * self.SQUARE_SIZE + self.BOARD_POS[0] + 20
        y = pos[1] * self.SQUARE_SIZE + self.BOARD_POS[1] + 20
        self.screen.blit(img, (x, y), img.get_rect())
    
    def clear_square(self, pos):
        """ Puts in the given position a background image, to simulate that the
        piece was removed.
        """
        # flip orientation
        pos = (pos[1], pos[0])

        x = pos[0] * self.SQUARE_SIZE + self.BOARD_POS[0] + 20
        y = pos[1] * self.SQUARE_SIZE + self.BOARD_POS[1] + 20
        self.screen.blit(self.clear_img, (x, y), self.clear_img.get_rect())
    
    def clear_tips(self, board):
        for i in range(8):
            for j in range(8):
                if board[i][j] == EMPTY:
                    self.clear_square((i, j))

    def update(self, board, blacks, whites, current_player_color, valid_moves=None):
        self.current_board = [row[:] for row in board]  # Copie profonde du plateau
        self.current_blacks = blacks
        self.current_whites = whites
        self.current_player_color = current_player_color
        self.current_valid_moves = valid_moves[:] if valid_moves else None

        current_size = self.screen.get_size()
        if current_size != self.SCREEN_SIZE:
            self.handle_resize(current_size[0], current_size[1])
        self.clear_tips(board)  # Ensures tips from previous move are cleared
        self.screen.blit(self.board_img, self.BOARD_POS)

        for i in range(8):
            for j in range(8):
                if board[i][j] in (BLACK, WHITE):
                    self.put_stone((i, j), board[i][j])

        # Ajoute les tips
        if valid_moves:
            for move in valid_moves:
                if board[move[0]][move[1]] == EMPTY:
                    self.put_stone(move, EMPTY)

        self.show_score(blacks, whites)
        self.show_turn(current_player_color)
        pygame.display.update()


    def show_score(self, blacks, whites):
        if self.theme == "Harry_Potter":
            if self.background_img:
                # Left side
                left_clear_rect = pygame.Rect(self.BOARD_POS[0] - 110, self.BOARD_POS[1], 100, 100)
                self.screen.blit(self.background_img, left_clear_rect, area=left_clear_rect)
                # Right side
                right_clear_rect = pygame.Rect(self.BOARD_POS[0] + self.BOARD_SIZE + 70, self.BOARD_POS[1], 100, 100)
                self.screen.blit(self.background_img, right_clear_rect, area=right_clear_rect)
        else:
            self.screen.fill((0, 0, 0), (self.BOARD_POS[0] - 120, self.BOARD_POS[1], 100, 100))
            self.screen.fill((0, 0, 0), (self.BOARD_POS[0] + self.BOARD_SIZE + 60, self.BOARD_POS[1], 100, 100))
        
        label_color = (212, 175, 55) if self.theme == "Harry_Potter" else (255, 255, 255)
        label_black = self.font.render(self.house1 or "Black", True, label_color)
        label_white = self.font.render(self.house2 or "White", True, label_color)
        score_color = (212, 175, 55) if self.theme == "Harry_Potter" else (255, 255, 255)
        score_black = self.score_font.render(f"{blacks}", True, score_color)
        score_white = self.score_font.render(f"{whites}", True, score_color)

        left_x = self.BOARD_POS[0] - 100
        right_x = self.BOARD_POS[0] + self.BOARD_SIZE + 80

        if self.theme == "Harry_Potter":
            logo_size = (60, 60)
            house_logos = {
                "Gryffindor": "gryffindor.png",
                "Slytherin": "slytherin.png",
                "Ravenclaw": "ravenclaw.png",
                "Hufflepuff": "hufflepuff.png"
            }
            if self.house1 in house_logos:
                logo1 = pygame.image.load(os.path.join("assets", "Harry_Potter", "houses", house_logos[self.house1]))
                logo1 = pygame.transform.scale(logo1, logo_size)
                logo1.set_colorkey((0, 0, 0))  # Optional: make black transparent if needed
                self.screen.blit(logo1, (left_x + 25 - logo1.get_width() // 2, self.BOARD_POS[1] - 60))
            if self.house2 in house_logos:
                logo2 = pygame.image.load(os.path.join("assets", "Harry_Potter", "houses", house_logos[self.house2]))
                logo2 = pygame.transform.scale(logo2, logo_size)
                logo2.set_colorkey((0, 0, 0))
                self.screen.blit(logo2, (right_x + 25 - logo2.get_width() // 2, self.BOARD_POS[1]- 60))

        self.screen.blit(label_black, (left_x + 25 - label_black.get_width() // 2, self.BOARD_POS[1]))
        self.screen.blit(score_black, (left_x + 25 - score_black.get_width() // 2, self.BOARD_POS[1] + 20))
        self.screen.blit(label_white, (right_x + 25 - label_white.get_width() // 2, self.BOARD_POS[1]))
        self.screen.blit(score_white, (right_x + 25 - score_white.get_width() // 2, self.BOARD_POS[1] + 20))

    def show_valid_moves(self, moves):
        for move in moves:
            self.put_stone(move, EMPTY)
        pygame.display.update()

    def get_mouse_input(self, valid_moves):
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x < self.BOARD_POS[0] or \
                       mouse_x > self.BOARD_SIZE + self.BOARD_POS[0] or \
                       mouse_y < self.BOARD_POS[1] or \
                       mouse_y > self.BOARD_SIZE + self.BOARD_POS[1]:
                        continue 
                        
                    col = (mouse_x - self.BOARD_POS[0] - 20) // self.SQUARE_SIZE
                    row = (mouse_y - self.BOARD_POS[1] - 20) // self.SQUARE_SIZE
                    position = (row, col)

                    if 0 <= row < 8 and 0 <= col < 8:
                        position = (row, col)
                        if position in valid_moves:
                            return position
                        
                elif event.type == VIDEORESIZE:
                    self.handle_resize(event.w, event.h)
                        
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def show_winner(self, color):
        winner_text = "Draw!"
        if color == BLACK:
            winner_text = "Black Wins!"
        elif color == WHITE:
            winner_text = "White Wins!"
        elif color == EMPTY:
            winner_text = "Tie!"

        msg = self.font.render(winner_text, True, (255, 255, 255))
        self.screen.blit(msg, (250, 200))
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    return
            time.sleep(0.1)

    def show_turn(self, current_player_color):
        color_name = self.house1 if current_player_color == BLACK and self.house1 else (
            self.house2 if current_player_color == WHITE and self.house2 else (
                "Black" if current_player_color == BLACK else "White"))
        text_bf = f"{color_name}'s Turn"
        fst_c = text_bf[0].upper()
        text_bf = fst_c + text_bf[1:]
        text = self.font.render(text_bf, True, (212, 175, 55))
        rect = pygame.Rect(0, self.SCREEN_SIZE[1] - 50, self.SCREEN_SIZE[0], 50)
        if self.theme == "Harry_Potter" and self.background_img:
            turn_rect = pygame.Rect(0, self.SCREEN_SIZE[1] - 50, self.SCREEN_SIZE[0], 50)
            self.screen.blit(self.background_img, turn_rect, area=turn_rect)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), rect)
        x = self.SCREEN_SIZE[0] // 2 - text.get_width() // 2
        y = self.SCREEN_SIZE[1] - 40
        self.screen.blit(text, (x, y))

    def select_houses(self):
        selected = [None, None]
        choosing = [0]  # 0: player1, 1: player2

        house_images = {
            "Gryffindor": pygame.image.load("assets/Harry_Potter/gryffindor.png"),
            "Slytherin": pygame.image.load("assets/Harry_Potter/slytherin.png"),
            "Ravenclaw": pygame.image.load("assets/Harry_Potter/ravenclaw.png"),
            "Hufflepuff": pygame.image.load("assets/Harry_Potter/hufflepuff.png"),
        }

        house_names = list(house_images.keys())

        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 36)

        while None in selected:
            self.screen.fill((0, 0, 0))
            prompt = f"Player {choosing[0]+1}, choose your house"
            text = font.render(prompt, True, (255, 255, 255))
            self.screen.blit(text, (self.SCREEN_SIZE[0]//2 - text.get_width()//2, 40))

            for i, name in enumerate(house_names):
                img = pygame.transform.scale(house_images[name], (100, 100))
                x = 100 + i * 150
                y = 200
                self.screen.blit(img, (x, y))
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 100, 100), 2)
                label = self.font.render(name, True, (255, 255, 255))
                self.screen.blit(label, (x + 50 - label.get_width()//2, y + 110))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for i in range(len(house_names)):
                        x = 100 + i * 150
                        y = 200
                        if x <= mx <= x+100 and y <= my <= y+100:
                            selected[choosing[0]] = house_names[i]
                            choosing[0] += 1
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        return selected[0], selected[1]
    
    def load_pieces(self):
        if self.theme == "Harry_Potter" and self.house1 and self.house2:
            path = lambda house: os.path.join("assets", "Harry_Potter", "Piece", f"{house}_pion.png")
            self.black_img = pygame.image.load(path(self.house1)).convert_alpha()
            self.white_img = pygame.image.load(path(self.house2)).convert_alpha()
        else:
            try:
                self.black_img = pygame.image.load(os.path.join("assets", "Normal", "black.bmp")).convert_alpha()
                self.white_img = pygame.image.load(os.path.join("assets", "Normal", "white.bmp")).convert_alpha()
            except pygame.error as e:
                print("Erreur lors du chargement des pions du thème Normal :", e)
                # Fallback pieces
                self.black_img = pygame.Surface((40, 40), pygame.SRCALPHA)
                self.black_img.fill((0, 0, 0))
                self.white_img = pygame.Surface((40, 40), pygame.SRCALPHA)
                self.white_img.fill((255, 255, 255))