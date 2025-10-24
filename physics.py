#Math

import math

def PhysicsCalc(Velocity, Angle):
    # Convert angle from degrees to radians
    Angle_rad = math.radians(Angle)
    
    # Calculate horizontal and vertical components of velocity
    Vx = Velocity * math.cos(Angle_rad)
    Vy = Velocity * math.sin(Angle_rad)
    
    
   