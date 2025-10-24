import physics
import visuals # currently no visuals.py so won't do anything

# Try to follow this signature if possible. It's good to have a main file within each of your files
# so you can call other helpers from that (i.e runPhysicsCalc should call helpers)

def run_game(initial_speed, initial_angle):
    # Delegate to physics.py
    # phyics has constants declared already for ground level and gravity.
    arc = physics.physics_calc(initial_speed, initial_angle)

    # Delegate to visuals.py
    visuals.runVisuals(arc)


def main():
    print("Projectile Motion Simulator")

    # Get user inputs
    try:
        initial_speed = float(input("Enter initial speed (m/s): "))
        initial_angle = float(input("Enter launch angle (degrees): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    # Run the main simulation
    run_game(initial_speed, initial_angle)


if __name__ == "__main__":
    main()
