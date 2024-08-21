import pygame
import math
from board import board_array

pygame.init()

WIDTH = 600
HEIGHT = 650
sprite_x_scale = (WIDTH // 30)
sprite_y_scale = ((HEIGHT - 50) // 32)
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf',20)
level = board_array
PI = math.pi
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/pacman/{i}.png'),(sprite_y_scale,sprite_x_scale)))

player_x = 300
player_y = 324
direction = 0
counter = 0
speed = 2
score = 0
powerup_count = 0
powerup = False
collision = 0


def get_coordinates(x_pos,y_pos,x_scale,y_scale):
    center = (x_pos + x_scale // 2, y_pos + y_scale // 2 + 1)
    center_right = (x_pos + x_scale, y_pos + y_scale //2)
    center_left = (x_pos, y_pos + y_scale // 2)
    center_top = (x_pos + x_scale // 2, y_pos)
    center_bottom = (x_pos + x_scale // 2, y_pos + y_scale)
    return center, center_left, center_right, center_top, center_bottom

def transform_coordinates(x_pos,y_pos,x_scale,y_scale):
    px_coordinate = x_pos // x_scale
    py_coordinate = y_pos // y_scale
    return px_coordinate, py_coordinate


def draw_board(lvl,screen,x_scale,y_scale):
    x_scale = (WIDTH // 30)
    y_scale = ((HEIGHT - 50) // 32)
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * x_scale + (0.5 * x_scale), i * y_scale + (0.5 * y_scale)), 4)
            if lvl[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * x_scale + (0.5 * x_scale), i * y_scale + (0.5 * y_scale)), 10)
            if lvl[i][j] == 3:
                pygame.draw.line(screen, 'blue', (j * x_scale + (0.5 * x_scale), i * y_scale),
                                 (j * x_scale + (0.5 * x_scale), i * y_scale + y_scale), 3)
            if lvl[i][j] == 4:
                pygame.draw.line(screen, 'blue', (j * x_scale, i * y_scale + (0.5 * y_scale)),
                                 (j * x_scale + x_scale, i * y_scale + (0.5 * y_scale)), 3)
            if lvl[i][j] == 5:
                # small offset on line
                pygame.draw.arc(screen, 'blue', [(j * x_scale - (x_scale * 0.4)) - 2, (i * y_scale + (0.5 * y_scale)), x_scale, y_scale],
                                0, PI / 2, 3)
            if lvl[i][j] == 6:
                pygame.draw.arc(screen, 'blue',
                                [(j * x_scale + (x_scale * 0.5)), (i * y_scale + (0.5 * y_scale)), x_scale, y_scale], PI / 2, PI, 3)
            if lvl[i][j] == 7:
                pygame.draw.arc(screen, 'blue', [(j * x_scale + (x_scale * 0.5)), (i * y_scale - (0.4 * y_scale)), x_scale, y_scale], PI,
                                3 * PI / 2, 3)
            if lvl[i][j] == 8:
                # small offset on line
                pygame.draw.arc(screen, 'blue',
                                [(j * x_scale - (x_scale * 0.4)) - 2, (i * y_scale - (0.4 * y_scale)), x_scale, y_scale], 3 * PI / 2,
                                2 * PI, 3)
            if lvl[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * x_scale, i * y_scale + (0.5 * y_scale)),
                                 (j * x_scale + x_scale, i * y_scale + (0.5 * y_scale)), 3)

def draw_player(player_x, player_y,screen):
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale // 2,player_y + sprite_y_scale // 2),2)
        pygame.draw.circle(screen,'white',(player_x, player_y),2)
        pygame.draw.circle(screen,'white',(player_x, player_y + sprite_y_scale),2)
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y),2)
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y + sprite_y_scale),2)

    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale // 2,player_y + sprite_y_scale // 2),2)
        pygame.draw.circle(screen,'white',(player_x, player_y),2)
        pygame.draw.circle(screen,'white',(player_x, player_y + sprite_y_scale),2)
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y),2)
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y + sprite_y_scale),2)
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale // 2,player_y + sprite_y_scale // 2),2)
        pygame.draw.circle(screen,'white',(player_x, player_y),2)
        pygame.draw.circle(screen,'white',(player_x, player_y + sprite_y_scale),2)
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y),2)
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y + sprite_y_scale),2)
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale // 2,player_y + sprite_y_scale // 2),2)
        pygame.draw.circle(screen,'white',(player_x, player_y),2)
        pygame.draw.circle(screen,'white',(player_x, player_y + sprite_y_scale),2)
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y),2)
        pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y + sprite_y_scale),2)

def position_check(lvl_map,x_pos,y_pos,x_scale,y_scale):
    center, center_left, center_right, center_top, center_bottom = get_coordinates(x_pos,
                                                                             y_pos,
                                                                             x_scale,
                                                                             y_scale)
    available_moves = [False,False,False,False]
    spaces = [0,1,2]
    cx, cy = transform_coordinates(center[0],center[1],x_scale,y_scale)
    lx, ly = transform_coordinates(center_left[0],center_left[1],x_scale,y_scale)
    rx, ry = transform_coordinates(center_right[0], center_right[1],x_scale,y_scale)
    tx, ty = transform_coordinates(center_top[0], center_top[1],x_scale,y_scale)
    bx, by = transform_coordinates(center_bottom[0], center_bottom[1],x_scale,y_scale)

    #right
    if lvl_map[ry][rx] in spaces:
        available_moves[0] = True
    #left
    if lvl_map[ly][lx] in spaces:
        available_moves[1] = True
    #up
    if lvl_map[ty][tx] in spaces:
        available_moves[2] = True
    #down
    if lvl_map[by][bx] in spaces:
        available_moves[3] = True

    # print(f'{(cx,cy),(rx,ry)}')
    return available_moves, (cx,cy)

def check_collisions(lvl_map,centerx,centery,score):
    collision = 0
    if lvl_map[centery][centerx] in range(1,3):
        if lvl_map[centery][centerx] == 2:
            collision = 1
            score += 1
            lvl_map[centery][centerx] = 0
            return collision, score
        score += 1
        lvl_map[centery][centerx] = 0
        
    return collision, score

#main loop
run = True
while run:
    timer.tick(fps)
    #for pacman animation
    if counter < 19:
        counter += 1
    else:
        counter = 0
    
    #powerup logic
    if powerup and powerup_count < (fps * 10):
        powerup_count += 1
    elif powerup and powerup_count >= (fps * 10):
        powerup_count = 0
        powerup = False


    #drawing
    screen.fill('black')
    draw_board(level,screen,sprite_x_scale,sprite_y_scale)
    draw_player(player_x,player_y,screen)

    #check logic
    available_moves , (centerx, centery) = position_check(level,player_x,player_y,sprite_x_scale,sprite_y_scale)
    collision, score = check_collisions(level,centerx,centery,score)
    if collision == 1:
        powerup = True

    #right
    if direction == 0 and available_moves[0]:
        player_x += 1
    #left
    elif direction == 1 and available_moves[1]:
        player_x -= 1
    #up
    elif direction == 2 and available_moves[2]:
        player_y -= 1
    #down
    elif direction == 3 and available_moves[3]:
        player_y += 1
    

    #key handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 1
            if event.key == pygame.K_UP:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3
                # print(f'player_x is {player_x}')
                # print(f'player_y is {player_y}')
                # print(f'x_coord is {px_coordinate}')
                # print(f'y_coord is {py_coordinate}')
                # print(f'element to the left {level[py_coordinate + 1][px_coordinate]}')
                # print(f'current position is {(py_coordinate, px_coordinate)}')

    
    pygame.display.flip()

pygame.quit()