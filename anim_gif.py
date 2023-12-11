import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import numpy as np

from System import *
from Object import *
from Trail import *

from Verlet import *
from VelocityVerlet import *

NAME = 'VelocityVerlet2'
TRAIL_LENGTH = 70

def create_anim_gif(
        name: str, 
        title: str, 
        system: System,
        xlims: list[float],
        ylims: list[float]
) -> None:
    fig = plt.figure()
    plt.xlim(xlims[0], xlims[1])
    plt.ylim(ylims[0], ylims[1])
    plt.grid()
    plt.gca().set_aspect('equal')
    plt.title(title)

    _, frames = system.get_frames()
    l, = plt.plot([], [], 'o')

    trail_plots = []
    trails: list[Trail] = []
    for _ in range(system.amount()):
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
        Object(2, np.array([0, 0], dtype='float64'), np.array([0, 0], dtype='float64')),
        Object(1, np.array([1, 0], dtype='float64'), np.array([0, 1], dtype='float64'))
    ]
    sys = VelocityVerlet(objects, 10, 0.02, True)

    create_anim_gif(NAME, 'Velocity Verlet 1', sys, [-2, 2], [-1, 3])