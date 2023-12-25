import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import numpy as np
import os

from solvers.System import *
from Object import *
from Trail import *

from solvers.Verlet import *
from solvers.VelocityVerlet import *
from solvers.Leapfrog import *

import cases.elliptic
from cases.case import Case
from cases.elliptic import *

TRAIL_LENGTH = 200

def create_anim_gif(
        system: System,
        case: Case,
) -> None:
    fig = plt.figure()
    plt.xlim(case.get_xlims()[0], case.get_xlims()[1])
    plt.ylim(case.get_ylims()[0], case.get_ylims()[1])
    plt.grid()
    plt.gca().set_aspect('equal')
    plt.title(f'${case.get_name()}$: {system.get_method_name()} | $\delta t={system.get_time_step()}$')

    info, frames = system.get_frames()
    l, = plt.plot([], [], 'o')

    trail_plots = []
    trails: list[Trail] = []
    for _ in range(system.amount()):
        p, = plt.plot([], [])
        trails.append(Trail(TRAIL_LENGTH))
        trail_plots.append(p)
    
    writer = PillowWriter(fps=15)

    full_path = f'solutions/{case.get_name()}/{system.get_method_name()}/{case.get_name()}_{system.get_time_step()}.gif'
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with writer.saving(fig, full_path, 100):
        for i, frame in enumerate(frames):
            # plt.title(f'${case.get_name()}$: {system.get_method_name()} | $\delta t={system.get_time_step()}$ | info: {round(np.linalg.norm(info[i][1]), 4)}')
            x_points, y_points = frame
            l.set_data(x_points, y_points)
            for i in range(len(trails)):
                x_trail, y_trail = trails[i].update_trail(x_points[i], y_points[i])
                trail_plots[i].set_data(x_trail, y_trail)
            
            writer.grab_frame()

if __name__ == '__main__':
    objects = Elliptic().get_objects()
    sys = Leapfrog(objects, 10, 0.02, True)

    create_anim_gif(sys, Elliptic())