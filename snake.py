# Ctrl + Shift + P, then select interpreter
# Choose an interpreter that works
import pygame
import random

# Game Settings
GAME_SIZE = 400
BLOCK_SIZE = GAME_SIZE / 40 # make smaller to slow
SNAKE_COLOR = 100, 95, 255
APPLE_COLOR = (205, 0, 55)
BACKGROUND_COLOR = (0, 55, 55) # dark green, called below

pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((GAME_SIZE, GAME_SIZE))
pygame.display.set_caption('SNAKE!')

class Game_Object(): # the third class made body of snake and apple
    def __init__(self, xcor, ycor, color): # self is python specific
        self.xcor = xcor
        self.ycor = ycor # these lines are essentially properties for Game_Object
        self.color = color
    def show(self):
        pygame.draw.rect(game_display, self.color, pygame.Rect(self.xcor, self.ycor, BLOCK_SIZE, BLOCK_SIZE))

class Snake():
    def __init__(self, xcor, ycor): #constructor ---called whenever instantaite class
        self.is_alive = True
        self.direction = "RIGHT" # can use "" or ''
        self.body = [(xcor, ycor), 
                     (xcor - BLOCK_SIZE, ycor),
                     (xcor - BLOCK_SIZE * 2, ycor)]
    def show(self): # called whenever you call snake.show
        for body_part in self.body:
            pygame.draw.rect(game_display, (SNAKE_COLOR), pygame.Rect(body_part[0], body_part[1], BLOCK_SIZE, BLOCK_SIZE))
    def move(self):
        head_xcor = self.body[0][0]
        head_ycor = self.body[0][1]
        if self.direction == "RIGHT":
            head_xcor = head_xcor + BLOCK_SIZE
        elif self.direction == "LEFT":
            head_xcor = head_xcor - BLOCK_SIZE 
        elif self.direction == "UP":
            head_ycor = head_ycor - BLOCK_SIZE 
        elif self.direction == "DOWN":
            head_ycor = head_ycor + BLOCK_SIZE  

        self.body.insert(0, (head_xcor, head_ycor))
        self.body.pop()
    def has_collided_with_wall(self):#these names need to be real specific
        head = self.body[0]
        if head[0] < 0 or head[1] < 0 or head[0] + BLOCK_SIZE > GAME_SIZE or head[1] + BLOCK_SIZE > GAME_SIZE:
            return True
        return False
    def has_eaten_apple(self, apple_in_question):
        head = self.body[0]
        if head[0] == apple_in_question.body.xcor and head[1] == apple_in_question.body.ycor:
            return True
        return False

class Apple():
    def __init__(self): #constructor for apple every time generated
        xcor = random.randrange(0, GAME_SIZE / BLOCK_SIZE) * BLOCK_SIZE
        ycor = random.randrange(0, GAME_SIZE / BLOCK_SIZE) * BLOCK_SIZE
        self.body = Game_Object(xcor, ycor, APPLE_COLOR)
    def show(self):
        self.body.show()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snake.is_alive = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                snake.direction = "RIGHT"
            elif event.key == pygame.K_UP:
                    snake.direction = "UP"
            elif event.key == pygame.K_DOWN:
                    snake.direction = "DOWN"

snake = Snake(BLOCK_SIZE * 5, BLOCK_SIZE * 5) #where snake starts
apple = Apple()

# Main Game Loop
while snake.is_alive:

    handle_events() # when refactored moved event handling into its own method which we call right here

    game_display.blit(game_display, (0,0))

    snake.move()
    if snake.has_collided_with_wall():
            snake.is_alive = False # kills snake if hits wall

    if snake.has_eaten_apple(apple):
            apple = Apple() #instansiation of class here, creates new apple in random generated area from constructor
            
    game_display.fill(BACKGROUND_COLOR) # fills the screen with dark green, do not put after snake.show() or else it will not show up. defined at top
    snake.show() # displays to screen
    apple.show()

    pygame.display.flip()
    clock.tick(10) #slow down to make it slow

pygame.quit()