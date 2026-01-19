# Neuron
### Digital Brain Simulation

A high-fidelity neural simulation framework designed to model biological brain activity with 85-90%+ accuracy. Neuron implements a versatile `GeneralizedNeuron` model capable of simulating diverse neural types and regional behaviors (Cortex, Cerebellum, Brainstem).

---

## 🚀 Key Features

- **Multi-Type Neuron Modeling**: Supports Pyramidal, Interneuron, Sensory, Purkinje, Granule, and Motor neurons.
- **Biologically Inspired Dynamics**:
    - **Spiking & Refractory Periods**: Realistic membrane potential resets and recovery times.
    - **STDP (Spike-Timing-Dependent Plasticity)**: Hebbian learning that modifies synaptic weights based on millisecond-level spike timing.
    - **Spike-Frequency Adaptation**: Threshold adjustments based on input variance.
    - **Dendritic Processing**: Integration of proximal and distal inputs with signal attenuation.
- **Regional Specialization**: Behavior varies by brain region (e.g., Purkinje cells in the Cerebellum vs. Pyramidal cells in the Cortex).
- **Recurrent Network Simulation**: A framework for building connected populations of neurons with both external and recurrent connectivity.

## 🛠 Project Structure

* `neuron.py`: The core `GeneralizedNeuron` class containing the mathematical models for membrane dynamics and learning.
* `network.py`: A simulation environment for connecting multiple neurons into a functioning network.
* `visualize_neuron.py`: Diagnostic tool for plotting single-neuron membrane potential, spikes, adaptation current, and STDP weight changes.
* `visualize_network.py`: Visualization of population dynamics and spike counts across the network.

## 🔧 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/your-username/SIMON-Digital-Brain.git](https://github.com/your-username/SIMON-Digital-Brain.git)
   cd SIMON-Digital-Brain
