"""Fixed-step numerical integrators.

Each takes f(x) -> dx/dt, the current state x, and a timestep dt_s, and returns
the next state. Inputs are held constant across the step (zero-order hold), which
is exactly what a real controller's PWM update does.
"""

from collections.abc import Callable

import numpy as np

Deriv = Callable[[np.ndarray], np.ndarray]


# Euler Step
def euler_step(f: Deriv, x: np.ndarray, dt_s: float) -> np.ndarray:
    return x + f(x) * dt_s


# RK4 step
def rk4_step(f: Deriv, x: np.ndarray, dt_s: float) -> np.ndarray:
    k1 = f(x)
    k2 = f(x + k1 * dt_s / 2)
    k3 = f(x + k2 * dt_s / 2)
    k4 = f(x + k3 * dt_s)
    return x + (k1 + 2 * k2 + 2 * k3 + k4) * dt_s / 6
