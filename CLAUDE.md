# CLAUDE.md

Context for Claude Code. Read this at the start of every session.

## What this project is

`hil-sim` is a hardware-in-the-loop (HIL) simulator that Ben is building from scratch
to learn how HIL works. Ben is a computer engineer with embedded and motor-control
experience but is new to HIL. The primary goal is **understanding**, not just a
working tool.

Development follows the X-in-the-loop ladder:
1. **MIL**: plant + controller as Python functions, simulated offline.
2. **SIL**: plant and controller as separate processes, fixed-step real-time loop,
   virtual I/O (UDP / shared memory / Linux vcan).
3. Operator interface: live plots, parameters, fault injection, scripted scenarios, logging.
4. **PIL**: controller runs on a real MCU, talking to the sim over serial/CAN.
5. **HIL**: real electrical I/O (DAC/ADC, PWM capture, encoder emulation).

First plant: brushed DC motor. First DUT: a simple motor controller (not yet built).

## How to help (important)

- **Explain before writing.** For anything conceptual, explain the idea and the
  tradeoffs first, then propose code.
- **Ben writes the physics and control laws.** Do NOT implement plant models
  (`src/hil_sim/plant/`), control laws (`src/hil_sim/control/`), or numerical
  integrators (`src/hil_sim/sim/integrators.py`) unless Ben explicitly asks. Instead:
  review his code, point out bugs, suggest tests, ask guiding questions.
- **Scaffolding is fair game.** Plotting, CLI scripts, test harnesses, logging,
  config, CI, and UI boilerplate can be written directly.
- Keep changes small and reviewable. One concept per change.
- When something could matter for real-time behavior later (allocation in the loop,
  blocking I/O, variable timesteps), call it out even if we're offline for now.

## Architecture rules

- `plant/`: pure functions. `derivatives(state, inputs, params) -> dstate`.
  No I/O, no timing, no global state. Must be unit-testable.
- `control/`: controllers only see what a real controller would (measured signals,
  setpoints) and output actuator commands. They never read plant state directly.
- `sim/`: integrators and (later) the fixed-step real-time executive.
- `io/` (later): the I/O abstraction layer. One interface, swappable backends
  (virtual now, real hardware later). The plant and controller must not know
  which backend is in use.
- Scripts in `scripts/` wire things together; library code never imports from scripts.

## Conventions

- Python 3.11+. Type hints on public functions. `numpy` for state vectors.
- **SI units everywhere.** Put the unit in the name when it isn't obvious:
  `omega_rad_s`, `i_a`, `v_applied`, `dt_s`, `J_kg_m2`.
- State vectors are documented at the top of each plant module
  (e.g. DC motor: `x = [i_a, omega_rad_s]`).
- Parameters live in frozen dataclasses with realistic default values.
- Every plant model gets a steady-state test against a hand calculation.

## Commands

- Install: `pip install -e ".[dev]"` (inside `.venv`)
- Test: `pytest`
- Lint: `ruff check .` / format: `ruff format .`
- Milestone 1 demo: `python scripts/run_step_response.py`

## Current status

Milestone 1 (MIL, DC motor). See `docs/roadmap.md`. Update this line as milestones complete.
