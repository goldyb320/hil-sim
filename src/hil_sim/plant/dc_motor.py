"""Brushed DC motor plant model.

State vector:  x = [i_a, omega_rad_s]
    i_a          armature current [A]
    omega_rad_s  shaft speed [rad/s]

Inputs:
    v_applied    terminal voltage [V]
    t_load_nm    load torque opposing motion [N*m]

Equations (write these yourself -- see docs/roadmap.md, milestone 1):
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


def derivatives(
    x: np.ndarray, v_applied: float, t_load_nm: float, p: DCMotorParams
) -> np.ndarray:
    """Return dx/dt = [di_a/dt, domega/dt] for the current state and inputs."""
    raise NotImplementedError("Milestone 1: implement the two DC motor equations")
