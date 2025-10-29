import pygame
import sys
import math

pygame.init()

# Window setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirate Cannon Adventure - Waves")

clock = pygame.time.Clock()

# Wave properties
wave_amplitude = 15      # height of waves
wave_length = 200        # distance between peaks
wave_speed = 0.1        # speed of wave movement

t = 0  # time counter

# Game loop
while True:
    dt = clock.tick(60) / 1000
    t += dt  # increase time for animation

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Drawing section ---
    screen.fill((135, 206, 235))  # sky background

    # Generate wave points
    points = []
    for x in range(0, WIDTH + 1, 10):
        y = HEIGHT - 100 + math.sin((x / wave_length) + (t / wave_speed)) * wave_amplitude
        points.append((x, y))

    # Add corners to close the polygon (bottom of the screen)
    points.append((WIDTH, HEIGHT))
    points.append((0, HEIGHT))

    # Draw the wave as a filled polygon
    pygame.draw.polygon(screen, (0, 0, 255), points)

    pygame.display.flip()