# hil-sim

A hardware-in-the-loop (HIL) simulator, built from scratch as a learning project.

The plan is software first (MIL -> SIL), then a real-time executive and operator
interface, then real hardware (PIL -> HIL). The first plant is a brushed DC motor;
the first device under test will be a simple motor controller.

See `docs/roadmap.md` for milestones and `docs/glossary.md` for terminology.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Common commands

```bash
pytest                           # run tests
ruff check .                     # lint
python scripts/run_step_response.py   # milestone 1 open-loop step response
```
