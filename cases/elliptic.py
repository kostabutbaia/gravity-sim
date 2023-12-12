import numpy as np

from Object import *
from cases.utils import *
from cases.case import Case

class Elliptic(Case):
    def get_name(self) -> str:
        return 'elliptic'

    def get_objects(self) -> list[Object]:
        d = 1
        Mc = 0.0001
        Mp = 2
        return [
            Object(Mp, np.array([-Mc*d/(Mc+Mp), 0], dtype='float64'), np.array([0, get_orb_speed(1, Mp, Mc, d)], dtype='float64')),
            Object(Mc, np.array([Mp*d/(Mc+Mp), 0], dtype='float64'), np.array([0, -get_orb_speed(1, Mc, Mp, d)+0.8], dtype='float64'))
        ]
    
    def get_xlims(self) -> list:
        return [-1.2, 1.2]

    def get_ylims(self) -> list:
        return [-1.2, 1.2]