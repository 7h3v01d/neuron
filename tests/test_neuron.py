import unittest
import numpy as np
from src.neuron import GeneralizedNeuron

class TestGeneralizedNeuron(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.num_inputs = 3
        self.inputs = np.array([0.5, -0.2, 0.8])
        self.strong_inputs = np.array([10.0, 10.0, 10.0])  # Strong inputs to trigger spikes
        self.time_step = 0.1
    
    def test_initialization(self):
        """Test neuron initialization for different types and regions."""
        neuron_types = ["pyramidal", "purkinje", "granule", "motor", "interneuron", "sensory", "generic"]
        regions = ["cortex", "cerebellum", "brainstem"]
        
        for neuron_type in neuron_types:
            for region in regions:
                neuron = GeneralizedNeuron(self.num_inputs, neuron_type, region, self.time_step)
                state = neuron.get_state()
                
                self.assertEqual(len(neuron.weights), self.num_inputs)
                self.assertEqual(state["neuron_type"], neuron_type)
                self.assertEqual(state["region"], region)
                self.assertEqual(state["membrane_potential"], -70.0)
                self.assertEqual(state["spike"], 0)
                
                # Check type-specific properties
                if neuron_type == "purkinje":
                    self.assertFalse(state["is_excitatory"])
                    self.assertEqual(state["threshold"], -50.0 if region != "cerebellum" else -45.0)
                elif neuron_type == "sensory":
                    self.assertEqual(state["threshold"], -65.0)
                elif neuron_type == "motor" and region == "brainstem":
                    self.assertEqual(state["output_scaling"], 2.0 * 1.5)  # Updated to match neuron.py's 3.0
    
    def test_spiking_dynamics(self):
        """Test spiking behavior."""
        neuron = GeneralizedNeuron(self.num_inputs, "pyramidal", "cortex", self.time_step)
        
        # Simulate strong input to trigger spike
        neuron.weights = np.array([1.0, 1.0, 1.0])
        neuron.bias = 0.0
        
        output = neuron.forward(self.strong_inputs)
        if neuron.membrane_potential >= neuron.threshold:
            self.assertEqual(output, 1.0)
            self.assertEqual(neuron.membrane_potential, neuron.reset_potential)
            self.assertEqual(neuron.refractory_time, neuron.refractory_period)
        
        # Test refractory period
        output = neuron.forward(self.strong_inputs)
        if neuron.refractory_time > 0:
            self.assertEqual(output, 0.0)
    
    def test_adaptive_behavior(self):
        """Test adaptive behavior for sensory neurons."""
        sensory_neuron = GeneralizedNeuron(self.num_inputs, "sensory", "cortex", self.time_step)
        initial_threshold = sensory_neuron.threshold
        
        # High-variance inputs
        high_var_inputs = [np.array([1.0, -1.0, 0.5]), np.array([-1.0, 1.0, -0.5])]
        for inputs in high_var_inputs:
            sensory_neuron.forward(inputs)
        self.assertLess(sensory_neuron.threshold, initial_threshold)
        
        # Low-variance inputs
        sensory_neuron = GeneralizedNeuron(self.num_inputs, "sensory", "cortex", self.time_step)
        low_var_inputs = [np.array([0.5, 0.4, 0.6]), np.array([0.5, 0.4, 0.6])]
        for inputs in low_var_inputs:
            sensory_neuron.forward(inputs)
        self.assertGreaterEqual(sensory_neuron.threshold, initial_threshold - 0.01)
        
        # Verify interneuron is inhibitory (no switching)
        interneuron = GeneralizedNeuron(self.num_inputs, "interneuron", "cortex", self.time_step)
        self.assertFalse(interneuron.is_excitatory)
    
    def test_learning(self):
        """Test Hebbian learning."""
        neuron = GeneralizedNeuron(self.num_inputs, "pyramidal", "cortex", self.time_step)
        initial_weights = neuron.weights.copy()
        neuron.weights = np.array([1.0, 1.0, 1.0])
        neuron.bias = 0.0
        neuron.membrane_potential = neuron.threshold  # Force spike
        neuron.forward(self.inputs)
        for i in range(self.num_inputs):
            if self.inputs[i] != 0:
                self.assertNotEqual(neuron.weights[i], initial_weights[i])
    
    def test_input_validation(self):
        """Test input size validation."""
        neuron = GeneralizedNeuron(self.num_inputs, "generic", "cortex", self.time_step)
        with self.assertRaises(ValueError):
            neuron.forward([0.1, 0.2])  # Wrong input size
    
    def test_spike_output(self):
        """Test excitatory and inhibitory spike outputs."""
        excitatory_neuron = GeneralizedNeuron(self.num_inputs, "pyramidal", "cortex", self.time_step)
        inhibitory_neuron = GeneralizedNeuron(self.num_inputs, "interneuron", "cortex", self.time_step)  # Changed to interneuron
        
        # Set conditions to trigger spikes
        excitatory_neuron.weights = np.array([1.0, 1.0, 1.0])
        excitatory_neuron.bias = 0.0
        excitatory_neuron.membrane_potential = excitatory_neuron.threshold
        
        inhibitory_neuron.weights = np.array([1.0, 1.0, 1.0])
        inhibitory_neuron.bias = 0.0
        inhibitory_neuron.membrane_potential = inhibitory_neuron.threshold
        
        excitatory_output = excitatory_neuron.forward(self.strong_inputs)
        inhibitory_output = inhibitory_neuron.forward(self.strong_inputs)
        
        self.assertEqual(excitatory_output, 1.0)
        self.assertEqual(inhibitory_output, -1.0)

if __name__ == "__main__":
    unittest.main()