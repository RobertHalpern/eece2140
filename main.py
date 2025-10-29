import physics
import visuals 
# Note: You can call methods directly from the imported class/module: 
# physics.physics_calc() and visuals.runVisuals()

def run_game(initial_speed, initial_angle):
    # Delegate to physics.py
    # The result is the arc (list of positions)
    arc = physics.physics.physics_calc(initial_speed, initial_angle)

    # Delegate to visuals.py
    simulator = visuals.VisualSimulator()
    simulator.run(arc)


def main():
    print("Projectile Motion Simulator")

    # Get user inputs
    try:
        initial_speed = float(input("Enter initial speed (m/s) [e.g., 80]: "))
        initial_angle = float(input("Enter launch angle (degrees) [e.g., 45]: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    # Run the main simulation
    run_game(initial_speed, initial_angle)


if __name__ == "__main__":
    main()