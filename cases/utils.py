import numpy as np

def get_orb_speed(G: float, M1: float, M2: float, d: float) -> float:
    return M2*np.sqrt(G/(d*(M1 + M2)))