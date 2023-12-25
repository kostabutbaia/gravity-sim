import numpy as np

from Object import *
from cases.utils import *
from cases.case import Case

class GravAssist(Case):
    def get_name(self) -> str:
        return 'gravassist'

    def get_objects(self) -> list[Object]:
        d = 10
        self.lim = d+5.2
        MJ = 1
        MS = 2083
        Mv = 4e-25

        r = MS*d/(MJ+MS)/2

        delta_v = np.sqrt(MS/r)*(np.sqrt(2*d/(r+d))-1)+1


        t_h = np.pi*np.sqrt((d+r)**3/(8*MS))
        v_orb = np.sqrt(MS/d)

        theta = t_h*v_orb/(d) + 0.085
        R = MS*d/(MJ+MS)
        # 0.03485 - goes to circlular orbit
        # 03482 - success on second approach
        theta = -np.pi + theta - 0.034818
        return [
            Object(MS, np.array([-MJ*d/(MJ+MS), 0], dtype='float64'), np.array([0, get_orb_speed(1, MS, MJ, d)], dtype='float64')),
            Object(MJ, np.array([R*np.cos(theta), R*np.sin(theta)], dtype='float64'), np.array([get_orb_speed(1, MJ, MS, d)*np.sin(theta), -get_orb_speed(1, MJ, MS, d)*np.cos(theta)], dtype='float64')),
            Object(Mv, np.array([r, 0], dtype='float64'), np.array([0, -get_orb_speed(1, Mv, MS, r)-delta_v], dtype='float64'))
        ]
    
    def get_xlims(self) -> list:
        return [-self.lim, self.lim]

    def get_ylims(self) -> list:
        return [-self.lim, self.lim]