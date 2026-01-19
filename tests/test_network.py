import unittest
import numpy as np
from src.network import NeuralNetwork

class TestNeuralNetwork(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.network = NeuralNetwork(num_neurons=10, num_inputs_per_neuron=5)

    def test_initialization(self):
        self.assertEqual(len(self.network.neurons), 10)
        self.assertEqual(self.network.num_inputs_per_neuron, 5)
        self.assertEqual(self.network.external_connectivity.shape, (10, 5))
        self.assertEqual(self.network.recurrent_connectivity.shape, (10, 10))
        self.assertTrue(np.all(np.diag(self.network.recurrent_connectivity) == 0), "No self-connections")

    def test_forward_pass(self):
        inputs = np.array([100.0, 50.0, -20.0, 80.0, 30.0])
        outputs = self.network.forward(inputs)
        self.assertEqual(outputs.shape, (10,))
        self.assertTrue(np.all(np.isin(outputs, [-1, 0, 1])), "Outputs should be -1, 0, or 1")

    def test_spike_variability(self):
        time_steps = 20
        outputs = np.zeros(self.network.num_neurons)
        spike_counts = np.zeros(self.network.num_neurons)
        for t in range(time_steps):
            inputs = np.array([100.0, 50.0, -20.0, 80.0, 30.0]) + np.random.randn(5) * 60.0
            outputs = self.network.forward(inputs, outputs)
            spike_counts += (outputs != 0).astype(int)
        self.assertTrue(np.all(spike_counts >= 0), "Spike counts should be non-negative")
        self.assertTrue(np.std(spike_counts) > 1.0, "Spiking should vary across neurons")
        self.assertTrue(spike_counts[2] > 5, "Neuron 2 should spike early")
        self.assertTrue(spike_counts[3] > 5, "Neuron 3 should spike early")
        self.assertTrue(spike_counts[8] > 2, "Inhibitory neuron 8 should spike")

if __name__ == '__main__':
    unittest.main()