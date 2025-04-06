import cv2
import turtle
import numpy as np
from matplotlib import pyplot as plt
import time

# Set up Turtle window and color mode
win = turtle.Screen()
win.bgcolor('black')
turtle.colormode(255)

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

# Optional: Uncomment to visualize the thresholded image
# plt.imshow(th3)
# plt.axis('off')
# plt.tight_layout()
# plt.show()

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

# Initialize Turtle
t = turtle.Turtle()
t.color("black")  # Turtle fill color (not used here)
t.shapesize(1)
t.pencolor(255, 153, 51)  # Saffron for outline
t.speed(0)  # Fastest drawing speed
turtle.tracer(0, 0)  # Disable animation for manual updates
t.penup()
t.goto(positions[0])
t.pendown()

# Pause to observe initial setup
time.sleep(3)

# Draw the outline
p = positions[0]
while p:
    p = find_closest(p)
    if p:
        current_pos = np.asarray(t.pos())
        new_pos = np.asarray(p)
        length = np.linalg.norm(new_pos - current_pos)
        if length < CUTOFF_LEN:
            t.goto(p)
            turtle.update()
        else:
            t.penup()
            t.goto(p)
            t.pendown()
        positions.remove(p)
    else:
        p = None

# Write festive greeting
t.penup()
t.goto(0, -HEIGHT/2 - 50)  # Position below image
t.pencolor(255, 255, 255)  # White text
t.write("Happy Ram Navami everyone", align="center", font=("Arial", 16, "normal"))

# Finish
turtle.done()