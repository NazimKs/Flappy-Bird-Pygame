import pygame, sys, random;
def draw_screen(floor_x_pos):
    screen.blit(floor_surface, (floor_x_pos, 600))
    screen.blit(floor_surface, (floor_x_pos+384, 600))
def create_pipe():
    random_pos_pipe = random.choice(pipe_height)
    new_pipetop = pipe_surface.get_rect(midtop=(500, random_pos_pipe))
    new_pipebottom = pipe_surface.get_rect(midbottom=(500, random_pos_pipe-200))
    return (new_pipebottom, new_pipetop)
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if(pipe.bottom >= 682):
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe_screen = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe_screen,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.bottom <= -66 or bird_rect.top >= 600:
        death_sound.play()
        return False
    return True
def rotate_bird(bird):
     new_bird = pygame.transform.rotozoom(bird, bird_movement * 1.5, 1)
     return new_bird
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(66, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score : {str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(192, 66))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score : {str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(192, 66))
        screen.blit(score_surface, score_rect)
        highscore_surface = game_font.render(f'High Score : {str(int(highscore))}', True, (255, 255, 255))
        highscore_rect = highscore_surface.get_rect(center=(192, 560))
        screen.blit(highscore_surface, highscore_rect)
def update_score(score,highscore):
    if score > highscore:
        highscore = score
    return highscore
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((384, 682))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 30)
#Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
highscore = 0

bg_surface = pygame.transform.scale(pygame.image.load('assets/background-day.png'), (384, 682)).convert()
floor_surface = pygame.transform.scale(pygame.image.load('assets/base.png'), (448, 150)).convert()
floor_x_pos = 0

bird_downflap = pygame.transform.scale(pygame.image.load('assets/bluebird-downflap.png'), (51, 36)).convert_alpha()
bird_midflap = pygame.transform.scale(pygame.image.load('assets/bluebird-midflap.png'), (51, 36)).convert_alpha()
bird_upflap = pygame.transform.scale(pygame.image.load('assets/bluebird-upflap.png'), (51, 36)).convert_alpha()

bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames [bird_index]
bird_rect = bird_surface.get_rect(center=(66, 341))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.transform.scale(pygame.image.load('assets/pipe-green.png'), (78, 480)).convert()
pipe_list = []
pipe_height = [266, 400, 533]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

gameover_screen = pygame.transform.scale(pygame.image.load('assets/message.png'), (250, 360)).convert_alpha()
gameover_rect = gameover_screen.get_rect(center=(192, 341))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_die.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
flap_sound.set_volume(0.05)
death_sound.set_volume(0.2)
score_sound.set_volume(0)
score_countdown = 200
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and not(game_active):
                game_active = True
                pipe_list.clear()
                bird_rect.center = (66, 341)
                bird_movement = 0
                bird_movement -= 7
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index <2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()
    screen.blit(bg_surface, (0, 0))
    if game_active:
    #bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird_surface = rotate_bird(bird_surface)
        screen.blit(rotated_bird_surface,bird_rect)
        game_active = check_collision(pipe_list)
    #pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 1/150
        score_display('main_game')
        score_countdown -= 1
        if score_countdown == 0:
            score_sound.play()
            score_countdown = 150
    else:
        screen.blit(gameover_screen, gameover_rect)
        highscore = update_score(score, highscore)
        score_display('game_over')
        score_countdown = 200
    #floor
    floor_x_pos -= 1
    draw_screen(floor_x_pos)
    if floor_x_pos == -384:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(90)