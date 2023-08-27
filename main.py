# Name: YuYeon Kim
# Title: Pong!
# Date: April 14, 2023
# Description: Using keyboard input so that 2 players can play the pong game

# https://gist.github.com/vinothpandian/4337527
# submitted by vinothpandian

#import random, loading the random module (ex. generate random numbers)
import random
#import pygame, set of modules designed for creating games, sys is a module that support us to connect with the python terminal
import pygame, sys
#import many pygame modules used by pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_UP, K_DOWN, K_w, K_s

#initialize the pygame modules
pygame.init()
#frames per second to specify frame rate for the display
fps = pygame.time.Clock()

#define variables like some color variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set the size of the screen and other variables like ball size and paddle size
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2

#set the inital game variables
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

#create the display screen
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
#display hello world as a caption on the top left
pygame.display.set_caption('Hello World')


#function to initialze the ball velocity and position
def ball_init(right):
    global ball_pos, ball_vel  #global variables(it is updating global variables of ball_pos and ball_vel, not creating new variables)
    #initial position of a ball (center)
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    #set ball's random hor and ver velocities
    horz = random.randrange(5, 7)
    vert = random.randrange(3, 5)
    #change the direction of the ball when it bounces off the walls
    if right == False:
        horz = -horz
    ball_vel = [horz, -vert]


#function to initialize variables of the game
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score  # these are floats
    global score1, score2  # these are ints
    #initial position of paddles
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
    #initaial scores
    l_score = 0
    r_score = 0
    #set random direction of inital balls
    if random.randrange(0, 2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#function to draw elements on the screen
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score

    #background is BLACK
    canvas.fill(BLACK)
    #whitelines to draw the court
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],
                     [WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

    #change the position of the paddles (up and down) according to their position and velocity
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[
            1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[
            1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #change position of the ball according to its velocity
    ball_pos[0] += int(
        ball_vel[0])  #change horizontal position based on horizontal velocity
    ball_pos[1] += int(
        ball_vel[1])  #change vertical position based on vertical velocity

    #draw the ball red and draw the paddles green
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(
        canvas, GREEN,
        [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
         [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
         [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
         [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]],
        0)
    pygame.draw.polygon(
        canvas, GREEN,
        [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
         [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
         [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
         [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]],
        0)

    #change the direction of the ball when it hits the top/bottom of the screen or hits the paddles
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(
            ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,
                                  paddle1_pos[1] + HALF_PAD_HEIGHT, 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        #add 1 score for the right if the left paddle miss a ball
        r_score += 1
        #then reset the ball for a new round
        ball_init(True)

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(
            ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,
                                  paddle2_pos[1] + HALF_PAD_HEIGHT, 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        #add 1 score for the left if the right paddle miss the ball
        l_score += 1
        #then reset the ball for a new round
        ball_init(False)

    #Record the score of each side and display it on the screen
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score " + str(l_score), 1, (255, 255, 0))
    canvas.blit(label1, (50, 20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score " + str(r_score), 1, (255, 255, 0))
    canvas.blit(label2, (470, 20))


#function for moving the paddle when the key is pressed
def keydown(event):
    global paddle1_vel, paddle2_vel

    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8


#function for when the key is released, it sets the velocities of the paddles to zero.
def keyup(event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0


init()  #initialize many modules need for pygame modules

#infinite loop until a user quits
while True:
    #draw the window
    draw(window)

    #loop over the following events. If a key is pressed, show keydown event, if it is unpressed, show keyup event, if the window is closed, exist the system.
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    #updates the display
    pygame.display.update()
    #frame rate limited to 60fps
    fps.tick(60)
# https://gist.github.com/vinothpandian/4337527