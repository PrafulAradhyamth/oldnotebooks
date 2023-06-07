import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Bubble Pop Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define bubble properties
bubble_radius = 20
bubble_speed = 3
bubble_spawn_interval = 1000  # in milliseconds

# Initialize variables
score = 0
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
bubbles = []

# Function to create a new bubble
def create_bubble():
    x = random.randint(bubble_radius, window_width - bubble_radius)
    y = window_height + bubble_radius
    color = random.choice([RED, BLUE])
    return {"x": x, "y": y, "color": color}

# Function to draw bubbles on the screen
def draw_bubbles():
    for bubble in bubbles:
        pygame.draw.circle(window, bubble["color"], (bubble["x"], bubble["y"]), bubble_radius)

# Function to update bubble positions
def update_bubbles():
    for bubble in bubbles:
        bubble["y"] -= bubble_speed

# Function to check if bubble is popped
def is_bubble_popped(bubble, mouse_x, mouse_y):
    distance = ((bubble["x"] - mouse_x) ** 2 + (bubble["y"] - mouse_y) ** 2) ** 0.5
    return distance <= bubble_radius

# Main game loop
running = True
last_spawn_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for bubble in bubbles:
                if is_bubble_popped(bubble, mouse_x, mouse_y):
                    bubbles.remove(bubble)
                    score += 1

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= bubble_spawn_interval:
        bubbles.append(create_bubble())
        last_spawn_time = current_time

    window.fill(BLACK)
    draw_bubbles()
    update_bubbles()

    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
