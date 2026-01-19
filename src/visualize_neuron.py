import numpy as np
import matplotlib.pyplot as plt
from src.neuron import GeneralizedNeuron

# Simulate a pyramidal neuron
neuron = GeneralizedNeuron(num_inputs=3, neuron_type="pyramidal", region="cortex", time_step=0.1)
time_steps = 100
inputs = [np.array([2.0, 2.0, 2.0]) for t in range(time_steps)]  # Sustained inputs
membrane_potentials = []
spikes = []
adaptation_currents = []
weights = []

# Run simulation
for t in range(time_steps):
    output = neuron.forward(inputs[t])
    membrane_potentials.append(neuron.membrane_potential)
    spikes.append(output)
    adaptation_currents.append(neuron.adaptation_current)
    weights.append(neuron.weights[0])  # Track first weight

# Plot results
time = np.arange(0, time_steps * neuron.time_step, neuron.time_step)
plt.figure(figsize=(10, 10))
plt.subplot(4, 1, 1)
plt.plot(time, membrane_potentials, label="Membrane Potential (mV)")
plt.axhline(neuron.threshold, color='r', linestyle='--', label="Threshold")
plt.title("Pyramidal Neuron: Membrane Potential")
plt.xlabel("Time (ms)")
plt.ylabel("Potential (mV)")
plt.legend()

plt.subplot(4, 1, 2)
plt.stem(time, spikes, label="Spikes")
plt.title("Spikes")
plt.xlabel("Time (ms)")
plt.ylabel("Spike (1 or 0)")
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(time, adaptation_currents, label="Adaptation Current (mA)")
plt.title("Adaptation Current")
plt.xlabel("Time (ms)")
plt.ylabel("Current (mA)")
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(time, weights, label="Weight (Synapse 0)")
plt.title("STDP Weight Changes")
plt.xlabel("Time (ms)")
plt.ylabel("Weight")
plt.legend()

plt.tight_layout()
plt.show()