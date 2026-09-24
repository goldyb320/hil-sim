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
        self.integral = 0.0

    def update(self, setpoint: float, measurement: float, dt_s: float) -> float:
        """Return the actuator command for this step.

        Things to think about: output saturation, and integrator windup when saturated.
        """

        # Set points for the proportional and integral error terms, integral use for seped control
        error = setpoint - measurement
        self.integral += error * dt_s

        output = self.kp * error + self.ki * self.integral
        if output < self.output_min:
            self.integral = 0.0
            output = self.output_min
        elif output > self.output_max:
            self.integral = 0.0
            output = self.output_max
        return output
