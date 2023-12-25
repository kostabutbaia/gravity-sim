import numpy as np

from Object import *
from cases.utils import *
from cases.case import Case

class Curve(Case):
    def get_name(self) -> str:
        return 'curve'

    def get_objects(self) -> list[Object]:
        self.lim = 15
        M = 5
        u = 1
        v = u + (M)**(1/2)

        return [
            Object(M, np.array([0.5, 0], dtype='float64'), np.array([u, 0], dtype='float64')),
            Object(0.0001, np.array([0, -5], dtype='float64'), np.array([u, v], dtype='float64'))
        ]

    def get_xlims(self) -> list:
        return [-5, 10]

    def get_ylims(self) -> list:
        return [-5, 10]