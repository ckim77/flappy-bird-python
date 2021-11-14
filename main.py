import pygame
import sys
import random


def show_score():
    score_surface = font.render ("Score :" + str(score), True, (255,255,255))
    score_rect = score_surface.get_rect(center = (35, bird_rect.centery))
    screen.blit(score_surface, score_rect)

def game_floor():
    screen.blit(floor_base,(floor_x_pos, 900))
    screen.blit(floor_base,(floor_x_pos + 576, 900))

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False    

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        die_sound.play()
        return False
    return True

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = bottom_pipe = pipe_surface.get_rect(midbottom = (1000, random_pipe_pos - 300))
    bottom_pipe = pipe_surface.get_rect(midtop = (1000, random_pipe_pos))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else: 
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

pygame.init()
clock = pygame.time.Clock()

#variables
font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
gravity = 0.25
bird_movement = 0

screen = pygame.display.set_mode((1000, 1024))

#bg
background = pygame.image.load("pictures/bball-background.jpeg").convert()
background = pygame.transform.scale(background, (1000, 1024))

#bird
bird = pygame.image.load("pictures/lbj-head.png").convert_alpha()
bird = pygame.transform.scale(bird, (50,50))
bird_rect = bird.get_rect(center=(100,512))

#floor
floor_base = pygame.image.load("pictures/ground.png").convert()
floor_base = pygame.transform.scale(floor_base, (1000, 1024))
floor_x_pos = 0

#message
message = pygame.image.load("pictures/start.jpeg").convert_alpha()
message = pygame.transform.scale(message, (1000, 1024))
game_over_rect = message.get_rect(center = (500, 512))

#pipes
pipe_surface = pygame.image.load("pictures/pipe.jpeg")
pipe_surface = pygame.transform.scale(pipe_surface, (80, 1024))

pipe_list = []
pipe_height = [400, 600, 800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

flap_sound = pygame.mixer.Sound('sound/sfx_wing.mp3')
die_sound = pygame.mixer.Sound('sound/lebron-james.mp3')

game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
                score += 1
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100, 512)
                bird_movement = 0
                pipe_list.clear()
                game_active = True
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.blit(background, (0,0))
    
    # function for game over
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)

        # draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # collision checker, restarts the game
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)
    
    # create floor
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)

