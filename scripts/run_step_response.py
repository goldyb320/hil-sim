"""Milestone 1 demo: open-loop voltage step into the DC motor.

Usage:
    python scripts/run_step_response.py --integrator euler --dt 1e-4
    python scripts/run_step_response.py --integrator rk4 --dt 1e-3

Try increasing --dt with Euler until the simulation goes unstable. Compare with the
motor's electrical time constant L/R. That relationship is why step size matters in HIL.
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

from hil_sim.plant.dc_motor import DCMotorParams, derivatives
from hil_sim.sim.integrators import euler_step, rk4_step

INTEGRATORS = {"euler": euler_step, "rk4": rk4_step}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--integrator", choices=INTEGRATORS, default="euler")
    ap.add_argument("--dt", type=float, default=1e-4, help="timestep [s]")
    ap.add_argument("--t-end", type=float, default=0.5, help="duration [s]")
    ap.add_argument("--volts", type=float, default=12.0)
    ap.add_argument("--load", type=float, default=0.0, help="load torque [N*m]")
    args = ap.parse_args()

    p = DCMotorParams()
    step = INTEGRATORS[args.integrator]
    n = int(args.t_end / args.dt)

    t = np.arange(n + 1) * args.dt
    xs = np.zeros((n + 1, 2))
    for k in range(n):
        f = lambda x: derivatives(x, args.volts, args.load, p)  # noqa: E731
        xs[k + 1] = step(f, xs[k], args.dt)

    fig, (ax_i, ax_w) = plt.subplots(2, 1, sharex=True)
    ax_i.plot(t, xs[:, 0])
    ax_i.set_ylabel("current [A]")
    ax_w.plot(t, xs[:, 1])
    ax_w.set_ylabel("speed [rad/s]")
    ax_w.set_xlabel("time [s]")
    fig.suptitle(f"DC motor step: {args.volts} V, {args.integrator}, dt={args.dt:g} s")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
