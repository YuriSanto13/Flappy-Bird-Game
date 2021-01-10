import pygame
import random
from time import sleep
from pygame.locals import *
SCREEN_WIDTH = 286
SCREEN_HEIGHT = 512
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100
PIPE_WIDTH = 75
PIPE_HEIGHT = 513
PIPE_GAP = 150

# Object Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(), 
        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(), 
        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]
        self.speed = SPEED
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.current_image = 0
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    
    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        # UPDATE HEIGHT
        self.rect[1] += self.speed
    def bump(self):
        self.speed = -SPEED

# Object Pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect[0] -= GAME_SPEED


# Object Ground
class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png')
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        self.rect[0] = xpos

    def update(self):
        self.rect[0] -= GAME_SPEED
# If Object is off screen
def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


# Generate random pipes
def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

# Set screen game
pygame.init()
screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT ))
BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
GAME_OVER = pygame.image.load('assets/sprites/gameover.png')
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)
ground_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
point_group = pygame.sprite.Group()
point = points()
point_group.add(point)

for i in range (2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

for i in range(2):
    ground = Ground(GROUND_WIDTH* i)
    ground_group.add(ground)

clock = pygame.time.Clock()

while True:
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()
    screen.blit(BACKGROUND, (0, 0))
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH - 8)
        ground_group.add(new_ground)
    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        pipes = get_random_pipes(SCREEN_WIDTH * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
    
    bird_group.update()
    ground_group.update()
    pipe_group.update()
    pipe_group.draw(screen)
    ground_group.draw(screen)
    bird_group.draw(screen)
    pygame.display.update()
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
    pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game over 
        screen.blit(GAME_OVER, (47, SCREEN_HEIGHT/2))
        pygame.display.update()
        sleep(10)
        break