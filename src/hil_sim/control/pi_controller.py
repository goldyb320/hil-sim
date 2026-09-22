"""PI controller.

A controller only sees what a real one would: a setpoint and a measurement.
It must never read plant state directly.
"""

from dataclasses import dataclass


@dataclass
class PIController:
    kp: float
    ki: float
    output_min: float
    output_max: float
    integral: float = 0.0

    def reset(self) -> None:
        raise NotImplementedError("Milestone 1: reset internal state")

    def update(self, setpoint: float, measurement: float, dt_s: float) -> float:
        """Return the actuator command for this step.

        Things to think about: output saturation, and integrator windup when saturated.
        """
        raise NotImplementedError("Milestone 1: implement the PI law")
