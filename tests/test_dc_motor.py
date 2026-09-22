import numpy as np

from hil_sim.plant.dc_motor import DCMotorParams, derivatives


def test_at_rest_with_no_voltage_nothing_happens():
    p = DCMotorParams()
    dx = derivatives(np.zeros(2), v_applied=0.0, t_load_nm=0.0, p=p)
    np.testing.assert_allclose(dx, [0.0, 0.0])


def test_steady_state_matches_hand_calculation():
    # Derive this yourself before reading: set both derivatives to zero and
    # solve for i and omega given V and T_load.
    p = DCMotorParams()
    v, t_load = 12.0, 0.0
    omega_ss = p.Kt_nm_per_a * v / (p.R_ohm * p.b_nm_s_per_rad + p.Kt_nm_per_a * p.Ke_v_per_rad_s)
    i_ss = (v - p.Ke_v_per_rad_s * omega_ss) / p.R_ohm

    dx = derivatives(np.array([i_ss, omega_ss]), v, t_load, p)
    np.testing.assert_allclose(dx, [0.0, 0.0], atol=1e-9)
