import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import numpy as np

from System import *
from Object import *
from Trail import *

NAME = 'not_follow_2'
TRAIL_LENGTH = 10

def create_anim_gif(name: str, system: System) -> None:
    fig = plt.figure()
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
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
        for frame in frames:
            x_points, y_points = frame
            l.set_data(x_points, y_points)
            for i in range(len(frame)):
                x_trail, y_trail = trails[i].update_trail(x_points[i], y_points[i])
                trail_plots[i].set_data(x_trail, y_trail)
            
            writer.grab_frame()


if __name__ == '__main__':
    objects = [
        Object(100, np.array([0, 0], dtype='float64'), np.array([0, 0], dtype='float64')),
        Object(1, np.array([1, 0], dtype='float64'), np.array([0, np.sqrt(100)], dtype='float64'))
    ]
    sys = System(objects, 10, 0.02, False)
    create_anim_gif(NAME, sys)