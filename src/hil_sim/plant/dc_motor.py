"""Brushed DC motor plant model.

State vector:  x = [i_a, omega_rad_s]
    i_a          armature current [A]
    omega_rad_s  shaft speed [rad/s]

Inputs:
    v_applied    terminal voltage [V]
    t_load_nm    load torque opposing motion [N*m]

Equations:
    Electrical: V = L*di/dt + R*i + Ke*omega
    Mechanical: J*domega/dt = Kt*i - b*omega - T_load
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DCMotorParams:
    """Defaults approximate a small 12 V hobby motor."""

    R_ohm: float = 1.0  # winding resistance
    L_h: float = 0.5e-3  # winding inductance
    Ke_v_per_rad_s: float = 0.01  # back-EMF constant
    Kt_nm_per_a: float = 0.01  # torque constant
    J_kg_m2: float = 1e-5  # rotor + load inertia
    b_nm_s_per_rad: float = 1e-6  # viscous friction


# v_applied is the terminal voltage applied to the motor
# t_load_nm is the load torque opposing motion
# p is the DCMotorParams object
def derivatives(x: np.ndarray, v_applied: float, t_load_nm: float, p: DCMotorParams) -> np.ndarray:
    """Return dx/dt = [di_a/dt, domega/dt] for the current state and inputs."""
    i_a, omega_rad_s = x

    # Electrical: V = L*di/dt + R*i + Ke*omega
    # Mechanical: J*domega/dt = Kt*i - b*omega - T_load
    # Equations are rearranged to solve for di/dt and domega/dt.
    di_a_dt = (v_applied - p.R_ohm * i_a - p.Ke_v_per_rad_s * omega_rad_s) / p.L_h
    domega_dt = (p.Kt_nm_per_a * i_a - p.b_nm_s_per_rad * omega_rad_s - t_load_nm) / p.J_kg_m2

    return np.array([di_a_dt, domega_dt])
