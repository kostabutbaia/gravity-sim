import numpy as np
from Object import Object

from functools import reduce
from System import *

G = 1
def get_orbit_speed(M: float, R: float) -> float:
    return np.sqrt(G*M/R)

class VelocityVerlet(System):
    def __init__(self, objects: list[Object], t_final: float, t_step: float, follow_center: bool):
        self.objects = objects
        self.t_final = t_final
        self.t_step = t_step
        self.follow_center = follow_center

    def amount(self) -> int:
        return len(self.objects)

    def get_acceleration(r1: list, r2: list, M2: float) -> list[float]:
        return -G * M2/np.linalg.norm(r1 - r2)**3 * (r1 - r2)
    
    def center_of_mass_velocity(self) -> list:
        return reduce(lambda o1, o2: o1.m*o1.v + o2.m*o2.v, self.objects)/reduce(lambda o1, o2: o1.m + o2.m, self.objects)
    
    def _follow_mass_center(self):
        mass_vel = self.center_of_mass_velocity()
        for o in self.objects:
            o.v -= mass_vel

    def get_system_pos_state(self) -> list:
        x_cords = []
        y_cords = []
        for o in self.objects:
            x_cords.append(o.r[0])
            y_cords.append(o.r[1])
        return [x_cords, y_cords]
    
    def get_energy(self):
        E_k = sum([o.m*np.linalg.norm(o.v)**2/2 for o in self.objects])
        E_p = 0
        for o1 in self.objects:
            for o2 in self.objects:
                if o1 is not o2:
                    E_p += G*o1.m*o2.m/np.linalg.norm(o1.r-o2.r)
        return E_k - 1/2*E_p

    def _update_object_r(self, ob: Object):
        new_r = ob.r + ob.v*self.t_step
        for o in self.objects:
            if o is not ob:
                # Velocity Verlet Integration
                a = VelocityVerlet.get_acceleration(ob.r, o.r, o.m)
                new_r += 1/2*a*self.t_step**2
        return new_r
    
    def _update_object_v(self, ob: Object, updates_r: dict):
        new_v = np.array(ob.v)
        for o in self.objects:
            if o is not ob:
                # Velocity Verlet Integration
                a = VelocityVerlet.get_acceleration(ob.r, o.r, o.m)
                new_v += self.t_step/2*(a+VelocityVerlet.get_acceleration(updates_r[id(ob)], updates_r[id(o)], o.m))
        return new_v

    def _update_system(self):
        updates_r = dict()
        updates_v = dict()
        for o in self.objects:
            updates_r[id(o)] = self._update_object_r(o)
        for o in self.objects:
            updates_v[id(o)] = self._update_object_v(o, updates_r)
        for o in self.objects:
            o.r = updates_r[id(o)]
            o.v = updates_v[id(o)]

    def get_frames(self) -> list:
        if self.follow_center: self._follow_mass_center()
        t_range = np.arange(0, self.t_final, self.t_step)
        frames = []
        energies=[]
        for t in t_range:
            frames.append(self.get_system_pos_state())
            self._update_system()
            energies.append(self.get_energy())
        return t_range, frames


def main():
    objects = [
        Object(1, np.array([0, 0], dtype='float64'), np.array([0, 0], dtype='float64')),
        Object(1, np.array([1, 0], dtype='float64'), np.array([0, 1], dtype='float64'))
    ]

    sys = System(objects, 10, 0.02, True)


if __name__ == '__main__':
    main()