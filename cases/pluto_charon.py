import numpy as np

from Object import *
from cases.utils import *
from cases.case import Case

class PlutoCharon(Case):
    def get_name(self) -> str:
        return 'plutocharon'

    def get_objects(self) -> list[Object]:
        d = 1
        Mc = 1
        Mp = 8.253
        return [
            Object(Mp, np.array([-Mc*d/(Mc+Mp), 0], dtype='float64'), np.array([0, get_orb_speed(1, Mp, Mc, d)], dtype='float64')),
            Object(Mc, np.array([Mp*d/(Mc+Mp), 0], dtype='float64'), np.array([0, -get_orb_speed(1, Mc, Mp, d)], dtype='float64'))
        ]
    
    def get_xlims(self) -> list:
        return [-1, 1]

    def get_ylims(self) -> list:
        return [-1, 1]