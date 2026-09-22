"""Fixed-step numerical integrators.

Each takes f(x) -> dx/dt, the current state x, and a timestep dt_s, and returns
the next state. Inputs are held constant across the step (zero-order hold), which
is exactly what a real controller's PWM update does.
"""

from collections.abc import Callable

import numpy as np

Deriv = Callable[[np.ndarray], np.ndarray]


def euler_step(f: Deriv, x: np.ndarray, dt_s: float) -> np.ndarray:
    raise NotImplementedError("Milestone 1: forward Euler")


def rk4_step(f: Deriv, x: np.ndarray, dt_s: float) -> np.ndarray:
    raise NotImplementedError("Milestone 1: classic 4th-order Runge-Kutta")
