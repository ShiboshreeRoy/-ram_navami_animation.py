import cv2
import turtle
import numpy as np
import random
import time

# Set up Turtle window and color mode
win = turtle.Screen()
win.bgcolor('black')
turtle.colormode(255)
WIDTH = win.window_width()
HEIGHT = win.window_height()

# Function to draw a gradient sky with clamped color values
def draw_sky():
    sky = turtle.Turtle()
    sky.hideturtle()
    sky.speed(0)
    sky.penup()
    for y in range(int(HEIGHT/2), -int(HEIGHT/2), -1):
        r = max(0, min(255, 135 - y//5))
        g = max(0, min(255, 206 - y//5))
        b = max(0, min(255, 235 - y//5))
        color = (r, g, b)
        sky.pencolor(color)
        sky.goto(-WIDTH/2, y)
        sky.pendown()
        sky.goto(WIDTH/2, y)
        sky.penup()

# Function to draw a cloud
def draw_cloud(t, size):
    t.begin_fill()
    for _ in range(5):
        t.circle(size, 60)
        t.left(120)
    t.end_fill()

# Function to create and move clouds
clouds = []
def create_cloud():
    if len(clouds) < 5:
        cloud = turtle.Turtle()
        cloud.hideturtle()
        cloud.color(255, 255, 255)
        cloud.penup()
        cloud.goto(random.uniform(-WIDTH/2, WIDTH/2), random.uniform(HEIGHT/2 - 100, HEIGHT/2))
        cloud.speed(0)
        draw_cloud(cloud, 20)
        clouds.append(cloud)
    win.ontimer(create_cloud, 5000)  # New cloud every 5 seconds

def move_clouds():
    for cloud in clouds:
        cloud.setx(cloud.xcor() + 0.5)
        if cloud.xcor() > WIDTH/2:
            cloud.clear()
            cloud.goto(-WIDTH/2, cloud.ycor())
            draw_cloud(cloud, 20)
    win.ontimer(move_clouds, 50)

# Function to draw a flower
def draw_flower(t, size):
    t.begin_fill()
    for _ in range(5):
        t.forward(size)
        t.right(144)
    t.end_fill()

# Function to create and move falling flowers
flowers = []
def create_flower():
    if len(flowers) < 10:
        flower = turtle.Turtle()
        flower.hideturtle()
        flower.color(random.choice([(255, 182, 193), (255, 255, 224), (221, 160, 221)]))
        flower.penup()
        flower.goto(random.uniform(-WIDTH/2, WIDTH/2), HEIGHT/2 + 50)
        flower.speed(0)
        draw_flower(flower, 10)
        flowers.append(flower)
    win.ontimer(create_flower, 1000)

def move_flowers():
    for flower in flowers[:]:
        flower.sety(flower.ycor() - random.uniform(1, 3))
        if flower.ycor() < -HEIGHT/2 - 50:
            flower.clear()
            flowers.remove(flower)
    win.ontimer(move_flowers, 50)

# Function to create and explode bombs with sparks
bombs = []
def create_bomb():
    if len(bombs) < 3:
        bomb = turtle.Turtle()
        bomb.shape("circle")
        bomb.shapesize(1)
        bomb.color("gray")
        bomb.penup()
        bomb.goto(random.uniform(-WIDTH/2, WIDTH/2), random.uniform(HEIGHT/2, HEIGHT/2 + 100))
        bomb.speed(0)
        bombs.append(bomb)
        win.ontimer(lambda: explode_bomb(bomb), 2000)
    win.ontimer(create_bomb, 3000)

def explode_bomb(bomb):
    if bomb in bombs:
        bomb.color("yellow")
        for _ in range(5):
            bomb.shapesize(bomb.shapesize()[0] + 0.5)
            time.sleep(0.1)
        # Add sparks
        for _ in range(10):
            spark = turtle.Turtle()
            spark.hideturtle()
            spark.speed(0)
            spark.penup()
            spark.goto(bomb.pos())
            spark.pendown()
            spark.pencolor("orange")
            angle = random.uniform(0, 360)
            spark.setheading(angle)
            for i in range(10):
                spark.forward(5)
                spark.pencolor((255, 165 - i*15, 0))  # Fade from orange to dark
        bomb.hideturtle()
        bombs.remove(bomb)

# Function to find the closest point
def find_closest(p):
    if len(positions) > 0:
        nodes = np.array(positions)
        distances = np.sum((nodes - p) ** 2, axis=1)
        i_min = np.argmin(distances)
        return positions[i_min]
    else:
        return None

# Function to process image and find edges
def outline(src_image):
    blurred = cv2.GaussianBlur(src_image, (7, 7), 0)
    th3 = cv2.adaptiveThreshold(blurred, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                thresholdType=cv2.THRESH_BINARY, blockSize=9, C=2)
    return th3

# Load and process the image
image = 'Jai-Shree-Ram-thumb.png'
im = cv2.imread(image, 0)
th3 = outline(im)

# Get image dimensions and set cutoff length
WIDTH = im.shape[1]
HEIGHT = im.shape[0]
print(f"Image dimensions: {WIDTH}x{HEIGHT}")
CUTOFF_LEN = ((WIDTH + HEIGHT) / 2) / 60

# Find edge coordinates and adjust to center origin
iH, iW = np.where(th3 == [0])
iW = iW - WIDTH / 2
iH = -1 * (iH - HEIGHT / 2)
positions = [list(iwh) for iwh in zip(iW, iH)]

# Initialize main Turtle for drawing outline with glow effect
t = turtle.Turtle()
t.hideturtle()
t.pencolor(255, 153, 51)  # Saffron for outline
t.speed(0)
t.penup()
t.goto(positions[0])
t.pendown()

# Initialize glow Turtle
glow = turtle.Turtle()
glow.hideturtle()
glow.pencolor(255, 204, 153)  # Lighter saffron for glow
glow.speed(0)
glow.penup()
glow.goto(positions[0])
glow.pendown()

# Draw sky gradient
draw_sky()

# Start effects
create_cloud()
move_clouds()
create_flower()
move_flowers()
create_bomb()

# Main drawing loop with glow
p = positions[0]
while p:
    p = find_closest(p)
    if p:
        current_pos = np.asarray(t.pos())
        new_pos = np.asarray(p)
        length = np.linalg.norm(new_pos - current_pos)
        if length < CUTOFF_LEN:
            t.goto(p)
            glow.goto(p[0] + 2, p[1] + 2)  # Slightly offset for glow
        else:
            t.penup()
            glow.penup()
            t.goto(p)
            glow.goto(p[0] + 2, p[1] + 2)
            t.pendown()
            glow.pendown()
        positions.remove(p)
    else:
        p = None

# Write festive greeting
t.penup()
t.goto(0, -HEIGHT/2 - 50)
t.pencolor(255, 255, 255)
t.write("Happy Ram Navami everyone", align="center", font=("Arial", 16, "normal"))

# Optimize performance
turtle.tracer(0, 0)
turtle.update()

# Keep the window open
turtle.done()