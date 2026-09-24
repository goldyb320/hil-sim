# 0001: Start in Python

Status: accepted

## Context
The project is a learning exercise; early milestones are offline (MIL) and need fast
iteration and easy plotting more than hard real-time performance.

## Decision
Write milestones 1-3 in Python. Revisit the real-time executive's language (C++/Rust)
before or during milestone 2 if jitter measurements show Python can't hold the target step.

## Consequences
Fast learning loop now; possible port of the executive and plant later.