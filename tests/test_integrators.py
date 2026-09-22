import numpy as np

from hil_sim.sim.integrators import euler_step, rk4_step


def _decay(x: np.ndarray) -> np.ndarray:
    return -x  # dx/dt = -x, exact solution x(t) = x0 * exp(-t)


def _integrate(step, dt: float, t_end: float = 1.0) -> float:
    x = np.array([1.0])
    for _ in range(round(t_end / dt)):
        x = step(_decay, x, dt)
    return float(x[0])


def test_euler_converges():
    assert abs(_integrate(euler_step, 1e-4) - np.exp(-1)) < 1e-4


def test_rk4_is_much_more_accurate_than_euler():
    exact = np.exp(-1)
    err_euler = abs(_integrate(euler_step, 1e-2) - exact)
    err_rk4 = abs(_integrate(rk4_step, 1e-2) - exact)
    assert err_rk4 < err_euler / 1000
