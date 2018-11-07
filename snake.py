import random

WIDTH = 800
HEIGHT = 800

###### Initalize Snake:
snakeHead = Actor('snake_head', pos=(WIDTH/2, HEIGHT/2))   # Initializes an actor named Snake in the middle of the screen
snakeHead.dir = 'up'   # Sets the default direction of the snake to 'up'
snakeHead.alive = True
snake = [snakeHead]

# generate the rest of the snake's body
for i in range(1, 5):
    snakeBody = Actor('snake_body', pos=(snake[i-1].x,snake[i-1].y+images.snake_body.get_width()))
    print("x: ",snakeBody.x,"y: ", snakeBody.y)
    snake.append(snakeBody)

displacement = images.snake_body.get_width() # Defines how much a snake should move 

###### Initalize Points:

# Generates a new position for the Point object
def newPointPos():
    return (random.randint(20, WIDTH-20), random.randint(20, HEIGHT-20))

point = Actor('point', center=newPointPos())

###### Game Code:
def drawSnake():
    # Loops through the snake body backwards
    for i in range(len(snake)-1, -1, -1):
        snake[i].draw()

# Draws onto the screen
def draw():
    screen.clear() # Clears the screen of any previous images
    screen.fill((255, 255, 255)) # Draws the background
    point.draw() # Creates a point
    drawSnake() # Updates the snake's location
    
    ## Creates the score section
    screen.draw.text(
        "SCORE: " + str(len(snake)-5),
        color='black',
        midtop=(WIDTH // 2, 10),
        fontsize=70
    )
    
    ## Checks if the snake is alive, if it isn't displays game over
    if(not snake[0].alive):
        screen.draw.text(
            "GAME OVER",
            color='red',
            midbottom=(WIDTH // 2, HEIGHT // 2),
            fontsize=70,
            shadow=(1, 1)
        )

# Calculates the change from one point and the next
def calcChangeOfPos(pos1, pos2):
    x_pos = (pos2[0] - pos1[0])
    y_pos = (pos2[1] - pos1[1])
    return (x_pos, y_pos)
    
# Updates the position of the snake depending on the set direction
def updateSnakeHead():
    prevPos = snake[0].pos
    if(snake[0].dir is 'up'):
        snake[0].y -= displacement
    elif(snake[0].dir is 'down'):
        snake[0].y += displacement
    elif(snake[0].dir is 'left'):
        snake[0].x -= displacement
    elif(snake[0].dir is 'right'):
        snake[0].x += displacement

    # Checks if the new position of the snake collides with anything
    collision = snake[0].collidelist(snake[1:])
    if snake[0].alive and (collision >= 0 or snake[0].y not in range(0,HEIGHT) or snake[0].x not in range(0,WIDTH)):
        snake[0].alive = False

    print(calcChangeOfPos(prevPos, snake[0].pos))
    return prevPos

# Updates the rest of the body parts based on the pos of the previous part. 
# Starting with the snakehead.
def updateSnake():
    #Loops through the rest of the snake's body
    prevPos = updateSnakeHead()
    for i in range(1, len(snake)):
        tempPos = snake[i].pos
        snake[i].pos = prevPos
        prevPos = tempPos

def update(dt):
    if snake[0].alive:# and timeElapsed>0.05:
        # Checks if the snake has collided with a point.
        if snake[0].collidepoint(point.pos):
            snake.append(Actor('snake_body', pos=snake[-1].pos))
            point.pos = newPointPos()
        updateSnake()

def on_key_down(key):
    if(key is keys.LEFT):
        snake[0].dir = 'left'
    elif(key is keys.RIGHT):
        snake[0].dir = 'right'
    elif(key is keys.UP):
        snake[0].dir = 'up'
    elif(key is keys.DOWN):
        snake[0].dir = 'down'