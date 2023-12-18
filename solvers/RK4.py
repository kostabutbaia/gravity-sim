import numpy as np
from Object import Object

from solvers.System import *

class RK4(System):
    G = 1
    def __init__(self, objects: list[Object], t_final: float, t_step: float, follow_center: bool):
        self.objects = objects
        self.t_final = t_final
        self.t_step = t_step
        self.follow_center = follow_center
    
    def get_time_step(self) -> int:
        return self.t_step

    def get_method_name(self) -> str:
        return 'RK4'

    def amount(self) -> int:
        return len(self.objects)

    def get_acceleration(r1: list, r2: list, M2: float) -> list[float]:
        return -RK4.G * M2/np.linalg.norm(r1 - r2)**3 * (r1 - r2)
    
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
        a = 0
        for o in self.objects:
            if o is not ob:
                a += RK4.get_acceleration(ob.r, o.r, o.m)
        k1 = self.t_step*a
        l1 = self.t_step*ob.velocities[-1]

        a = 0
        for o in self.objects:
            if o is not ob:
                a += RK4.get_acceleration(ob.r+0.5*l1, o.r, o.m)
        k2 = self.t_step*a
        l2 = self.t_step*(ob.velocities[-1] + 0.5*k1)

        a = 0
        for o in self.objects:
            if o is not ob:
                a += RK4.get_acceleration(ob.r+0.5*l2, o.r, o.m)
        k3 = self.t_step*a
        l3 = self.t_step*(ob.velocities[-1] + 0.5*k2)

        a = 0
        for o in self.objects:
            if o is not ob:
                a += RK4.get_acceleration(ob.r+l3, o.r, o.m)
        k4 = self.t_step*a
        l4 = self.t_step*(ob.velocities[-1] + k3)

        v_new = ob.velocities[-1] + 1/6*(k1+2*k2+2*k3+k4)
        pos_new = ob.positions[-1] + 1/6*(l1+2*l2+2*l3+l4)

        return pos_new, v_new

    def _update_system(self):
        updates = dict()
        for o in self.objects:
            updates[id(o)] = self._update_object(o)
        for o in self.objects:
            pos_new, v_new = updates[id(o)]
            o.positions.append(pos_new)
            o.velocities.append(v_new)
            o.r = pos_new

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