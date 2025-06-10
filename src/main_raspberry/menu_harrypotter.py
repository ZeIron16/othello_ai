import os
import pygame_menu
import pygame

current_theme_str = ["Harry_Potter"]

harry_potter_theme = pygame_menu.Theme(
    background_color=pygame_menu.baseimage.BaseImage(
        os.path.join('assets', 'Harry_Potter', 'bg_parchment2.png'),
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL, # <-- Reviens à FILL
    ),
    title_font=os.path.join('assets', 'fonts', 'HARRYP__.TTF'),
    widget_font=os.path.join('assets', 'fonts', 'HARRYP__.TTF'),
    widget_font_color=(150, 100, 20), # Le jaune doré foncé que nous avons défini
    widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(),
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
)

default_theme = pygame_menu.themes.THEME_DARK
selected_theme = harry_potter_theme if current_theme_str[0] == "Harry_Potter" else default_theme




def show_harry_potter_house_selector(screen, on_selection_done, on_cancel):
    screen = pygame.display.set_mode((1000, 800))
    menu_width, menu_height = screen.get_size()
    menu = pygame_menu.Menu('', menu_width, menu_height, theme=selected_theme)
    houses = ['gryffindor', 'slytherin', 'ravenclaw', 'hufflepuff']

    player1_house = [None]
    player2_house = [None]
    selecting_player = [1]
    selection_in_progress = [False]

    def create_house_click_handler(house_name):
        """Create a proper closure for each house button"""
        def on_house_clicked():
            if selection_in_progress[0]:
                return
            
            selection_in_progress[0] = True
            
            if selecting_player[0] == 1:
                player1_house[0] = house_name
                selecting_player[0] = 2
                selection_in_progress[0] = False
                draw_house_buttons()
            else:
                if house_name != player1_house[0]:
                    player2_house[0] = house_name
                    menu.disable()
                    on_selection_done(player1_house[0], player2_house[0])
                else:
                    selection_in_progress[0] = False
        
        return on_house_clicked

    def draw_house_buttons():
        menu.clear()
        
        # Title
        menu.add.label("Select Houses", font_size=60, align=pygame_menu.locals.ALIGN_CENTER).set_margin(0, 10)
        
        # Player instruction
        if selecting_player[0] == 1:
            menu.add.label("Player 1: Choose your house").set_margin(0, 10)
        else:
            menu.add.label("Player 2: Choose your house").set_margin(0, 10)
            menu.add.label(f"(Player 1 chose {player1_house[0]})", font_size=30).set_margin(0, 0)

        house_row = menu.add.frame_h(900, 280, align=pygame_menu.locals.ALIGN_CENTER, max_width=900, max_height=280)

        for house in houses:
            # Create a vertical frame for each house
            house_frame = menu.add.frame_v(200, 260, max_width=200, max_height=260)
            
            # Image container frame (helps with centering)
            image_frame = menu.add.frame_v(180, 180, background_color=(0, 0, 0, 0))  # Transparent
            
            try:
                image_path = f'assets/Harry_Potter/houses/{house}.png'
                image_widget = menu.add.image(image_path, scale=(0.90, 0.90))
                
                # Center the image in its frame
                image_frame.pack(image_widget, align=pygame_menu.locals.ALIGN_CENTER, vertical_position=pygame_menu.locals.POSITION_CENTER)
                image_frame.set_margin(0, 0)
                
            except (FileNotFoundError, pygame.error) as e:
                print(f"Warning: Could not load image for {house}: {e}")
                placeholder = menu.add.label(f"[{house}]", font_size=16)
                image_frame.pack(placeholder, align=pygame_menu.locals.ALIGN_CENTER)
            
            # Add the image frame to the house frame
            house_frame.pack(image_frame, align=pygame_menu.locals.ALIGN_CENTER)
            
            # Create button
            is_taken = selecting_player[0] == 2 and house == player1_house[0]
            
            if is_taken:
                button = menu.add.button("TAKEN", create_house_click_handler(house))
                button.readonly = True
                button.set_background_color((100, 100, 100))
            else:
                button = menu.add.button(house.capitalize(), create_house_click_handler(house))
            
            button.set_max_width(180)
            button.set_margin(5, 0)  # Small top margin to separate from image
            
            # Add button to house frame
            house_frame.pack(button, align=pygame_menu.locals.ALIGN_CENTER)
            
            # Add house frame to row
            house_row.pack(house_frame, align=pygame_menu.locals.ALIGN_CENTER, margin=(10, 0))

        menu.add.vertical_margin(20) 
        menu.add.button('Back', on_cancel)

    # Initial setup
    draw_house_buttons()
    menu.mainloop(screen)