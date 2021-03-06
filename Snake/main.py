import random
import time
import sqlite

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
        self.length = 2
        self.speed = speed
        self.size = 30
        self.surface = surface
        self.x = 360
        self.y = 360
        self.snake = [(self.x, self.y), (self.x - self.size, self.y - self.size)]
        self.dx = 0
        self.dy = -1

    def draw(self):
        if self.dy == -1:
            x, y = self.snake[len(self.snake) - 1]
            sc.blit(snake_head_up, (x - 6, y - 15))
            for i in range(len(self.snake) - 1):
                x, y = self.snake[i]
                sc.blit(snake_body, (x, y))
        elif self.dy == 1:
            x, y = self.snake[len(self.snake) - 1]
            sc.blit(snake_head_down, (x - 14, y - 6))
            for i in range(len(self.snake) - 1):
                x, y = self.snake[i]
                sc.blit(snake_body, (x, y))
        elif self.dx == 1:
            x, y = self.snake[len(self.snake) - 1]
            sc.blit(snake_head_right, (x - 5, y - 5))
            for i in range(len(self.snake) - 1):
                x, y = self.snake[i]
                sc.blit(snake_body, (x, y))
        elif self.dx == -1:
            x, y = self.snake[len(self.snake) - 1]
            sc.blit(snake_head_left, (x - 15, y - 15))
            for i in range(len(self.snake) - 1):
                x, y = self.snake[i]
                sc.blit(snake_body, (x, y))

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
        sc.blit(apple_img, (self.x, self.y))
        pg.draw.rect(self.surface, (0, 0, 0), (820 - 2, 720 - 2, 210 + 4, 20 + 4), 2)
        pg.draw.rect(self.surface, (0, 128, 0), (820, 720, self.time, 20))
        self.time -= 2
        if self.time < 0:
            self.newCords()


sc = pg.display.set_mode((WIDTH + 300, HEIGHT))
pg.display.set_caption("Snake")
background_game = pg.image.load('img.jpg').convert()
background_menu = pg.image.load('snake.jpg').convert()
apple_img = pg.image.load('apple.png').convert()
snake_head_up = pg.image.load('snake_head_up.png')
snake_head_right = pg.image.load('snake_head_right.png')
snake_head_down = pg.image.load('snake_head_down.png')
snake_head_left = pg.image.load('snake_head_left.png')
snake_body = pg.image.load('snake_body.png')


clock = pg.time.Clock()
FPS = 10
deltime = 0
pause_flag = True

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
    btn_new_game = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                          action=new_game)
    btn_exit = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                          action=exit_game)
    btn_start_menu = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                            action=start_menu)
    if len(snake.snake) != len(
            set(snake.snake)) or snake.x > WIDTH - SIZE or snake.x < 0 or snake.y > HEIGHT - SIZE or snake.y < 0:
        data_base.add_result(score, int(duration_of_the_game))
        while True:
            btn_start_menu.draw(sc, xbtn=300, ybtn=450, xtxt=33, ytxt=5, text="MAIN MENU")
            btn_new_game.draw(sc, xbtn=300, ybtn=370, xtxt=40, ytxt=2, text="NEW GAME")
            btn_exit.draw(sc, xbtn=300, ybtn=600, xtxt=80, ytxt=2, text="EXIT")
            print_text(sc, "GAME OVER", 80, 150, font_color=(255, 140, 0), font_size=150)
            pygame.display.flip()
            for evetn in pygame.event.get():
                if evetn.type == pygame.QUIT:
                    exit()



def new_game():
    global snake
    global apple
    global game_time
    global score
    global dirs
    global FPS
    FPS = 10
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    snake.length = 2
    snake.x = 330
    snake.y = 330
    apple.newCords()
    game_time = time.time()
    score = 0
    game()



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
    btn_start_menu = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                            action=start_menu)
    while pause_flag:
        btn_start_menu.draw(sc, xbtn=300, ybtn=600, xtxt=33, ytxt=5, text="MAIN MENU")
        btn_return.draw(sc, xbtn=300, ybtn=310, xtxt=60, ytxt=2, text="RETURN")
        btn_new_game.draw(sc, xbtn=300, ybtn=370, xtxt=40, ytxt=2, text="NEW GAME")
        print_text(sc, "PAUSE", 220, 150, font_color=(255, 140, 0), font_size=150)
        pg.draw.rect(sc, (80, 0, 3), (810, 0, 300, 810))
        print_text(sc, "SCORE:" + str(score), 820, 30, font_color=(255, 140, 0), font_size=40)
        print_text(sc, "TIME:" + time.strftime("%X", time.gmtime(current_time - game_time)), 820, 70,
                   font_color=(255, 140, 0), font_size=40)

        close_window()
        pg.display.flip()
    deltime = time.time() - pause_time


def display():
    global game_time
    global current_time
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


def show_records():
    sc.blit(background_menu, (-100, 0))
    base = data_base.get_result()
    btn_exit = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                      action=exit_game)
    btn_start_menu = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                        action=start_menu)
    print_text(sc, "POSITION:", 0, 10, font_color=(255, 255, 255), font_size=30)
    print_text(sc, "ID GAME:", 150, 10, font_color=(255, 255, 255), font_size=30)
    print_text(sc, "SCORE:", 400, 10, font_color=(255, 255, 255), font_size=30)
    print_text(sc, "TIME:", 650, 10, font_color=(255, 255, 255), font_size=30)
    while True:
        btn_start_menu.draw(sc, xbtn=450, ybtn=620, xtxt=33, ytxt=5, text="MAIN MENU")
        btn_exit.draw(sc, xbtn=450, ybtn=700, xtxt=80, ytxt=5, text="EXIT")
        for i in range(len(base)):
            if i == 7:
                break
            print_text(sc, str(1+i)+ 10*" " + str(base[i][0]) + 15*" " + str(base[i][1]) + 15*" " + str(base[i][2]), 20,
                       100 + 70*i, font_color=(255, 255, 255), font_size=70)
        close_window()
        clock.tick(FPS)
        pg.display.flip()


def start_menu():
    sc.blit(background_menu, (-100, 0))
    btn_start_game = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                            action=start_game)
    btn_exit = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                      action=exit_game)
    btn_record = Button(width=199, height=50, inactive_color=(192, 192, 192), active_color=(128, 128, 128),
                      action=show_records)
    while True:
        btn_start_game.draw(sc, xbtn=450, ybtn=350, xtxt=65, ytxt=5, text="START")
        btn_exit.draw(sc, xbtn=450, ybtn=500, xtxt=80, ytxt=5, text="EXIT")
        btn_record.draw(sc, xbtn=450, ybtn=425, xtxt=33, ytxt=5, text="MY RECORDS")
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
    data_base = sqlite.SQLiter('data_base.db')
    start_menu()