#Math

import math

class physics:
    GROUND = 0
    GRAVITY = 9.81

    def physics_calc(Velocity, Angle):
        # Convert angle from degrees to radians
        Angle_rad = math.radians(Angle)
        
        # Calculate horizontal and vertical components of velocity
        Vx = Velocity * math.cos(Angle_rad)
        Vy = Velocity * math.sin(Angle_rad)

        #Runs position calculation to get list of positions and times
        physics.position_calc(Vx, Vy)
        
        
    def position_calc(Vx, Vy):
        #Return a list of (x, y, t) tuples sampled every dt from t=0 until the
        #projectile lands (y == GROUND). The final sample is linearly interpolated
        #so y equals GROUND exactly."
        
        #set inital conditions
        initial_time = 0
        dt = 1
        start_y = 0
        start_x = 0
        positions = []
        y = start_y  # Initialize y to start_y
        x = start_x  # Initialize x to start_x
        t = initial_time  # Initialize t

        #if statement to control how many positions are calculated
        while y >= physics.GROUND:
            #calculate new positions
            x = start_x + Vx * initial_time
            y = start_y + Vy * initial_time - 0.5 * physics.GRAVITY * initial_time**2
            
            #append new position to list
            positions.append((x, y, initial_time))
            
            #increment time
            initial_time += dt

            
        print(positions)

#Test call to physics_calc
physics.physics_calc(50,45)


