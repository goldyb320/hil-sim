"""Milestone 1 demo: closed-loop speed control of the DC motor.

The plant integrates with RK4 at --plant-dt. The PI controller runs much slower,
at --ctrl-hz, and its voltage command is held constant (zero-order hold) between
updates -- exactly what a real embedded controller's PWM/DAC output does between
sample periods.

Usage:
    python scripts/run_closed_loop.py --setpoint 100 --kp 0.02 --ki 0.5
    python scripts/run_closed_loop.py --setpoint 150 --kp 0.02 --ki 0.5 \
        --load 5e-4 --load-time 0.25
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

from hil_sim.control.pi_controller import PIController
from hil_sim.plant.dc_motor import DCMotorParams, derivatives
from hil_sim.sim.integrators import rk4_step


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plant-dt", type=float, default=50e-6, help="plant integration step [s]")
    ap.add_argument("--ctrl-hz", type=float, default=1000.0, help="controller update rate [Hz]")
    ap.add_argument("--setpoint", type=float, default=100.0, help="speed setpoint [rad/s]")
    ap.add_argument("--kp", type=float, default=0.02, help="proportional gain")
    ap.add_argument("--ki", type=float, default=0.5, help="integral gain")
    ap.add_argument("--v-max", type=float, default=12.0, help="+/- voltage command limit [V]")
    ap.add_argument("--t-end", type=float, default=0.5, help="duration [s]")
    ap.add_argument("--load", type=float, default=0.0, help="load torque step [N*m]")
    ap.add_argument("--load-time", type=float, default=0.25, help="when the load step hits [s]")
    args = ap.parse_args()

    plant_dt = args.plant_dt
    ctrl_dt = 1.0 / args.ctrl_hz
    ctrl_period_steps = round(ctrl_dt / plant_dt)
    if abs(ctrl_period_steps * plant_dt - ctrl_dt) > 1e-12:
        print(
            f"warning: --ctrl-hz ({args.ctrl_hz:g}) is not an integer multiple of "
            f"--plant-dt ({plant_dt:g}); rounding to every {ctrl_period_steps} plant steps"
        )

    p = DCMotorParams()
    ctrl = PIController(kp=args.kp, ki=args.ki, output_min=-args.v_max, output_max=args.v_max)

    n = int(round(args.t_end / plant_dt))
    t = np.arange(n + 1) * plant_dt
    xs = np.zeros((n + 1, 2))
    v_cmd = np.zeros(n + 1)

    v = 0.0
    for k in range(n):
        if k % ctrl_period_steps == 0:
            v = ctrl.update(args.setpoint, xs[k, 1], ctrl_dt)
        v_cmd[k] = v

        t_load = args.load if t[k] >= args.load_time else 0.0
        f = lambda x, v=v, t_load=t_load: derivatives(x, v, t_load, p)  # noqa: E731
        xs[k + 1] = rk4_step(f, xs[k], plant_dt)
    v_cmd[n] = v

    fig, (ax_w, ax_v, ax_i) = plt.subplots(3, 1, sharex=True)

    ax_w.plot(t, xs[:, 1], label="speed")
    ax_w.axhline(args.setpoint, color="k", linestyle="--", label="setpoint")
    ax_w.set_ylabel("speed [rad/s]")
    ax_w.legend()

    ax_v.step(t, v_cmd, where="post")
    ax_v.set_ylabel("voltage cmd [V]")

    ax_i.plot(t, xs[:, 0])
    ax_i.set_ylabel("current [A]")
    ax_i.set_xlabel("time [s]")

    fig.suptitle(
        f"Closed loop: setpoint={args.setpoint:g} rad/s, "
        f"kp={args.kp:g}, ki={args.ki:g}, ctrl={args.ctrl_hz:g} Hz"
    )
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
