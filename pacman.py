import pygame
import math
import random
from board import board_array

class Character():
    def __init__(self, screen, image, direction, 
            x_coord, y_coord, x_scale, y_scale, 
            lvl_map):
        self.screen = screen
        self.image = image
        self.direction = direction
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.lvl_map = lvl_map

    def transform_coordinates(self,x_pos,y_pos,x_scale,y_scale):
        px_coordinate = x_pos // x_scale
        py_coordinate = y_pos // y_scale
        return px_coordinate, py_coordinate
    
    def get_coordinates(self):
        center = (self.x_coord + self.x_scale // 2, self.y_coord + self.y_scale // 2 + 1)
        center_right = (self.x_coord + self.x_scale, self.y_coord + self.y_scale //2)
        center_left = (self.x_coord, self.y_coord + self.y_scale // 2)
        center_top = (self.x_coord + self.x_scale // 2, self.y_coord)
        center_bottom = (self.x_coord + self.x_scale // 2, self.y_coord + self.y_scale)
        return center, center_left, center_right, center_top, center_bottom    
    
    
    def position_check(self):
        center, center_left, center_right, center_top, center_bottom = self.get_coordinates()
        available_moves = [False,False,False,False]
        spaces = [0,1,2]
        cx, cy = self.transform_coordinates(center[0],center[1],self.x_scale,self.y_scale)
        lx, ly = self.transform_coordinates(center_left[0],center_left[1],self.x_scale,self.y_scale)
        rx, ry = self.transform_coordinates(center_right[0], center_right[1],self.x_scale,self.y_scale)
        tx, ty = self.transform_coordinates(center_top[0], center_top[1],self.x_scale,self.y_scale)
        bx, by = self.transform_coordinates(center_bottom[0], center_bottom[1],self.x_scale,self.y_scale)

        #right
        if self.lvl_map[ry][rx] in spaces:
            available_moves[0] = True
        #left
        if self.lvl_map[ly][lx] in spaces:
            available_moves[1] = True
        #up
        if self.lvl_map[ty][tx] in spaces:
            available_moves[2] = True
        #down
        if self.lvl_map[by][bx] in spaces:
            available_moves[3] = True

        return available_moves, (cx,cy)
    


class Player(Character):
    def __init__(self, screen, image, direction, x_coord, y_coord, x_scale, y_scale, lvl_map):
        super().__init__(screen, image, direction, x_coord, y_coord, x_scale, y_scale, lvl_map)

    def draw(self,counter):
        if self.direction == 0:
            self.screen.blit(self.image[counter // 5], (self.x_coord, self.y_coord))
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale // 2,player_y + sprite_y_scale // 2),2)
            # pygame.draw.circle(screen,'white',(player_x, player_y),2)
            # pygame.draw.circle(screen,'white',(player_x, player_y + sprite_y_scale),2)
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y),2)
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y + sprite_y_scale),2)

        elif self.direction == 1:
            self.screen.blit(pygame.transform.flip(self.image[counter // 5], True, False), (self.x_coord, self.y_coord))
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale // 2,player_y + sprite_y_scale // 2),2)
            # pygame.draw.circle(screen,'white',(player_x, player_y),2)
            # pygame.draw.circle(screen,'white',(player_x, player_y + sprite_y_scale),2)
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y),2)
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y + sprite_y_scale),2)
        elif self.direction == 2:
            self.screen.blit(pygame.transform.rotate(self.image[counter // 5], 90), (self.x_coord, self.y_coord))
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale // 2,player_y + sprite_y_scale // 2),2)
            # pygame.draw.circle(screen,'white',(player_x, player_y),2)
            # pygame.draw.circle(screen,'white',(player_x, player_y + sprite_y_scale),2)
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y),2)
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y + sprite_y_scale),2)
        elif self.direction == 3:
            screen.blit(pygame.transform.rotate(self.image[counter // 5], 270), (self.x_coord, self.y_coord))
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale // 2,player_y + sprite_y_scale // 2),2)
            # pygame.draw.circle(screen,'white',(player_x, player_y),2)
            # pygame.draw.circle(screen,'white',(player_x, player_y + sprite_y_scale),2)
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y),2)
            # pygame.draw.circle(screen,'white',(player_x + sprite_x_scale, player_y + sprite_y_scale),2)
    def check_collisions(self,centerx,centery,score):
        collision = 0
        #check for pill
        if self.lvl_map[centery][centerx] in range(1,3):
            if self.lvl_map[centery][centerx] == 2:
                collision = 1
                score += 1
                self.lvl_map[centery][centerx] = 0
                return collision, score
            score += 1
            self.lvl_map[centery][centerx] = 0
            
        return collision, score   

class Ghost(Character):
    def __init__(self, screen, image, direction, 
            x_coord, y_coord, x_scale, y_scale, 
            lvl_map, is_blue=False,
            movement_counter = 0):
        self.screen = screen
        self.image = image
        self.direction = direction
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.lvl_map = lvl_map
        self.is_blue = is_blue
        self.blue_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (self.y_scale, self.x_scale))
        self.movement_counter = movement_counter
        self.original_x = x_coord
        self.original_y = y_coord

    def check_collisions(self,centerx,centery,other_x,other_y):
        collision = 0

        #check if on pacman's square
        if centerx == other_x and centery == other_y:
            collision = 1

        return collision
    
    def set_blue(self,is_blue):
        self.is_blue = is_blue

    def movement_count_plus(self):
        self.movement_counter += 1

    def movement_count_reset(self):
        self.movement_counter = 0

    def draw(self):
        image = self.image
        if self.is_blue:
            image = self.blue_img
        if self.direction == 0:
            self.screen.blit(image, (self.x_coord, self.y_coord))
        elif self.direction == 1:
            self.screen.blit(pygame.transform.flip(image, True, False), (self.x_coord, self.y_coord))
        elif self.direction == 2:
            self.screen.blit(pygame.transform.rotate(image, 90), (self.x_coord, self.y_coord))
        elif self.direction == 3:
            self.screen.blit(pygame.transform.rotate(image, 270), (self.x_coord, self.y_coord))

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

def display_texts(score,lives,screen,won=False,lose=False):
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text,(10,620))
    lives_text = font.render(f'Lives: {lives}', True, 'white')
    screen.blit(lives_text,(510,620))

    if won:
        win_text = font.render('You Won!', True, 'red')
        screen.blit(win_text,(270,310))
    if lose:
        lose_text = font.render('You Lost!', True, 'red')
        screen.blit(lose_text,(270,310))


pygame.init()

WIDTH = 600
HEIGHT = 650
PI = math.pi
sprite_x_scale = (WIDTH // 30)
sprite_y_scale = ((HEIGHT - 50) // 32)
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf',20)
level = board_array
total_points = 0
for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] == 1 or level[i][j] == 2:
            total_points += 1
counter = 0
speed = 2
score = 0
lives = 3
won = False
lose = False
powerup_count = 0
powerup = False
collision = 0  

original_x = 300
original_y = 324

#player setup
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/pacman/{i}.png'),(sprite_y_scale,sprite_x_scale)))
player_x = 300
player_y = 324
direction = 0
pacman = Player(screen,player_images,direction,player_x,player_y,
                sprite_x_scale,sprite_y_scale,level)

#blue ghost
blue_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (sprite_y_scale, sprite_x_scale))
blue_x = 380
blue_y = 128
blue_direction = 0
blue_ghost = Ghost(screen,blue_img,blue_direction,blue_x,blue_y,sprite_x_scale,
                   sprite_y_scale,level)

#orange ghost
orange_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (sprite_y_scale, sprite_x_scale))
orange_x = 60
orange_y = 160
orange_direction = 0
orange_ghost = Ghost(screen,orange_img,orange_direction,orange_x,orange_y,
                     sprite_x_scale,sprite_y_scale,level)

#pink ghost
pink_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (sprite_y_scale, sprite_x_scale))
pink_x = 260
pink_y = 410
pink_direction = 0
pink_ghost = Ghost(screen,pink_img,pink_direction,pink_x,pink_y,sprite_x_scale,
                   sprite_y_scale,level)

#red ghost
red_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (sprite_y_scale, sprite_x_scale))
red_x = 140
red_y = 160
red_direction = 0
red_ghost = Ghost(screen,red_img,red_direction,red_x,red_y,sprite_x_scale,
                  sprite_y_scale,level)

ghosts = [blue_ghost,orange_ghost,pink_ghost,red_ghost]

step_array = [x for x in range(1,5)]
ghost_movement_counter = random.choice(step_array) * fps


#main loop
run = True
while run:
    timer.tick(fps)
    #for pacman animation
    if counter < 19:
        counter += 1
    else:
        counter = 0

    #win condition
    if score == total_points:
        won = True
        print('won')

    #lose condition
    if lives == 0:
        lose = True
        print('lose')

    #powerup logic
    if powerup and powerup_count < (fps * 10):
        powerup_count += 1
    elif powerup and powerup_count >= (fps * 10):
        powerup_count = 0
        powerup = False
        print('powerup done')


    #drawing
    screen.fill('black')
    draw_board(level,screen,sprite_x_scale,sprite_y_scale)
    display_texts(score,lives,screen,won,lose)
    pacman.draw(counter)
    blue_ghost.draw()
    orange_ghost.draw()
    pink_ghost.draw()
    red_ghost.draw()


    #check logic
    available_moves, (centerx, centery) = pacman.position_check()
    collision, score = pacman.check_collisions(centerx,centery,score)
    if collision == 1:
        powerup = True
        print('powerup')

    #player movement
    #right
    if pacman.direction == 0 and available_moves[0]:
        pacman.x_coord += 1 * speed
    #left
    elif pacman.direction == 1 and available_moves[1]:
        pacman.x_coord -= 1 * speed
    #up
    elif pacman.direction == 2 and available_moves[2]:
        pacman.y_coord -= 1 * speed
    #down
    elif pacman.direction == 3 and available_moves[3]:
        pacman.y_coord += 1 * speed

    #ghost logic
    for ghost in ghosts:

        #ghost movement counter to randomly change direction
        if ghost.movement_counter < ghost_movement_counter:
            ghost.movement_count_plus()
        if ghost.movement_counter > ghost_movement_counter:
            ghost.direction = random.choice([x for x in range(4)])
            ghost.movement_count_reset()

        #if powerup activated
        if powerup:
            ghost.set_blue(True)
        else:
            ghost.set_blue(False)

        #check if pacman captured or captured by pacman
        capture = 0
        ghost_moves_available , (ghost_x, ghost_y) = ghost.position_check()
        capture = ghost.check_collisions(centerx,centery,ghost_x,ghost_y)
        if capture == 1 and not powerup:
            # print('captured')
            lives -= 1
            pacman.x_coord = original_x
            pacman.y_coord = original_y
        if capture == 1 and powerup:
            ghost.x_coord = ghost.original_x
            ghost.y_coord = ghost.original_y
            # print('im dead')

        #ghost movement
        #right
        if ghost.direction == 0:
            if ghost_moves_available[0]:
                ghost.x_coord += 1 * speed
            else:
                ghost.direction = random.choice([x for x in range(4)])
        #left
        if ghost.direction == 1:
            if ghost_moves_available[1]:
                ghost.x_coord -= 1 * speed
            else:
                ghost.direction = random.choice([x for x in range(4)])
        #up
        if ghost.direction == 2:
            if ghost_moves_available[2]:
                ghost.y_coord -= 1 * speed
            else:
                ghost.direction = random.choice([x for x in range(4)])
        #down
        if ghost.direction == 3:
            if ghost_moves_available[3]:
                ghost.y_coord += 1 * speed
            else:
                ghost.direction = random.choice([x for x in range(4)])
        

    #key handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman.direction = 0
            if event.key == pygame.K_LEFT:
                pacman.direction = 1
            if event.key == pygame.K_UP:
                pacman.direction = 2
            if event.key == pygame.K_DOWN:
                pacman.direction = 3

    
    pygame.display.flip()

pygame.quit()