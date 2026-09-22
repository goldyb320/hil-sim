# Glossary

- **HIL**: Hardware-in-the-loop. Real controller hardware wired to a real-time simulation of what it controls.
- **DUT / UUT**: Device / unit under test.
- **Plant**: The physical system being controlled (motor + load). The plant model is its math.
- **MIL**: Model-in-the-loop. Controller and plant both simulated offline.
- **SIL**: Software-in-the-loop. Real controller code, compiled for a PC, against the plant model.
- **PIL**: Processor-in-the-loop. Controller code on the real MCU, data exchanged over a digital link.
- **ECU**: Electronic control unit (automotive term for an embedded controller).
- **Real-time**: Every step finishes before a hard wall-clock deadline.
- **Fixed-step**: The sim advances by the same dt every step.
- **Jitter / overrun**: Variation in step timing / a step that missed its deadline.
- **RTOS / PREEMPT_RT**: Real-time OS / the Linux real-time kernel patch set.
- **ADC / DAC**: Analog-to-digital / digital-to-analog converter.
- **PWM**: Pulse-width modulation.
- **CAN**: Controller Area Network bus.
- **FPGA**: Reconfigurable hardware, used for microsecond-scale sim loops.
- **FMI / FMU**: Standard for packaging simulation models / one packaged model.
- **Fault injection**: Deliberately simulating failures to test the controller's response.
- **Zero-order hold**: Holding an input constant across a timestep.
