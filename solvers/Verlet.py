import numpy as np
from Object import Object

from solvers.System import *

class Verlet(System):
    G = 1
    def __init__(self, objects: list[Object], t_final: float, t_step: float, follow_center: bool):
        self.objects = objects
        self.t_final = t_final
        self.t_step = t_step
        self.follow_center = follow_center
    
    def get_time_step(self) -> int:
        return self.t_step

    def get_method_name(self) -> str:
        return 'Verlet'

    def amount(self) -> int:
        return len(self.objects)

    def get_acceleration(ob1: Object, ob2: Object) -> list[float]:
        return -Verlet.G * ob2.m/np.linalg.norm(ob1.positions[-1] - ob2.positions[-1])**3 * (ob1.positions[-1] - ob2.positions[-1])
    
    def center_of_mass_velocity(self) -> list:
        return sum([o.m*o.v  for o in self.objects])/sum([o.m for o in self.objects])
    
    def _follow_mass_center(self):
        mass_vel = self.center_of_mass_velocity()
        for o in self.objects:
            o.v -= mass_vel

    def get_system_pos_state(self) -> list:
        x_cords = []
        y_cords = []
        for o in self.objects:
            x_cords.append(o.positions[-1][0])
            y_cords.append(o.positions[-1][1])
        return [x_cords, y_cords]

    def _update_object(self, ob: Object):
        if ob.first_iter:
            ob.first_iter = False
            value = ob.r + ob.v*self.t_step
            for o in self.objects:
                if o is not ob:
                    a = Verlet.get_acceleration(ob, o)
                    value += 1/2*a*self.t_step**2

            return value
        else:
            last_term = 0
            for o in self.objects:
                if o is not ob:
                    a = Verlet.get_acceleration(ob, o)
                    last_term += a * self.t_step**2
            new_pos = 2*ob.positions[-1] - ob.positions[-2] + last_term
            return new_pos

    def _update_system(self):
        updates = dict()
        for o in self.objects:
            updates[id(o)] = self._update_object(o)
        for o in self.objects:
            o.positions.append(updates[id(o)])

    def get_frames(self) -> list:
        if self.follow_center: self._follow_mass_center()
        t_range = np.arange(0, self.t_final, self.t_step)
        frames = []
        for t in t_range:
            frames.append(self.get_system_pos_state())
            self._update_system()
        return t_range, frames

def main():
    objects = [
        Object(1, np.array([0, 0], dtype='float64'), np.array([0, 0], dtype='float64')),
        Object(1, np.array([1, 0], dtype='float64'), np.array([0, 1], dtype='float64'))
    ]

    sys = System(objects, 10, 0.02, False)


if __name__ == '__main__':
    main()