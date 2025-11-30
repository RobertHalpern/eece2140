import pygame
import sys
import math
import physics   # Physics stays in physics.py

class VisualSimulator:
    
    def __init__(self, width=1000, height=600, max_x=500.0, max_y=300.0, ground_offset=100):
        #  Configuration Constants 
        self.WIDTH = width
        self.HEIGHT = height
        self.GROUND_Y_OFFSET = ground_offset
        
        #  Physics to Screen Scaling 
        self.MAX_PHYSICS_X = max_x 
        self.MAX_PHYSICS_Y = max_y 
        self.X_SCALE = self.WIDTH / self.MAX_PHYSICS_X 
        self.Y_SCALE = (self.HEIGHT - self.GROUND_Y_OFFSET) / self.MAX_PHYSICS_Y 

        #  Drawing Colors 
        self.SKY_BLUE = (135, 206, 235)
        self.SEA_BLUE = (0, 0, 255)
        self.ARC_COLOR = (255, 0, 0)
        self.AIM_LINE_COLOR = (0, 0, 0)
        self.ARC_THICKNESS = 3
        self.PROJECTILE_RADIUS = 8
        
        #  Wave Animation Properties 
        self.wave_amplitude = 15      
        self.wave_length = 200        
        self.wave_speed = 0.1        
        self.t_wave = 0  

        #  Launch Origin Location (pixels) 
        self.launch_x_px = 80  
        self.launch_y_px = self.HEIGHT - self.GROUND_Y_OFFSET - 10

        #  Projectile Motion State 
        self.projectile_active = False
        self.mouse_down = False
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

        # Launch Power Scale (tweak feel)
        self.POWER_SCALE = 0.055  


    # Convert from Physics Coordinates (meters) to Screen Pixels
    def _phys_to_screen(self, x_phys, y_phys):
        screen_x = int(x_phys * self.X_SCALE)
        screen_y = int((self.HEIGHT - self.GROUND_Y_OFFSET) - (y_phys * self.Y_SCALE))
        return screen_x, screen_y


    # Draw Ocean Animation 
    def _draw_waves(self, screen):
        points = []
        for x in range(0, self.WIDTH + 1, 10):
            y = (self.HEIGHT - self.GROUND_Y_OFFSET 
                + math.sin((x / self.wave_length) + (self.t_wave / self.wave_speed)) * self.wave_amplitude)
            points.append((x, y))
        points.append((self.WIDTH, self.HEIGHT))
        points.append((0, self.HEIGHT))
        pygame.draw.polygon(screen, self.SEA_BLUE, points)


    # Mouse Launch Logic (calls physics class externally) 
    def _launch_projectile(self):
        mx, my = pygame.mouse.get_pos()
        dx = mx - self.launch_x_px
        dy = self.launch_y_px - my  # invert due to Pygame coords

        self.vx, self.vy = physics.physics.launch_from_mouse(dx, dy, self.POWER_SCALE)

        # Reset physics position
        self.x = 0
        self.y = 0
        self.projectile_active = True


    # Update Projectile Using Physics Class
    def _update_projectile(self, dt):
        self.x, self.y, self.vy = physics.physics.update_step(self.vx, self.vy, self.x, self.y, dt)

        # Stop if projectile hits ground
        if self.y <= 0:
            self.projectile_active = False


    # Draw Projectile 
    def _draw_projectile(self, screen):
        sx, sy = self._phys_to_screen(self.x, self.y)
        pygame.draw.circle(screen, self.ARC_COLOR, (sx, sy), self.PROJECTILE_RADIUS)


    # Draw Aiming Line When Dragging 
    def _draw_aim_line(self, screen):
        mx, my = pygame.mouse.get_pos()
        pygame.draw.line(screen, self.AIM_LINE_COLOR,
                         (self.launch_x_px, self.launch_y_px),
                         (mx, my), 3)
        
    def drawShip(self, screen, x_phys):
        # Convert physics x to screen x
        x_screen = int(x_phys * self.X_SCALE)

        # Wave riding motion
        y_wave = (
            (self.HEIGHT - self.GROUND_Y_OFFSET)
            + math.sin((x_screen / self.wave_length) + (self.t_wave / self.wave_speed))
              * self.wave_amplitude
        )

        # Offset to sit ship on wave
        y_ship = y_wave - 12

        #  Draw Ship Hull 
        hull_color = (139, 69, 19)
        hull_width = 50
        hull_height = 20

        pygame.draw.polygon(screen, hull_color, [
            (x_screen - hull_width,       y_ship),
            (x_screen + hull_width,       y_ship),
            (x_screen + hull_width - 15,  y_ship + hull_height),
            (x_screen - hull_width + 15,  y_ship + hull_height)
        ])

        #  Mast 
        pygame.draw.line(screen, (60, 60, 60),
                         (x_screen, y_ship),
                         (x_screen, y_ship - 50), 5)

        #  Sail 
        pygame.draw.polygon(screen, (255, 255, 255), [
            (x_screen,       y_ship - 50),
            (x_screen + 45,  y_ship - 25),
            (x_screen,       y_ship - 25)
        ])

        # Cannon 
        cannonX = x_screen - 20
        cannonY = y_ship - 10

        pygame.draw.rect(screen, (40, 40, 40), (cannonX, cannonY, 30, 8))
        pygame.draw.circle(screen, (70, 70, 70), (cannonX + 5, cannonY + 10), 6)


    #  MAIN LOOP
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Projectile Motion Simulator")
        clock = pygame.time.Clock()

        running = True
        while running:
            dt_ms = clock.tick(60)
            dt_s = dt_ms / 1000.0
            self.t_wave += dt_s

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            screen.fill(self.SKY_BLUE)

            # 2. Waves
            self._draw_waves(screen)

            # 3. Ship floating on waves
            self.drawShip(screen, x_phys=50)

            pygame.display.flip()

        pygame.quit()
        sys.exit()