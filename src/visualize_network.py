import numpy as np
import matplotlib.pyplot as plt
from src.network import NeuralNetwork

def visualize_network():
    np.random.seed(0)
    network = NeuralNetwork(num_neurons=10, num_inputs_per_neuron=5)
    time_steps = 40
    outputs = np.zeros(network.num_neurons)
    potentials = np.zeros((time_steps, network.num_neurons))
    spikes = np.zeros((time_steps, network.num_neurons))
    
    for t in range(time_steps):
        base_inputs = np.array([100.0, 50.0, -20.0, 80.0, 30.0])
        inputs = base_inputs * (1 + 0.2 * np.sin(t * 0.5)) + np.random.randn(5) * 20.0
        outputs = network.forward(inputs, outputs)
        potentials[t] = [neuron.get_state()['membrane_potential'] for neuron in network.neurons]
        spikes[t] = outputs
    
    # Plot membrane potentials
    plt.figure(figsize=(12, 6))
    for i in range(network.num_neurons):
        plt.plot(potentials[:, i], label=f'Neuron {i}')
    plt.title("Membrane Potentials Over Time")
    plt.xlabel("Time Step (0.5 ms)")
    plt.ylabel("Membrane Potential (mV)")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Plot spike counts
    spike_counts = np.sum(spikes != 0, axis=0)
    plt.figure(figsize=(12, 6))
    plt.bar(range(network.num_neurons), spike_counts, color='skyblue')
    plt.title("Spike Counts per Neuron")
    plt.xlabel("Neuron Index")
    plt.ylabel("Number of Spikes")
    plt.grid(True, axis='y')
    plt.show()

if __name__ == "__main__":
    visualize_network()