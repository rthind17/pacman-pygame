import pygame
import sys
import copy
from settings import *
from player_class import * 
from enemy_class import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = maze_width//COLS
        self.cell_height = maze_height//ROWS
        self.walls = []
        self.mars = []
        self.enemies = []
        self.enemy_pos = []
        self.player_pos = None
        self.load()
        self.player = Player(self, vec(self.player_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()

            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            elif self.state == 'GAME OVER':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()

            else:
                self.running = False

            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

########################## HELPER FUNCTIONS ###############################
    def draw_text(self, words, screen, pos, color, Font, center=False):
        text = Font.render(words, False, color)
        text_size = text.get_size()
        
        if center:
            pos[0] = pos[0] - text_size[0]/2
            pos[1] = pos[1] - text_size[1]/2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze1.png')
        self.background = pygame.transform.scale(self.background, (maze_width, maze_height))

        #Opening walls file
        #Create walls list with coordinates of walls
        #Stored as a vector
        with open ("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.mars.append(vec(xidx, yidx))
                    elif char == "P":
                        self.player_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.enemy_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, black, (xidx*self.cell_width, yidx*self.cell_height, self.cell_width, self.cell_height))


    def make_enemies(self):
        for idx, pos in enumerate(self.enemy_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))



############################### GRID FUNCTION #############################
    def draw_grid(self):
        for x in range(width//self.cell_width):
            pygame.draw.line(self.background, grey, (x*self.cell_width, 0), (x*self.cell_width, height))

        for x in range(height//self.cell_height):
            pygame.draw.line(self.background, grey, (0, x*self.cell_height), (width, x*self.cell_height))

        #for mars in self.mars:
           # pygame.draw.rect(self.background, (184, 4, 4), (mars.x*self.cell_width, mars.y*self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0 
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.mars = []
        with open ("walls.txt", "r") as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "C":
                        self.mars.append(vec(xidx, yidx))
        self.state = "playing"       

        
######################## START SCREEN FUNCTIONS ###########################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(black)
        self.draw_text(
                '1 PLAYER ONLY',
                self.screen,
                [width/2, height/2+25],
                (41, 198, 230),
                pygame.font.SysFont('arial black', 20),
                center=True
        )

        self.draw_text(
                'PUSH SPACE BAR!',
                self.screen,
                [width/2, height/2+50],
                (245, 165, 17),
                pygame.font.SysFont('arial black', 20),
                center=True
        )

        self.draw_text(
                'namco',
                self.screen,
                [width/2, height/2+100],
                (184, 4, 4),
                pygame.font.SysFont('arial black', 30),
                center=True
        )

        self.draw_text(
                'TM & ... 2019 NAMCO LTD.',
                self.screen,
                [width/2, height/2+125],
                (227, 227, 227),
                pygame.font.SysFont('arial black', 20),
                center=True
        )

        self.draw_text(
                'NAMCO HOMETEK, INC.',
                self.screen,
                [width/2, height/2+150],
                (227, 227, 227),
                pygame.font.SysFont('arial black', 20),
                center=True
        )

        self.draw_text(
                'LICENSED BY RAJAN THIND',
                self.screen,
                [width/2, height/2+175],
                (227, 227, 227),
                pygame.font.SysFont('arial black', 20),
                center=True
        )

        self.draw_text(
                'PAC-MAN',
                self.screen,
                [width/2, height/5],
                (247, 247, 20),
                pygame.font.Font(font_path, font_size),
                center=True
        )

        self.draw_text(
                'HIGH SCORE:',
                self.screen,
                [4, 2],
                (184, 4, 4),
                pygame.font.SysFont('arial black', 25)
        )
        pygame.display.update()

########################## PLAYING FUNCTIONS ##############################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.player_move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.player_move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.player_move(vec(0, -1)) 
                if event.key == pygame.K_DOWN:
                    self.player.player_move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(black)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_mars()
        
        #self.draw_grid()
        
        self.draw_text(
                'HIGH   SCORE:   0',
                self.screen,  
                [10, 4],
                (227, 227, 227),
                pygame.font.SysFont('arial black', 25) 
        )

        self.draw_text(
                'CURRENT   SCORE:   {}'.format(self.player.current_score),
                self.screen,
                [width//2, 4],
                (227, 227, 227),
                pygame.font.SysFont('arial black', 25)
        )

        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "GAME OVER"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_mars(self):
        for mars in self.mars:
            pygame.draw.circle(self.screen, (184, 4, 4), 
            (int(mars.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2, 
            int(mars.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

############################ GAME OVER FUNCTIONS ##########################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(black)
        self.draw_text(
                "GAME OVER",
                self.screen,
                [width//2, 100],
                (184, 4, 4),
                pygame.font.SysFont('arial', 50),
                center=True
            )
        self.draw_text(
                "Press SPACE BAR To Play Again",
                self.screen,
                [width//2, height//2],
                (227, 227, 227),
                pygame.font.SysFont('arial', 40),
                center=True
            )
        self.draw_text(
                "Press ESC To Quit",
                self.screen,
                [width//2, height//2+50],
                (227, 227, 227),
                pygame.font.SysFont('arial', 40),
                center=True
            )


        pygame.display.update()
            



