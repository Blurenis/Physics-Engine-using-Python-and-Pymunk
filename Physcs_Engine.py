import pygame
import pymunk
import random
import numpy as np

# Initialization of Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Setting up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Engine Simulation with Walls")

# Initializing Pymunk
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity force downwards

# Function to create a ball with random size and color
def create_ball(x, y):
    radius = np.random.normal(8, 3)  # Random size
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.8  # Elasticity of the ball
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
    space.add(body, shape)
    return shape, color, radius  # Return shape, color, and radius

# Function to create walls
def create_walls():
    walls = []
    # Left wall
    walls.append(pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 1))
    # Right wall
    walls.append(pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 1))
    # Top wall
    walls.append(pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), 1))
    # Bottom wall
    walls.append(pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 1))
    
    for wall in walls:
        wall.elasticity = 0.8  # Elasticity of the walls
        space.add(wall)

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True
    balls = []
    
    create_walls()  # Create the walls

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle ball creation when the left mouse button is held down
        if pygame.mouse.get_pressed()[0]:  # If the left button is pressed
            x, y = pygame.mouse.get_pos()  # Get mouse position
            balls.append(create_ball(x, y))  # Create a new ball

        # Update physics
        space.step(1 / FPS)

        # Draw everything
        screen.fill((0, 0, 0))  # Black background
        for ball, color, radius in balls:
            pos = ball.body.position
            # Draw the colored ball
            pygame.draw.circle(screen, color, (int(pos.x), int(pos.y)), radius)

        # Display the number of balls at the top center
        font = pygame.font.Font(None, 36)
        text = font.render(f'Number of Balls: {len(balls)}', True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(WIDTH // 2, 20))  # Centered at the top
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
