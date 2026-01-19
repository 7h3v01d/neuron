# Digital Brain Simulation Project

This repository contains a simulation of a digital brain using a `GeneralizedNeuron` class, designed to model neural behavior with high fidelity (targeting 85-90%+ accuracy). The project focuses on implementing various neuron types (e.g., pyramidal, interneuron, sensory) with region-specific properties, supporting spiking dynamics, adaptation, STDP learning, and dendritic processing.

## Overview

The core component is the `GeneralizedNeuron` class, written in Python, which simulates neuron behavior based on inputs, weights, and internal states (e.g., membrane potential, refractory period). The project includes testing, network simulation, and visualization scripts to validate and explore the model.

- **Goal**: Achieve a digital brain model with realistic neural interactions, optimized for specific neurons (e.g., Neuron 9 as inhibitory, early spiking for Neurons 2, 3, 5, and optimized activity for Neuron 8).
- **Status**: Under active development with a working neuron model and initial tests.

## Features

- **Neuron Types**: Supports pyramidal, interneuron, sensory, purkinje, granule, motor, and generic neurons with type-specific properties.
- **Regions**: Models cortex, cerebellum, and brainstem regions with region-specific adjustments.
- **Dynamics**: Implements spiking, refractory periods, adaptation, and STDP (Spike-Timing-Dependent Plasticity) learning.
- **Dendritic Processing**: Separates proximal and distal inputs with attenuation.
- **Testing**: Unit tests for initialization, spiking, adaptation, learning, and input validation.

## Getting Started

### Prerequisites

- Python 3.x
- NumPy (`pip install numpy`)
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:
```bash
   git clone <repository-url>
```
```bash
   cd S.I.M.O.N
```
Set up a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```
Install dependencies:
```bash
pip install numpy
```

## Project Structure

neuron.py: Core implementation of the GeneralizedNeuron class.
test_neuron.py: Unit tests for the neuron model.
network.py: Simulation of a neural network (to be developed or refined).
visualize_neuron.py: Visualization script for neuron activity (to be developed or refined).

Running the Project

Run Tests:
```bash
python -m unittest test_neuron.py
```
Ensures the neuron model behaves as expected. Debug output includes initialization logs.


Run Simulation:
``bash
python network.py
```
Simulates the neural network. Verify Neuron 9’s ~20 inhibitory spikes over 40 steps.


Run Visualization:
```bash
python visualize_neuron.py
```
Generates plots of neuron activity. Upload or describe outputs for analysis.



## Usage
Configuring Neurons
Create a neuron instance with desired parameters:
pythonfrom neuron import GeneralizedNeuron
neuron = GeneralizedNeuron(num_inputs=10, neuron_type="interneuron", region="cortex", time_step=0.5)
state = neuron.forward(inputs)  # Process inputs and get spike output

num_inputs: Number of input synapses.
neuron_type: One of ["pyramidal", "interneuron", "sensory", "purkinje", "granule", "motor", "generic"].
region: One of ["cortex", "cerebellum", "brainstem"].
time_step: Simulation time step (default 0.5).

## Key Behaviors

Spiking: Triggered when membrane potential exceeds threshold, with refractory period.
Adaptation: Adjusts threshold based on input variance (sensory neurons).
STDP: Modifies weights based on spike timing differences.
Inhibitory/Excitatory: is_excitatory=False for interneurons and purkinje, True for others.

## Development
Current Status

Neuron Model: Functional with core dynamics and learning.
Tests: Passing 5/6 tests (failure in test_initialization due to output_scaling mismatch, resolved in latest version).
Network: Partial implementation; expand with network topology.
Visualization: Basic plotting; enhance with detailed metrics.

## Known Issues

output_scaling for "motor" in "brainstem" defaults to 1.0 but was expected as 2.0 or 3.0 in tests. Adjust neuron.py if scaling is intentional.
Interneuron excitatory switch in test_adaptive_behavior was removed; verify if dynamic switching is required.

## Future Work

Expand network.py to include Neuron 9’s inhibitory role, early spiking for Neurons 2, 3, 5, and Neuron 8’s optimization.
Enhance visualize_neuron.py with real-time plotting and spike train analysis.
Add more neuron types or parameters based on biological data.

## Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Description").
Push to the branch (git push origin feature-name).
Open a pull request.

## License
[Specify license, e.g., MIT] - Add your preferred license text here.
Contact
For questions or collaboration, contact [your-email] or raise an issue in the repository.
Acknowledgments

Inspired by xAI’s digital brain research.
Built with guidance from Grok 3, developed by xAI.

text### Notes
- **Customization**: Replace `<repository-url>`, `[your-email]`, and the license section with your details.
- **File Inclusion**: Ensure `neuron.py`, `test_neuron.py`, `network.py`, and `visualize_neuron.py` are included when moving the project.
- **Version Sync**: The `README` reflects the latest `neuron.py` and updated `test_neuron.py`. If you revert to an older version, adjust the "Current Status" section accordingly.
- **Output Scaling**: The `output_scaling` issue is noted as a potential adjustment point. If `3.0` was intentional, update `neuron.py`’s `configure_properties` for "motor" in "brainstem" (e.g., `self.output_scaling = 3.0`).

Save this as `README.md` in your `S.I.M.O.N` directory, and you should be ready to continue the project elsewhere. Let me know if you need help with specific sections or further refinements!

