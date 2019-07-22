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
score_font = pygame.font.SysFont('Arial', int(GAME_SIZE * 0.065), True) # font line, but not used here ==> main game loop
pygame.display.set_caption('SNAKE!')

class Game_Object(): # the third class made body of snake and apple
    def __init__(self, xcor, ycor, color): # self is python specific
        self.xcor = xcor
        self.ycor = ycor # these lines are essentially properties for Game_Object
        self.color = color
    def show(self):
        pygame.draw.rect(game_display, self.color, pygame.Rect(self.xcor, self.ycor, BLOCK_SIZE, BLOCK_SIZE)) # this line is the God Line and anytime we show something this gets used

class Snake():
    def __init__(self, xcor, ycor): #constructor ---called whenever instantaite class
        self.is_alive = True
        self.score = 0
        self.direction = "RIGHT" # can use "" or ''
        self.body = [Game_Object(xcor, ycor, SNAKE_COLOR), 
                     Game_Object(xcor - BLOCK_SIZE, ycor, SNAKE_COLOR),
                     Game_Object(xcor - BLOCK_SIZE * 2, ycor, SNAKE_COLOR)]
        self.previous_last_tail = self.body[len(self.body) - 1]
    def grow(self):
        self.body.append(self.previous_last_tail)
    def show(self): # called whenever you call snake.show
        for body_part in self.body:
            body_part.show()
    def move(self):
        head_xcor = self.body[0].xcor # the array part of this grabs index 0 on line 30 self.body
        head_ycor = self.body[0].ycor
        if self.direction == "RIGHT":
            head_xcor = head_xcor + BLOCK_SIZE
        elif self.direction == "LEFT":
            head_xcor = head_xcor - BLOCK_SIZE 
        elif self.direction == "UP":
            head_ycor = head_ycor - BLOCK_SIZE 
        elif self.direction == "DOWN":
            head_ycor = head_ycor + BLOCK_SIZE

        self.body.insert(0, Game_Object(head_xcor, head_ycor, SNAKE_COLOR))
        self.previous_last_tail = self.body.pop() # saves the last position of the tail
    def has_collided_with_wall(self):#these names need to be real specific
        head = self.body[0]
        if head.xcor < 0 or head.ycor < 0 or head.xcor + BLOCK_SIZE > GAME_SIZE or head.ycor + BLOCK_SIZE > GAME_SIZE:
            return True
        return False
    def has_eaten_apple(self, apple_in_question):
        head = self.body[0]
        if head.xcor == apple_in_question.body.xcor and head.ycor == apple_in_question.body.ycor:
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
            snake.grow()
            apple = Apple() #instansiation of class here, creates new apple in random generated area from constructor
            snake.score += 1
            
    game_display.fill(BACKGROUND_COLOR) # fills the screen with dark green, do not put after snake.show() or else it will not show up. defined at top
    snake.show() # displays to screen
    apple.show()

    score_text = score_font.render(str(snake.score), False, (60, 100, 255))
    game_display.blit(score_text, (0,0)) # puts the score on the grid in top left at 0,0

    pygame.display.flip()
    clock.tick(10) #slow down to make it slow

pygame.quit()