import pygame
import sys

# Initialize pygame
pygame.init()

# Create a window (width=800, height=600)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Test Window")

# Set a color (RGB)
BLUE = (0, 120, 255)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with blue
    screen.fill(BLUE)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
