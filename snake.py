import time, os

import pygame,pygame_menu,random
pygame.init()
WIDTH = 800
HEIGHT = 600
FPS = 5
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

def disable():
    global state
    mainmenu.disable()
    state = "game"
def eat(xcoord,ycoord):
    global all_food
    for food in all_food:
        if food[0]-snake_block<=xcoord<=food[0]+snake_block:
            if food[1]-snake_block<=ycoord<=food[1]+snake_block:
                all_food.remove(food)
                return True
    else: return False
def loose():
    global play_btn, label_id, snake_list, x1, y1, x1_change, y1_change, length
    if ((snake_head in snake_list[:-1]) and length >=4) or (x1 < 0 or x1 >= WIDTH or y1 < 0 or y1 >= HEIGHT):
            label = mainmenu.add.label(f"Счёт: {length}")
            label_id = label.get_id()
            mainmenu.move_widget_index(label, 0)
            mainmenu.set_title("ПРОИГРАЛ")
            play_btn.set_title('Играть заново')
            mainmenu.enable()
            state = "menu"
            snake_list = []
            x1 = WIDTH / 2
            y1 = HEIGHT / 2
            snake_block = 30
            snake_step = 30
            x1_change = 0
            y1_change = 0
            length = 1
            return True
num_of_food = 1
def rnge_slider_on_change(value):
    global num_of_food
    num_of_food = value

mainmenu = pygame_menu.Menu('ЗМЕЙКА',width=WIDTH,height=HEIGHT)
play_btn = mainmenu.add.button('Играть', disable)
mainmenu.add.range_slider("Сложность", 1, (1, 2, 3, 4, 5), onchange=rnge_slider_on_change)
mainmenu.add.button('Выход', quit)

snake_list = []
x1 = WIDTH / 2
y1 = HEIGHT / 2
snake_block = 30
snake_step = 30
x1_change = 0
y1_change = 0
length = 1
names = os.listdir("img/food")
foods = []
for food in names:
   foods.append(pygame.image.load(f"img/food/{food}"))

def generate_food():
    global  all_food
    while len(all_food)<num_of_food:
        foodx = random.randrange(0, WIDTH - snake_block)
        foody = random.randrange(0, HEIGHT - snake_block)
        food_spr = pygame.transform.scale(random.choice(foods), (snake_block, snake_block))
        food_rect = food_spr.get_rect(x=foodx, y=foody)
        all_food.append((foodx, foody,food_spr,food_rect))
    else:
        for i in range(len(all_food)):
            food_data = all_food[i]
            food = food_data[2]
            food_rect = food_data[3]

            screen.blit(food,food_rect)
names = os.listdir("img/food")
snake = []
for food in names:
    snake.append(pygame.image.load(f"img/food/{food}"))
head_sprites = [
   pygame.image.load("img/HeadR.png"),
   pygame.image.load("img/HeadL.png"),
   pygame.image.load("img/HeadB.png"),
   pygame.image.load("img/HeadT.png")
]
tail_sprites = [
   pygame.image.load("img/tailright.png"),
   pygame.image.load("img/tailleft.png"),
   pygame.image.load("img/taildown.png"),
   pygame.image.load("img/tailup.png")
]

snake_side = 0
def draw_head (snake_side,snake_list):
    snake_head_img = head_sprites[snake_side]
    snake_head = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
    snake_head_rect = snake_head.get_rect(x=snake_list[-1][0], y=snake_list[-1][1])
    screen.blit(snake_head,snake_head_rect)
tail_side = 0
tail_list = []
def draw_tail (tail_side,tail_list):
    tail_img = tail_sprites[tail_side]
    tail_head = pygame.transform.scale(tail_img, (snake_block, snake_block))
    tail_head_rect = tail_head.get_rect(x=snake_list[0][0], y=snake_list[0][1])
    screen.blit(tail_head,tail_head_rect)

all_food = []
generate_food()
bg_image = pygame.image.load("img/bg.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
bg_rect = bg_image.get_rect()
run = True
while run:
    clock.tick(FPS)
    events = pygame.event.get()
    x1 += x1_change
    y1 += y1_change
    screen.fill("white")
    screen.blit(bg_image, bg_rect)
    snake_head = [x1, y1]
    generate_food()


    snake_list.append(snake_head)

    if eat(x1, y1):
        generate_food()
        length += 1

    if len(snake_list) > length:
        del snake_list[0]
    loose()
    for x in snake_list[0:]:
        snake_img = pygame.image.load('img/body.png')
        snake = pygame.transform.scale(snake_img, (snake_block, snake_block))
        snake.set_colorkey("white")
        screen.blit(snake, (x[0], x[1]))

    for event in events:


        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                state = "menu"
                mainmenu.enable()
            if event.key == pygame.K_RIGHT:
                x1_change = snake_step
                y1_change = 0
                snake_side=0
            if event.key == pygame.K_LEFT:
                x1_change = -snake_step
                y1_change = 0
                snake_side=1
            if event.key == pygame.K_DOWN:
                y1_change = snake_step
                x1_change = 0
                snake_side=2
            if event.key == pygame.K_UP:
                y1_change = -snake_step
                x1_change = 0
                snake_side=3
    draw_head(snake_side=snake_side, snake_list=snake_list)
    draw_tail(tail_side=snake_side, tail_list=snake_list)
    if mainmenu.is_enabled():
        mainmenu.mainloop(screen)
    pygame.display.flip()




pygame.quit()
