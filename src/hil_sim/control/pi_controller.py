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
    last_p: float = 0.0
    last_i: float = 0.0

    def reset(self) -> None:
        self.integral = 0.0
        self.last_p = 0.0
        self.last_i = 0.0

    def update(self, setpoint: float, measurement: float, dt_s: float) -> float:
        """Return the actuator command for this step.

        Anti-windup uses conditional integration: while the output is saturated,
        the integral is frozen (not reset), unless the error would pull the
        output back out of saturation.
        """
        error = setpoint - measurement
        p_term = self.kp * error

        # Propose the new integral, but don't commit it yet.
        candidate = self.integral + error * dt_s
        unclamped = p_term + self.ki * candidate

        # Would integrating push us further into a limit we're already past?
        pushing_high = unclamped > self.output_max and error > 0
        pushing_low = unclamped < self.output_min and error < 0
        if not (pushing_high or pushing_low):
            self.integral = candidate
        # else: keep self.integral exactly as it was (frozen)

        i_term = self.ki * self.integral
        output = min(max(p_term + i_term, self.output_min), self.output_max)

        self.last_p = p_term
        self.last_i = i_term
        return output
