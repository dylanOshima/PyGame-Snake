import random

WIDTH = 800
HEIGHT = 800

global timeElapsed
timeElapsed = 1

###### Initalize Snake
snakeHead = Actor('snake_head', pos=(WIDTH/2, HEIGHT/2))   # Initializes an actor named Snake
snakeHead.dir = 'up'   # Sets the default direction of the snake to 'up'
snakeHead.alive = True
snake = [snakeHead]

# generate the rest of the snake's body
for i in range(1, 5):
    snakeBody = Actor('snake_body', pos=snake[i-1].midbottom)
    snake.append(snakeBody)

###### Initalize Points
def newPointPos():
    return (random.randint(20, WIDTH-20), random.randint(20, HEIGHT-20))

point = Actor('point', center=newPointPos())

def updateSnakeHead():
    displacement = images.snake_body.get_width()
    prevPos = snake[0].pos
    if(snake[0].dir is 'up'):
        snake[0].y -= displacement
    elif(snake[0].dir is 'down'):
        snake[0].y += displacement
    elif(snake[0].dir is 'left'):
        snake[0].x -= displacement
    elif(snake[0].dir is 'right'):
        snake[0].x += displacement
    
    collision = snake[0].collidelist(snake[1:])
    if snake[0].alive and (collision >= 0 or snake[0].y not in range(0,HEIGHT) or snake[0].x not in range(0,WIDTH)):
        snake[0].alive = False
    
    return prevPos
    
def updateSnake():
    #Loops through the rest of the body parts
    prevPos = updateSnakeHead()
    for i in range(1, len(snake)):
        tempPos = snake[i].pos
        snake[i].pos = prevPos
        prevPos = tempPos
    
def drawSnake():
    for i in range(len(snake)-1, -1, -1):
        snake[i].draw()

# Draws onto the screen
def draw():
    screen.clear()
    screen.fill((255, 255, 255))
    point.draw()
    drawSnake()
    screen.draw.text(
        "SCORE: " + str(len(snake)-5),
        color='black',
        midtop=(WIDTH // 2, 10),
        fontsize=70
    )
    if(not snake[0].alive):
        screen.draw.text(
            "GAME OVER",
            color='red',
            midbottom=(WIDTH // 2, HEIGHT // 2),
            fontsize=70,
            shadow=(1, 1)
        )

def update(dt):
    global timeElapsed
    
    if snake[0].alive and timeElapsed>0.05:
        if snake[0].collidepoint(point.pos):
            snake.append(Actor('snake_body', pos=snake[-1].pos))
            point.pos = newPointPos()
        
        updateSnake()
        timeElapsed = 0

    timeElapsed += dt

def on_key_down(key):
    if(key is keys.LEFT):
        snake[0].dir = 'left'
    elif(key is keys.RIGHT):
        snake[0].dir = 'right'
    elif(key is keys.UP):
        snake[0].dir = 'up'
    elif(key is keys.DOWN):
        snake[0].dir = 'down'