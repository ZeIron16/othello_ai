WHITE = 0
BLACK = 1
EMPTY = -1
#Windows size 
WIDTH = 1000
HEIGHT = 800
# Constants for player types
HUMAN = 'human'
COMPUTER = 'computer'
EXTERN = 'extern'

# Language options
LANGUAGES = [
    ('Français', 'fr'),
    ('English', 'en'),
    ('中文', 'zh')
]

# Theme options
THEMES = [
    ('Normal', 'Normal'),
    ('Harry Potter', 'Harry_Potter')
]

AUDIO_OPTIONS = [
    ('On', True),
    ('Off', False)
]

# Default settings
DEFAULT_LANGUAGE = 'en'
DEFAULT_THEME = 'Normal'

# Player options - sera construit dynamiquement selon la langue
PLAYER_OPTIONS = [
    ('Humain', HUMAN),
    ('Ordinateur', COMPUTER),
    ('En ligne', EXTERN)
]

# Translations for UI
TRANSLATIONS = {
    'fr': {
        'play': 'Jouer',
        'quit': 'Quitter',
        'player1': 'Joueur 1',
        'player2': 'Joueur 2',
        'language': 'Langue',
        'theme': 'Thème',
        'human': 'Humain',
        'computer': 'Ordinateur',
        'online': 'En ligne',
        'server_ip': 'IP du serveur',
        'theme_normal': 'Normal',
        'theme_harry_potter': 'Harry Potter',
        'audio': 'Audio',
        'audio_on': 'Activé',
        'audio_off': 'Désactivé'
    },
    'en': {
        'play': 'Play',
        'quit': 'Quit',
        'player1': 'Player 1',
        'player2': 'Player 2',
        'language': 'Language',
        'theme': 'Theme',
        'human': 'Human',
        'computer': 'Computer',
        'online': 'Online',
        'server_ip': 'Server IP',
        'theme_normal': 'Normal',
        'theme_harry_potter': 'Harry Potter',
        'audio': 'Audio',
        'audio_on': 'On',
        'audio_off': 'Off'
    },
    'zh': {
        'play': '开始游戏',
        'quit': '退出',
        'player1': '玩家1',
        'player2': '玩家2',
        'language': '语言',
        'theme': '主题',
        'human': '人类',
        'computer': '电脑',
        'online': '在线',
        'server_ip': '服务器IP',
        'theme_normal': '普通',
        'theme_harry_potter': '哈利波特',
        'audio': '音频',
        'audio_on': '开启',
        'audio_off': '关闭'
    }
}

font_path = 'assets/fonts/NotoSansTC-VariableFont_wght.ttf'