# Roadmap

## Milestone 1: MIL, DC motor (current)
- [ ] Implement `derivatives()` in `plant/dc_motor.py`
- [ ] Implement `euler_step` and `rk4_step`
- [ ] `pytest` passes (steady state matches hand calc)
- [ ] Run `scripts/run_step_response.py`; find the dt where Euler goes unstable and
      relate it to L/R
- [ ] Implement `PIController`, close the speed loop, tune it
- [ ] Add a load-torque step and a frozen-sensor fault

## Milestone 2: SIL
- [ ] Split plant and controller into separate processes (UDP)
- [ ] Fixed-step wall-clock executive that measures jitter and overruns
- [ ] Structured logging to file

## Milestone 3: Operator interface
- [ ] Live plots, parameter changes, start/stop
- [ ] Fault-injection controls
- [ ] Scripted scenarios with pass/fail (pytest-based)

## Milestone 4: PIL
- [ ] Controller on a real MCU, talking to the sim over serial or CAN

## Milestone 5: HIL
- [ ] Electrical I/O front end (DAC/ADC, PWM capture, encoder emulation)
