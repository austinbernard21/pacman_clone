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


def get_coordinates(x_pos,y_pos,x_scale,y_scale):
    px_coordinate = x_pos // x_scale
    py_coordinate = y_pos // y_scale
    return px_coordinate, py_coordinate


player_x = 300
player_y = 324
centerx = player_x + sprite_x_scale // 2
centery = player_y + sprite_y_scale // 2 + 1
px_coordinate, py_coordinate = get_coordinates(centerx,centery,
                                               sprite_x_scale,sprite_y_scale)
# px_coordinate = player_x // sprite_x_scale
# py_coordinate = player_y // sprite_y_scale
# player_x, player_y = (px_coordinate * sprite_x_scale ,
#                        py_coordinate * sprite_y_scale)
print(f'player_x is {player_x}')
print(f'player_y is {player_y}')
print(f'x_coord is {px_coordinate}')
print(f'y_coord is {py_coordinate}')
direction = 0
counter = 0
speed = 2

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


def get_available_moves(lvl_map,px_coord,py_coord):
    #right, left, up, down
    available_moves = [False,False,False,False]
    spaces = [0,1,2]
    #right
    if lvl_map[py_coord][px_coord + 1] in spaces:
        available_moves[0] = True
    #left
    if lvl_map[py_coord][px_coord - 1] in spaces:
        available_moves[1] = True
    #up
    if lvl_map[py_coord - 1][px_coord] in spaces:
        available_moves[2] = True
    #down
    if lvl_map[py_coord + 1][px_coord] in spaces:
        available_moves[3] = True

    return available_moves

#main loop
run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
    else:
        counter = 0


    screen.fill('black')
    draw_board(level,screen,sprite_x_scale,sprite_y_scale)
    draw_player(player_x,player_y,screen)
    centerx = player_x + sprite_x_scale // 2
    centery = player_y + sprite_y_scale // 2
    px_coordinate, py_coordinate = get_coordinates(centerx,centery,
                                               sprite_x_scale,sprite_y_scale)
    #r,l,u,d
    available_moves = get_available_moves(level,px_coordinate,py_coordinate)

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
    
    # check_position()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
                print(f'player_x is {player_x}')
                print(f'player_y is {player_y}')
                print(f'x_coord is {px_coordinate}')
                print(f'y_coord is {py_coordinate}')
                print(f'element to the right {level[py_coordinate][px_coordinate+1]}')
                print(f'current position is {(py_coordinate, px_coordinate)}')
            if event.key == pygame.K_LEFT:
                direction = 1
                print(f'player_x is {player_x}')
                print(f'player_y is {player_y}')
                print(f'x_coord is {px_coordinate}')
                print(f'y_coord is {py_coordinate}')
                print(f'element to the left {level[py_coordinate][px_coordinate-1]}')
                print(f'current position is {(py_coordinate, px_coordinate)}')
            if event.key == pygame.K_UP:
                direction = 2
                print(f'player_x is {player_x}')
                print(f'player_y is {player_y}')
                print(f'x_coord is {px_coordinate}')
                print(f'y_coord is {py_coordinate}')
                print(f'element to the top {level[py_coordinate - 1][px_coordinate]}')
                print(f'current position is {(py_coordinate, px_coordinate)}')
            if event.key == pygame.K_DOWN:
                direction = 3
                print(f'player_x is {player_x}')
                print(f'player_y is {player_y}')
                print(f'x_coord is {px_coordinate}')
                print(f'y_coord is {py_coordinate}')
                print(f'element to the left {level[py_coordinate + 1][px_coordinate]}')
                print(f'current position is {(py_coordinate, px_coordinate)}')

    
    pygame.display.flip()

pygame.quit()