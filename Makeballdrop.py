## Generates sequential images of a bouncing ball

import numpy as np
import matplotlib.pyplot as plt
import os

# Parameters
g = 9.8  # acceleration due to gravity (m/s^2)
e = 0.9  # coefficient of restitution (bounciness)
dt = 0.02  # time step (s)
radius = 1  # radius of the ball
initial_height = 100  # initial height (m)
output_dir = 'D:\\Workplace\\projects\\bouncing_ball_frames1\\'  # Directory to save frames

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Initialize variables
y = initial_height
v = 0
t = 0
frame_number = 0

# Function to save the current frame
def save_frame(y, frame_number):
    fig, ax = plt.subplots()
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, initial_height + 5)
    circle = plt.Circle((0, y), radius, color='blue')
    ax.add_patch(circle)
    ax.set_aspect('equal', 'box')
    plt.title(f'Time: {t:.2f} s')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.grid(True)
    filename = os.path.join(output_dir, f'frame_{frame_number:04d}.jpeg')
    plt.savefig(filename)
    plt.close()
    print(f'Saved frame {frame_number}')

# Simulation loop
while t < 5:  # simulate for 5 seconds
    # Update position and velocity
    v = v - g * dt
    y = y + v * dt

    # Check for collision with the ground
    if y <= radius:
        y = radius
        v = -v * e

    # Save the current frame
    save_frame(y, frame_number)
    frame_number += 1
    t += dt

print(f'Simulation completed. Saved {frame_number} frames.')
