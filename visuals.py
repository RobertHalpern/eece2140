import pygame
import sys
import math
import physics   # Physics stays in physics.py
import data_export


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
        self.wave_speed = 0.3  
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

        # Tracer
        self.trail = []
        self.MAX_TRAIL_LENGTH = 300

        self.flight_data = []
        self.time_since_launch = 0.0
        self.last_vx = 0.0  # store constant Vx



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


    def _launch_projectile(self):
        mx, my = pygame.mouse.get_pos()
        cx, cy = self._get_cannon_position()

        dx = mx - cx
        dy = cy - my

        self.vx, self.vy, angle, speed = physics.physics.launch_from_mouse(dx, dy, self.POWER_SCALE)

        # save launch conditions for CSV
        self.launch_angle_deg = math.degrees(angle)
        self.launch_speed = speed
        self.last_vx = self.vx

        self.x = 0
        self.y = 0
        self.projectile_active = True
        self.trail = []
        self.flight_data = []
        self.time_since_launch = 0.0


    def _update_projectile(self, dt):
        # Save before updating
        self.flight_data.append(
            (
                self.time_since_launch,
                self.x,
                self.y,
                self.vx,
                self.vy
            )
        )

        self.time_since_launch += dt

        # Update physics
        self.x, self.y, self.vy = physics.physics.update_step(self.vx, self.vy, self.x, self.y, dt)

        # add trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.MAX_TRAIL_LENGTH:
            self.trail.pop(0)

        # stop if ground hit
        if self.y <= 0:
            self.projectile_active = False
            # Save file
            filename = data_export.save_trajectory_csv(
                self.flight_data,
                self.launch_angle_deg,
                self.launch_speed
            )
            print(f"Saved trajectory CSV: {filename}")



    # Draw Projectile 
    def _draw_projectile(self, screen):
        # physics coords → delta offset
        ox, oy = self._phys_to_screen(self.x, self.y)

        # cannon screen coords
        cx, cy = self._get_cannon_position()

        # projectile position = cannon + physics displacement
        sx = cx + (ox - self._phys_to_screen(0, 0)[0])
        sy = cy + (oy - self._phys_to_screen(0, 0)[1])

        pygame.draw.circle(screen, self.ARC_COLOR, (sx, sy), self.PROJECTILE_RADIUS)



    # Draw Aiming Line When Dragging 
    def _draw_aim_line(self, screen):
        mx, my = pygame.mouse.get_pos()
        cx, cy = self._get_cannon_position()
        pygame.draw.line(screen, self.AIM_LINE_COLOR,
                        (cx, cy),
                        (mx, my), 3)


    def _draw_trail(self, screen):
        # cannon bobbing offset (same as projectile)
        cx, cy = self._get_cannon_position()
        
        # origin of physics 0,0 in screen coords
        ox0, oy0 = self._phys_to_screen(0, 0)

        for tx, ty in self.trail:
            # convert physics → screen
            sx, sy = self._phys_to_screen(tx, ty)

            # align tracer to moving cannon base
            sx = cx + (sx - ox0)
            sy = cy + (sy - oy0)

            pygame.draw.circle(screen, (255, 255, 0), (sx, sy), 3)


    def _get_cannon_position(self):
        # Convert physics x to screen
        x_screen = int(50 * self.X_SCALE)   # ship x position is hardcoded as 50

        # Wave riding motion (same as drawShip)
        y_wave = (
            (self.HEIGHT - self.GROUND_Y_OFFSET)
            + math.sin((x_screen / self.wave_length) + (self.t_wave / self.wave_speed))
            * self.wave_amplitude
        )

        # Ship’s vertical position
        y_ship = y_wave - 12

        # Cannon geometry (same values as drawShip)
        cannonX = x_screen + 5 # I just guessed and checked to align the barrel
        cannonY = y_ship - 10

        return cannonX, cannonY



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

                # Mouse press
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True

                # Release → launch projectile
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.mouse_down:
                        self._launch_projectile()
                    self.mouse_down = False
                    
            screen.fill(self.SKY_BLUE)

            # 2. Waves
            self._draw_waves(screen)

            # 3. Ship floating
            self.drawShip(screen, x_phys=50)

            # 4. Aim line
            if self.mouse_down:
                self._draw_aim_line(screen)

            # 5. Projectile + physics update
            if self.projectile_active:
                self._update_projectile(dt_s)
                self._draw_trail(screen)
                self._draw_projectile(screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
