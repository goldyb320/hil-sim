# Milestone 1: MIL (DC motor)

What's implemented so far, why it's built this way, and how to run it. See
`docs/roadmap.md` for what's still open on this milestone.

## What's implemented

- **Plant** (`src/hil_sim/plant/dc_motor.py`): `derivatives()`, the brushed DC
  motor's electrical + mechanical ODEs as a pure function
  `(state, inputs, params) -> dstate`.
- **Integrators** (`src/hil_sim/sim/integrators.py`): `euler_step` and
  `rk4_step`, generic fixed-step ODE solvers — they know nothing about motors,
  just `f(x) -> dx/dt`.
- **Controller** (`src/hil_sim/control/pi_controller.py`): `PIController`, a
  PI speed controller with output saturation and anti-windup (the integral
  term resets when the output clips).
- **Scripts**:
  - `scripts/run_step_response.py` — open loop: fixed voltage into the motor,
    plots current and speed. Used to compare Euler vs. RK4 stability.
  - `scripts/run_closed_loop.py` — closed loop: `PIController` driving the
    plant at a speed setpoint, with an optional load-torque step. Plots
    speed (vs. setpoint), voltage command, and current.

## Why it's built this way

**State vector `x = [i_a, omega_rad_s]`.** The motor is two coupled
first-order systems: armature current (electrical) and shaft speed
(mechanical). Current produces torque, torque changes speed, speed produces
back-EMF, back-EMF changes current — that loop is why both have to be
integrated together as one state vector, not two independent ones.

**`derivatives()` is pure.** No `dt`, no I/O, no stored state — it just
answers "what's the slope right now, given this state and these inputs."
That's what makes it testable against a hand calculation (steady state: set
both derivatives to zero and solve) and reusable unchanged all the way up the
X-in-the-loop ladder — MIL, SIL, and eventually PIL/HIL all evaluate the same
equations, just wrapped by different I/O and timing.

**Euler vs. RK4 is a stability question, not just accuracy.** Forward Euler
extrapolates using only the slope at the start of the step; it's cheap but
unstable once `dt` gets large relative to the system's fastest time constant.
For this motor that's the electrical mode, `L/R` — with the default params,
around half a millisecond. `run_step_response.py` lets you find that
instability boundary with Euler directly and see RK4 stay stable at the same
`dt`. This is also why the closed-loop script integrates the plant at 50 µs
by default even though the controller only updates at 1 kHz: the plant's
step size is dictated by its own fastest dynamics, not by how often the
controller looks at it.

**Zero-order hold between controller updates.** A real embedded controller
can't update its output continuously — it computes a command once per sample
period and holds it until the next one. `run_closed_loop.py` models that
explicitly: the plant integrates every `--plant-dt`, but `PIController.update()`
is only called every `--ctrl-hz`, and the voltage in between is held flat
(plotted with `step(..., where="post")` to make that visible rather than
interpolating it away).

## How to run it

Install once:

```
pip install -e ".[dev]"
```

**Unit tests** (plant steady-state hand calc, integrator convergence/order):

```
pytest
```

Currently covers `plant/dc_motor.py` and `sim/integrators.py`
(`tests/test_dc_motor.py`, `tests/test_integrators.py`). `PIController` and
the closed-loop script aren't under automated test yet — they're checked
visually via the plots below.

**Open-loop step response** — watch Euler go unstable, compare to RK4 at the
same `dt`:

```
python scripts/run_step_response.py --integrator euler --dt 1e-4
python scripts/run_step_response.py --integrator euler --dt 1.5e-3   # push past L/R, watch it blow up
python scripts/run_step_response.py --integrator rk4 --dt 1.5e-3     # same dt, stays stable
```

**Closed-loop speed control** — PI controller holding a setpoint, with a mid-run
load-torque step:

```
python scripts/run_closed_loop.py --setpoint 100 --kp 0.02 --ki 0.5
python scripts/run_closed_loop.py --setpoint 150 --kp 0.02 --ki 0.5 --load 5e-4 --load-time 0.25
```

The `--kp`/`--ki` defaults are just starting points, not tuned values —
adjust them and rerun to see the effect on overshoot, settling time, and how
the controller rejects the load step.
