import numpy as np
from src.neuron import GeneralizedNeuron

class NeuralNetwork:
    def __init__(self, num_neurons, num_inputs_per_neuron, neuron_types=None, region="cortex"):
        np.random.seed(42)  # Fixed seed for consistency
        if neuron_types is None:
            neuron_types = ["pyramidal"] * int(0.8 * num_neurons) + ["interneuron"] * int(0.2 * num_neurons)
        if len(neuron_types) != num_neurons:
            raise ValueError("Number of neuron types must match num_neurons")
        self.num_neurons = num_neurons
        self.num_inputs_per_neuron = num_inputs_per_neuron
        self.neurons = [
            GeneralizedNeuron(num_inputs_per_neuron + num_neurons, neuron_type, region, time_step=0.5)
            for neuron_type in neuron_types
        ]
        self.external_connectivity = np.random.rand(num_neurons, num_inputs_per_neuron)
        self.external_connectivity = self.external_connectivity * (np.random.rand(num_neurons, num_inputs_per_neuron) < 0.85) * 80.0
        for i in range(num_neurons):
            norm = np.linalg.norm(self.external_connectivity[i])
            if norm > 0:
                self.external_connectivity[i] *= 80.0 / norm
        self.recurrent_connectivity = np.random.rand(num_neurons, num_neurons)
        self.recurrent_connectivity = self.recurrent_connectivity * (np.random.rand(num_neurons, num_neurons) < 0.9) * 80.0
        np.fill_diagonal(self.recurrent_connectivity, 0)
        for i in range(num_neurons):
            norm = np.linalg.norm(self.recurrent_connectivity[i])
            if norm > 0:
                self.recurrent_connectivity[i] *= 80.0 / norm
        for i, neuron in enumerate(self.neurons):
            if not neuron.is_excitatory:
                self.external_connectivity[i] *= -0.3
                self.recurrent_connectivity[i] *= -0.3
            if i == 6:  # Adjust Neuron 6
                neuron.bias += 50.0  # Boost activation
                neuron.threshold = -70.0  # Lower threshold

    def forward(self, inputs, previous_outputs=None):
        if previous_outputs is None:
            previous_outputs = np.zeros(self.num_neurons)
        outputs = np.zeros(self.num_neurons)
        recurrent_inputs = np.dot(self.recurrent_connectivity, previous_outputs)
        for i, neuron in enumerate(self.neurons):
            external = self.external_connectivity[i] * inputs
            neuron_inputs = np.concatenate([external, recurrent_inputs])
            outputs[i] = neuron.forward(neuron_inputs)
            state = neuron.get_state()
            print(f"Neuron {i}: Current={np.sum(neuron_inputs):.2f}, Potential={state['membrane_potential']:.2f}, Spike={outputs[i]}")
        return outputs

    def get_state(self):
        return [neuron.get_state() for neuron in self.neurons]

    def simulate_network():
        pass

if __name__ == "__main__":
    np.random.seed(42)  # Fixed seed
    network = NeuralNetwork(num_neurons=10, num_inputs_per_neuron=5)
    time_steps = 40
    outputs = np.zeros(network.num_neurons)
    for t in range(time_steps):
        base_inputs = np.array([100.0, 50.0, -20.0, 80.0, 30.0])
        inputs = base_inputs + np.random.randn(5) * 100.0  # Increased noise to 100.0
        outputs = network.forward(inputs, outputs)
        print(f"Step {t}: {outputs}")
    print(f"Final: {outputs}")
    simulate_network()