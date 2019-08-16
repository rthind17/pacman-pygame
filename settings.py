from pygame.math import Vector2 as vec

width = 610
height = 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
maze_width = width - TOP_BOTTOM_BUFFER
maze_height = height - TOP_BOTTOM_BUFFER
ROWS = 30
COLS= 28

#color settings
black = (0, 0, 0)
blue = (0, 251, 255)
grey = (199, 193, 193)
PLAYER_COLOR = (245, 238, 32)
#font
start_text_size = 20
start_screen_font = 'arial black'
font_path = './assets/crackman.ttf'
font_size = 40
#player settings
PLAYER_START_POS = 0
#enemy settings
