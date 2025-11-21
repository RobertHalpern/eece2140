import pygame
import sys
import math

class VisualSimulator:
    
    def __init__(self, width=1000, height=600, max_x=500.0, max_y=300.0, ground_offset=100):
        # --- Configuration Constants ---
        self.WIDTH = width
        self.HEIGHT = height
        self.GROUND_Y_OFFSET = ground_offset
        self.MAX_PHYSICS_X = max_x 
        self.MAX_PHYSICS_Y = max_y 
        
        # --- Scaling Factors ---
        self.X_SCALE = self.WIDTH / self.MAX_PHYSICS_X 
        self.Y_SCALE = (self.HEIGHT - self.GROUND_Y_OFFSET) / self.MAX_PHYSICS_Y 

        # --- Color and Drawing Properties ---
        self.SKY_BLUE = (135, 206, 235)
        self.SEA_BLUE = (0, 0, 255)
        self.ARC_COLOR = (255, 0, 0)
        self.ARC_THICKNESS = 3
        
        # --- Wave properties ---
        self.wave_amplitude = 15      
        self.wave_length = 200        
        self.wave_speed = 0.1        
        self.t_wave = 0  # Time counter for wave animation

    # --- Helper Methods ---

    def _physics_to_screen(self, x_phys, y_phys):
        """
        Converts physics coordinates (x_phys, y_phys) in meters
        to screen coordinates (screen_x, screen_y) in pixels.
        Note the use of 'self' to access class variables.
        """
        # Scale x
        screen_x = int(x_phys * self.X_SCALE)
        
        # Scale y: Pygame's y-axis increases *downwards*.
        screen_y = int((self.HEIGHT - self.GROUND_Y_OFFSET) - (y_phys * self.Y_SCALE))
        
        return screen_x, screen_y

    def _draw_waves(self, screen):
        """Draws the moving wave polygon."""
        points = []
        
        # Generate wave points
        for x in range(0, self.WIDTH + 1, 10):
            # Apply the sine wave to the ground level
            y = self.HEIGHT - self.GROUND_Y_OFFSET + math.sin((x / self.wave_length) + (self.t_wave / self.wave_speed)) * self.wave_amplitude
            points.append((x, y))

        # Add corners to close the polygon
        points.append((self.WIDTH, self.HEIGHT))
        points.append((0, self.HEIGHT))

        # Draw the wave as a filled polygon
        pygame.draw.polygon(screen, self.SEA_BLUE, points)

    def _draw_trajectory(self, screen, arc):
        """
        Draws the projectile's path arc on the screen.
        """
        if len(arc) < 2:
            return 

        # Convert all physics points to screen points
        screen_points = []
        for x, y, t in arc:
            # Only draw points that are within the screen boundary
            if x * self.X_SCALE <= self.WIDTH: 
                 screen_points.append(self._physics_to_screen(x, y))

        # Draw the line connecting all the screen points
        if len(screen_points) >= 2:
            pygame.draw.lines(screen, self.ARC_COLOR, False, screen_points, self.ARC_THICKNESS) 





    # Main Run Method --- we're going to call this from main.py

    def run(self, arc):
 
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Projectile Motion Simulator")
        clock = pygame.time.Clock()

        running = True
        while running:
            # dt_s is delta time in seconds
            dt_ms = clock.tick(60) # Limits frame rate to 60 FPS
            dt_s = dt_ms / 1000.0
            self.t_wave += dt_s # Update wave animation time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            # --- Drawing section ---
            screen.fill(self.SKY_BLUE)  # sky background

            # 1. Draw the trajectory
            self._draw_trajectory(screen, arc)
            
            # 2. Draw the wave/ground level
            self._draw_waves(screen)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# --- Testing block (for direct execution) ---
if __name__ == '__main__':
    print("Running visuals.py class directly with dummy data. Run main.py instead.")
    
    # Example usage:
    simulator = VisualSimulator()
    
    # Dummy arc data
    test_arc = [
        (0, 0, 0), 
        (100, 100, 1), 
        (200, 150, 2), 
        (300, 100, 3), 
        (400, 0, 4)
    ]
    simulator.run(test_arc)