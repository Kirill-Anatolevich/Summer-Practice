import random
import time

import pygame
import pygame as pg

pg.init()

WIDTH = 810
HEIGHT = 810

SIZE = 30

score = 0




def print_text(scene, message, x, y, font_color=(30, 0, 0), font_type='Kingthings_Petrock.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    scene.blit(text, (x, y))


class Button:

    def __init__(self, width, height, inactive_color, active_color, action=None):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.button_sound = pygame.mixer.Sound('click.wav')
        self.action = action


    def draw(self, scene, xbtn, ybtn, xtxt, ytxt, text):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        self.xbtn = xbtn
        self.ybtn = ybtn
        self.xtxt = xtxt
        self.ytxt = ytxt
        self.text = text
        self.scene = scene
        if (self.xbtn < mouse[0] < self.xbtn + self.width and self.ybtn < mouse[1] < self.ybtn + self.height):
            pygame.draw.rect(self.scene, pygame.Color(self.active_color),
                             (self.xbtn, self.ybtn, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.Sound.play(self.button_sound)
                pygame.time.delay(150)
                if self.action is not None:
                    self.action()

        else:
            pygame.draw.rect(self.scene, pygame.Color(self.inactive_color),
                             (self.xbtn, self.ybtn, self.width, self.height))

        print_text(scene=self.scene, x=self.xbtn + self.xtxt, y=self.ybtn + self.ytxt, message=self.text)


class Snake:

    def __init__(self, surface, speed):
        self.length = 1
        self.speed = speed
        self.surface = surface
        self.x = 360
        self.y = 360
        self.snake = [(self.x, self.y)]
        self.dx = 0
        self.dy = 0
        self.size = 30

    def draw(self):
        [(pg.draw.rect(self.surface, (31, 174, 233), (i, j, self.size - 1, self.size - 1))) for i, j in self.snake]
        self.x += self.dx * self.size
        self.y += self.dy * self.size
        self.snake.append((self.x, self.y))
        self.snake = self.snake[-self.length:]
        self.speed = 0


class Apple:
    def __init__(self, surface, size, img=None):
        self.img = img
        self.size = size
        self.surface = surface
        self.x = random.randrange(self.size, WIDTH - self.size, self.size)
        self.y = random.randrange(self.size, WIDTH - self.size, self.size)
        self.time = 180

    def newCords(self):
        self.x = random.randrange(self.size, WIDTH - self.size, self.size)
        self.y = random.randrange(self.size, WIDTH - self.size, self.size)
        self.time = 210

    def draw(self):
        pg.draw.rect(self.surface, (255, 0, 0), (self.x, self.y, self.size, self.size))
        pg.draw.rect(self.surface, (0, 0, 0), (820 - 2, 720 - 2, 210 + 4, 20 + 4), 2)
        pg.draw.rect(self.surface, (255, 0, 0), (820, 720, self.time, 20))
        self.time -= 2
        if self.time < 0:
            self.newCords()


sc = pg.display.set_mode((WIDTH + 300, HEIGHT))
pg.display.set_caption("Snake")
background_game = pg.image.load('img.jpg').convert()
background_menu = pg.image.load('snake.jpg').convert()

clock = pg.time.Clock()
FPS = 10

dirs = {'W': True, 'S': True, 'A': True, 'D': True}

snake = Snake(sc, 5)
apple = Apple(sc, 30)


def eat_apple(snake, apple):
    if snake.snake[-1] == (apple.x, apple.y):
        snake.length += 1
        apple.newCords()
        global score
        score += 5
        if score % 50 == 0:
            global FPS
            FPS += 2


font_end = pygame.font.SysFont('Arial', 66, bold=True)

def exit_game():
    exit()


def game_over(snake, apple):
    duration_of_the_game = time.time() - game_time
    print(duration_of_the_game)
    btn_new_game = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                          action=new_game)
    btn_exit = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                          action=exit_game)
    if len(snake.snake) != len(
            set(snake.snake)) or snake.x > WIDTH - SIZE or snake.x < 0 or snake.y > HEIGHT - SIZE or snake.y < 0:
        while True:
            btn_new_game.draw(sc, xbtn=300, ybtn=370, xtxt=40, ytxt=2, text="NEW GAME")
            btn_exit.draw(sc, xbtn=300, ybtn=480, xtxt=80, ytxt=2, text="EXIT")
            print_text(sc, "GAME OVER", 80, 150, font_color=(255, 140, 0), font_size=150)
            pygame.display.flip()
            for evetn in pygame.event.get():
                if evetn.type == pygame.QUIT:
                    exit()


pause_flag = True

def new_game():
    global snake
    global apple
    global game_time
    global score
    global dirs
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    snake.length = 1
    snake.x = 330
    snake.y = 330
    apple.newCords()
    game_time = time.time()
    score = 0
    game()

deltime = 0
def pause():
    global pause_time
    global pause_flag
    global deltime
    pause_flag = True
    pause_time = time.time()

    def change():
        global pause_flag
        pause_flag = False

    btn_return = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128), action=change)
    btn_new_game = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                        action=new_game)
    while pause_flag:
        btn_return.draw(sc, xbtn=300, ybtn=310, xtxt=60, ytxt=2, text="RETURN")
        btn_new_game.draw(sc, xbtn=300, ybtn=370, xtxt=40, ytxt=2, text="NEW GAME")
        print_text(sc, "PAUSE", 200, 150, font_color=(255, 140, 0), font_size=150)
        pg.draw.rect(sc, (80, 0, 3), (810, 0, 300, 810))
        print_text(sc, "SCORE:" + str(score), 820, 30, font_color=(255, 140, 0), font_size=40)
        print_text(sc, "TIME:" + time.strftime("%X", time.gmtime(current_time - game_time)), 820, 70,
                   font_color=(255, 140, 0), font_size=40)

        close_window()
        pg.display.flip()
    deltime = time.time() - pause_time
    print(deltime)

def display():
    global game_time
    global  current_time
    global deltime
    current_time = time.time()
    pg.draw.rect(sc, (80, 0, 3), (810, 0, 300, 810))
    btn_pause = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128), action=pause)
    btn_pause.draw(sc, xbtn=840, ybtn=300, xtxt=65, ytxt=2, text="PAUSE")
    print_text(sc, "SCORE:" + str(score), 820, 30, font_color=(255, 140, 0), font_size=40)
    game_time += deltime
    if deltime != 0:
        timegame = current_time - deltime
        deltime = 0
    else:
        timegame = current_time - game_time
    print_text(sc, "TIME:" + time.strftime("%X", time.gmtime(timegame)), 820, 70,
               font_color=(255, 140, 0), font_size=40)


font_score = pygame.font.SysFont('Arial', 26, bold=True)

game_time = 0
current_time = 0


def start_game():
    game()


def close_window():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()


def start_menu():
    sc.blit(background_menu, (-100, 0))
    btn_start_game = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                            action=start_game)
    btn_exit = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                      action=exit_game)
    while True:
        btn_start_game.draw(sc, xbtn=450, ybtn=350, xtxt=65, ytxt=2, text="START")
        btn_exit.draw(sc, xbtn=450, ybtn=440, xtxt=80, ytxt=2, text="EXIT")
        pg.display.flip()
        clock.tick(FPS)
        close_window()


def game():
    global game_time
    game_time = time.time()
    global dirs
    while True:
        sc.blit(background_game, (0, 0))
        snake.draw()
        display()
        apple.draw()
        eat_apple(snake, apple)
        game_over(snake, apple)
        # render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))

        pg.display.flip()
        clock.tick(FPS)

        close_window()

        key = pygame.key.get_pressed()
        if key[pygame.K_w] and dirs['W']:
            snake.dx, snake.dy = 0, -1
            dirs = {'W': True, 'S': False, 'A': True, 'D': True}
        if key[pygame.K_s] and dirs['S']:
            snake.dx, snake.dy = 0, 1
            dirs = {'W': False, 'S': True, 'A': True, 'D': True}
        if key[pygame.K_a] and dirs['A']:
            snake.dx, snake.dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': False}
        if key[pygame.K_d] and dirs['D']:
            snake.dx, snake.dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': False, 'D': True}


while True:
    start_menu()
