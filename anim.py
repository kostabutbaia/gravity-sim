import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import numpy as np

from Verlet import System
from Object import *
from Trail import *

NAME = 'Leapfrog4'
TRAIL_LENGTH = 70

def create_anim_gif(name: str, system: System) -> None:
    fig = plt.figure()
    plt.xlim(-2, 2)
    plt.ylim(-1, 3)
    plt.grid()
    plt.gca().set_aspect('equal')

    _, frames = system.get_frames()
    l, = plt.plot([], [], 'o')

    trail_plots = []
    trails: list[Trail] = []
    for _ in range(len(objects)):
        p, = plt.plot([], [])
        trails.append(Trail(TRAIL_LENGTH))
        trail_plots.append(p)
    
    writer = PillowWriter(fps=15)
    with writer.saving(fig, f'solutions/{name}.gif', 100):
        for k, frame in enumerate(frames):
            x_points, y_points = frame
            l.set_data(x_points, y_points)
            # plt.title(f"energy: {round(energies[k], 5)}", loc = 'left')
            for i in range(len(frame)):
                x_trail, y_trail = trails[i].update_trail(x_points[i], y_points[i])
                trail_plots[i].set_data(x_trail, y_trail)
            
            writer.grab_frame()


if __name__ == '__main__':
    M1 = 1
    M2 = 1

    objects = [
        Object(2, np.array([0, 0], dtype='float64'), np.array([0, 0], dtype='float64')),
        Object(1, np.array([1, 0], dtype='float64'), np.array([0, 1], dtype='float64'))
    ]
    sys = System(objects, 10, 0.02, True)
    create_anim_gif(NAME, sys)