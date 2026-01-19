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

### 1. **Clone the repository**:
   ```bash
   git clone [neuron.git](https://github.com/7h3v01d/neuron.git)
```
```bash
   cd neuron
```
### 2. Create a virtual environment:

```Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install dependencies:
```Bash
pip install -r requirements.txt
```
---

### 📈 Usage
Run a Single Neuron Simulation
To see how a Pyramidal neuron responds to sustained input and how its weights adapt via STDP:

```Bash
python -m src.visualize_neuron
```
Run Network Simulation
To observe the interaction between excitatory and inhibitory neurons in a recurrent loop:

```Bash
python -m src.visualize_network
```
---

## 🔬 Research Objectives

This project aims to replicate specific biological benchmarks:

- Inhibitory Balance: Targeting ~20 inhibitory spikes for interneurons (Neuron 9) over a 40-step cycle.
- Rapid Response: Optimizing Neurons 2, 3, and 5 for early-onset spiking (within 4-5 steps).
- Regional Accuracy: Modeling the unique thresholding and scaling of brainstem motor neurons and cerebellar purkinje cells.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

*Inspired by research into digital brain architectures and human scientific discovery.*
