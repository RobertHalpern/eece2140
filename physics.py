import math

class physics:
    GROUND = 0
    GRAVITY = 9.81
    
    @staticmethod
    def physics_calc(Velocity, Angle):
        """Calculates initial velocities and returns the list of positions for the arc."""
        # Convert angle from degrees to radians
        Angle_rad = math.radians(Angle)
        
        # Calculate horizontal and vertical components of velocity
        Vx = Velocity * math.cos(Angle_rad)
        Vy = Velocity * math.sin(Angle_rad)

        # Runs position calculation and RETURNS the list of positions
        return physics.position_calc(Vx, Vy)
        
    @staticmethod
    def position_calc(Vx, Vy):
        """
        Calculates and returns a list of (x, y, t) tuples sampled every dt
        from t=0 until the projectile lands (y == GROUND).
        """
        # set inital conditions
        initial_time = 0
        dt = .1
        start_y = 0
        start_x = 0
        positions = []
        t = initial_time 
        
        # Calculate positions until the projectile hits the ground
        while True:
            # calculate new positions
            x = start_x + Vx * t
            y = start_y + Vy * t - 0.5 * physics.GRAVITY * t**2
            
            # If the projectile is at or below ground level
            if y < physics.GROUND and len(positions) > 0:
                # Approximate the landing point at y=0
                last_t = t - dt
                x_final = start_x + Vx * last_t
                
                # Append the final ground hit point (x, 0, t)
                positions.append((round(x_final, 2), physics.GROUND, round(t, 2)))
                break
            elif y < physics.GROUND and len(positions) == 0:
                 # Case where the calculation immediately starts below ground (e.g., negative angle)
                 break

            # round for display/debugging accuracy
            x = round(x, 2)
            y = round(y, 2)
            t = round(t, 2)

            # append new position to list
            positions.append((x, y, t))
            
            # increment time
            t += dt

        return positions