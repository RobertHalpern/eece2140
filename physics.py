import math

class physics:
    GRAVITY = 9.81
    GRAVITY_SCALE = 7.0 

    @staticmethod
    def launch_from_mouse(dx, dy, power_scale):
        angle = math.atan2(dy, dx)
        power = math.sqrt(dx*dx + dy*dy) * 8
        speed = power * power_scale

        Vx = speed * math.cos(angle)
        Vy = speed * math.sin(angle)

        return Vx, Vy, angle, speed


    @staticmethod
    def update_step(Vx, Vy, x, y, dt):
        """
        Compute new position and velocity for the next time step.
        Returns updated (x, y, Vy).
        """
        # Update position
        x += Vx * dt
        y += Vy * dt

        # Gravity (scaled)
        Vy -= physics.GRAVITY * physics.GRAVITY_SCALE * dt

        # Return updated state
        return x, y, Vy
