import os
import pygame_menu
import pygame
import time

def show_end_screen(screen, winner_house, player1_house=None, player2_house=None, blacks=0, whites=0, on_play_again=None, on_quit=None):
    """
    Affiche l'écran de fin de jeu avec le gagnant
    
    Args:
        screen: L'écran pygame
        winner_house: La maison gagnante ('Gryffindor', 'Slytherin', etc.) ou None pour égalité
        player1_house: Maison du joueur 1 (optionnel)
        player2_house: Maison du joueur 2 (optionnel)
        blacks: Score des pions noirs
        whites: Score des pions blancs
        on_play_again: Fonction à appeler pour rejouer
        on_quit: Fonction à appeler pour quitter
    """
    
    # Obtenir la taille de l'écran
    screen_width, screen_height = screen.get_size()
    
    # Thème Harry Potter pour l'écran de fin
    harry_potter_theme = pygame_menu.Theme(
        background_color=pygame_menu.baseimage.BaseImage(
            os.path.join('assets', 'Harry_Potter', 'bg_parchment2.png'),
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,  
        ),
        title_font=os.path.join('assets', 'fonts', 'HARRYP__.TTF'),
        widget_font=os.path.join('assets', 'fonts', 'HARRYP__.TTF'),
        widget_font_color=(150, 100, 20),
        widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(),
        title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
    )
    
    # Créer le menu de fin avec la taille de l'écran
    menu = pygame_menu.Menu('', width=screen_width, height=screen_height, theme=harry_potter_theme)
    
    # Titre principal
    if winner_house:
        text_bf = f"{winner_house} Wins!" if winner_house else "Draw!"
        fst_c = text_bf[0].upper()
        text_bf = fst_c + text_bf[1:]
        menu.add.label(text_bf, font_size=60, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 15)
        menu.add.label("Victory!", font_size=40, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 10)
    else:
        menu.add.label("Draw!", font_size=60, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 15)
        menu.add.label("It's a tie!", font_size=40, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 10)
    
    # Afficher l'image de la maison gagnante
    if winner_house:
        try:
            winner_image_path = f'assets/Harry_Potter/houses/{winner_house}.png'
            winner_image = menu.add.image(winner_image_path, scale=(1.0, 1.0))
            winner_image.set_margin(0, 15)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Warning: Could not load winner image: {e}")
    
    # Scores
    menu.add.label("Final Scores", font_size=35, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 15)
    
    # Affichage des scores avec les maisons (adapté à la largeur d'écran)
    score_frame_width = min(600, screen_width - 50)
    score_frame = menu.add.frame_h(score_frame_width, 100, align=pygame_menu.locals.ALIGN_CENTER)  # Augmenté la hauteur
    
    # Score Player 1 (Blacks)
    player1_frame_width = min(250, score_frame_width // 2 - 20)
    player1_frame = menu.add.frame_v(player1_frame_width, 90, max_width=player1_frame_width, max_height=90)  # Augmenté la hauteur
    if player1_house:
        player1_frame.pack(menu.add.label(f"Player 1 ({player1_house})", font_size=18), align=pygame_menu.locals.ALIGN_CENTER)  # Réduit la taille
    else:
        player1_frame.pack(menu.add.label("Player 1 (Black)", font_size=18), align=pygame_menu.locals.ALIGN_CENTER)  # Réduit la taille
    player1_frame.pack(menu.add.label(f"Score: {blacks}", font_size=22), align=pygame_menu.locals.ALIGN_CENTER)  # Réduit la taille
    
    # Score Player 2 (Whites)  
    player2_frame_width = min(250, score_frame_width // 2 - 20)
    player2_frame = menu.add.frame_v(player2_frame_width, 90, max_width=player2_frame_width, max_height=90)  # Augmenté la hauteur
    if player2_house:
        player2_frame.pack(menu.add.label(f"Player 2 ({player2_house})", font_size=18), align=pygame_menu.locals.ALIGN_CENTER)  # Réduit la taille
    else:
        player2_frame.pack(menu.add.label("Player 2 (White)", font_size=18), align=pygame_menu.locals.ALIGN_CENTER)  # Réduit la taille
    player2_frame.pack(menu.add.label(f"Score: {whites}", font_size=22), align=pygame_menu.locals.ALIGN_CENTER)  # Réduit la taille
    
    score_frame.pack(player1_frame, align=pygame_menu.locals.ALIGN_CENTER, margin=(5, 0))
    score_frame.pack(player2_frame, align=pygame_menu.locals.ALIGN_CENTER, margin=(5, 0))
    
    # Boutons d'action
    menu.add.vertical_margin(20)
    
    button_frame_width = min(350, screen_width - 50)
    button_frame = menu.add.frame_h(button_frame_width, 60, align=pygame_menu.locals.ALIGN_CENTER)  # Augmenté la hauteur
    
    if on_play_again:
        time.sleep(2)
        play_again_btn = menu.add.button('Play Again', on_play_again)
        play_again_btn.set_max_width(150)
        button_frame.pack(play_again_btn, align=pygame_menu.locals.ALIGN_CENTER, margin=(5, 0))
    
    if on_quit:
        quit_btn = menu.add.button('Quit', on_quit)
        quit_btn.set_max_width(150)
        button_frame.pack(quit_btn, align=pygame_menu.locals.ALIGN_CENTER, margin=(5, 0))
    
    # Lancer le menu
    menu.mainloop(screen)


def show_default_end_screen(screen, winner, blacks=0, whites=0, on_play_again=None, on_quit=None):
    """
    Affiche l'écran de fin de jeu pour le thème par défaut
    
    Args:
        screen: L'écran pygame
        winner: Le gagnant (BLACK, WHITE, ou None pour égalité)
        blacks: Score des pions noirs
        whites: Score des pions blancs
        on_play_again: Fonction à appeler pour rejouer
        on_quit: Fonction à appeler pour quitter
    """
    
    # Obtenir la taille de l'écran
    screen_width, screen_height = screen.get_size()
    
    # Thème par défaut
    default_theme = pygame_menu.themes.THEME_DARK
    
    # Créer le menu de fin avec la taille de l'écran
    menu = pygame_menu.Menu('Game Over', width=screen_width, height=screen_height, theme=default_theme)
    
    # Titre selon le gagnant
    if winner is not None:
        winner_text = "Black Wins!" if winner == 0 else "White Wins!"  # BLACK = 0, WHITE = 1
        menu.add.label(winner_text, font_size=50, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 30)
    else:
        menu.add.label("Draw!", font_size=50, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 30)
    
    # Scores
    menu.add.label("Final Scores", font_size=35, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 20)
    menu.add.label(f"Black: {blacks}", font_size=25, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 10)
    menu.add.label(f"White: {whites}", font_size=25, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 10)
    
    # Boutons d'action
    menu.add.vertical_margin(30)
    
    if on_play_again:
        time.sleep(2)
        menu.add.button('Play Again', on_play_again)
    
    if on_quit:
        menu.add.button('Quit', on_quit)
    
    # Lancer le menu
    menu.mainloop(screen)