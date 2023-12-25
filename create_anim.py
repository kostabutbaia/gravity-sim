from copy import deepcopy
import numpy as np

from cases.case import Case

from solvers.Verlet import *
from solvers.VelocityVerlet import *
from solvers.Leapfrog import *
from solvers.RK4 import *

from anim_gif import create_anim_gif

from cases.elliptic import *
from cases.pluto_charon import *
from cases.assist import *
from cases.curve import *
from cases.gravassist import *


def create_anims(case: Case, t_final: float, t_step: float, follow_center: bool) -> None:
    objects = case.get_objects()

    system_RK4 = RK4(deepcopy(objects), t_final, t_step, follow_center)
    # system_verlet = Verlet(deepcopy(objects), t_final, t_step, follow_center)
    # system_velocityVerlet = VelocityVerlet(deepcopy(objects), t_final, t_step, follow_center)
    # system_leapfrog = Leapfrog(deepcopy(objects), t_final, t_step, follow_center)

    create_anim_gif(system_RK4, case)
    # print('RK4 Method Done!')
    # create_anim_gif(system_velocityVerlet, case)
    # print('Velocity Verlet Method Done!')
    # create_anim_gif(system_leapfrog, case)
    # print('Leapfrog Method Done!')

if __name__ == '__main__':
    create_anims(GravAssist(), 10, 0.01, False)

