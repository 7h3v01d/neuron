import numpy as np
import random
from datetime import datetime

class GeneralizedNeuron:
    def __init__(self, num_inputs, neuron_type="generic", region="cortex", time_step=0.5):
        self.num_inputs = num_inputs
        self.neuron_type = neuron_type.lower()
        self.region = region.lower()
        self.time_step = time_step
        self.weights = np.random.randn(num_inputs) * 0.3
        self.bias = np.random.randn() * 0.2
        self.rest_potential = -70.0
        self.membrane_potential = self.rest_potential
        self.threshold = -65.0
        self.base_threshold = -65.0
        self.reset_potential = -80.0
        self.leak_conductance = 0.02
        self.refractory_period = 0.15
        self.refractory_time = 0.0
        self.spike = 0
        self.burst_count = 0
        self.max_bursts = 3
        self.min_potential = -85.0
        self.adaptation_current = 0.0
        self.adaptation_strength = 0.0006
        self.adaptation_decay = 0.8
        self.dendritic_split = 0.7
        self.proximal_weights = self.weights[:int(num_inputs * self.dendritic_split)]
        self.distal_weights = self.weights[int(num_inputs * self.dendritic_split):]
        self.distal_attenuation = 0.5
        self.stdp_window = 20.0
        self.stdp_A_plus = 0.015
        self.stdp_A_minus = 0.012
        self.pre_spike_times = [[] for _ in range(num_inputs)]
        self.post_spike_times = []
        self.max_weight = 0.6
        self.min_weight = -0.6
        self.input_history = []
        self.max_history = 5
        self.output_scaling = 1.0

        if self.neuron_type == "interneuron" or self.neuron_type == "purkinje":
            self.is_excitatory = False
        else:
            self.is_excitatory = True

        self.configure_properties()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initialized {self.neuron_type} with is_excitatory={self.is_excitatory}")

    def configure_properties(self):
        if self.neuron_type == "pyramidal":
            self.base_threshold = -58.0
            self.threshold = -58.0
            self.leak_conductance = 0.02
            self.refractory_period = 0.15
            self.adaptation_strength = 0.0006
        elif self.neuron_type == "interneuron":
            self.base_threshold = -65.0
            self.threshold = -65.0
            self.leak_conductance = 0.04
            self.refractory_period = 0.15
            self.adaptation_strength = 0.0006
            self.is_excitatory = False
        elif self.neuron_type == "purkinje":
            self.base_threshold = -50.0
            self.threshold = -50.0
            self.is_excitatory = False
            if self.region == "cerebellum":
                self.threshold = -45.0
        elif self.neuron_type == "sensory":
            self.base_threshold = -65.0
            self.threshold = -65.0
        elif self.neuron_type == "motor":
            if self.region == "brainstem":
                self.output_scaling = 2.0 * 1.5

        if self.region == "cortex" and self.neuron_type == "pyramidal":
            self.bias = 180.0
        elif self.neuron_type == "interneuron":
            self.bias = 0.0

    def forward(self, inputs):
        if len(inputs) != self.num_inputs:
            raise ValueError("Number of inputs must match number of weights")
        inputs = np.array(inputs)
        current_time = len(self.input_history) * self.time_step
        self.input_history.append(inputs)
        if len(self.input_history) > self.max_history:
            self.input_history.pop(0)
        for i in range(self.num_inputs):
            if inputs[i] > 0.5:
                self.pre_spike_times[i].append(current_time)
            self.pre_spike_times[i] = [t for t in self.pre_spike_times[i] if current_time - t < self.stdp_window]
        self.adapt_behavior(inputs)
        self.refractory_time = max(0, self.refractory_time - self.time_step)
        self.adaptation_current *= np.exp(-self.adaptation_decay * self.time_step)
        if self.refractory_time <= 0 and self.membrane_potential >= self.threshold:
            self.spike = 1
            self.membrane_potential = self.reset_potential
            self.refractory_time = self.refractory_period
            self.adaptation_current += self.adaptation_strength
            self.post_spike_times.append(current_time)
            if self.neuron_type == "pyramidal" and self.burst_count < self.max_bursts:
                self.burst_count += 1
                self.refractory_time = self.refractory_period / 2
            self.update_weights(inputs)
            output_value = self.output_scaling
        else:
            self.spike = 0
            self.burst_count = 0
            output_value = 0.0
        self.post_spike_times = [t for t in self.post_spike_times if current_time - t < self.stdp_window]
        if self.is_excitatory:
            return self.spike * output_value
        else:
            return self.spike * -output_value

    def adapt_behavior(self, inputs):
        if self.neuron_type == "sensory":
            if len(self.input_history) > 1:
                input_variance = np.var(np.vstack(self.input_history), axis=0).mean()
                if input_variance > 0.5:
                    self.threshold = max(-70.0, self.threshold - 2.0)
                else:
                    self.threshold = min(self.threshold + 2.0, self.base_threshold + 10.0)
        if self.neuron_type == "interneuron":
            if np.mean(inputs) > 0.5:
                self.is_excitatory = False
            else:
                self.is_excitatory = True

    def update_weights(self, inputs):
        current_time = len(self.input_history) * self.time_step
        for i in range(self.num_inputs):
            delta_w = 0.0
            for pre_t in self.pre_spike_times[i]:
                for post_t in self.post_spike_times:
                    dt = post_t - pre_t
                    if dt > 0 and dt <= self.stdp_window:
                        delta_w += self.stdp_A_plus * np.exp(-dt / self.stdp_window)
                    elif dt < 0 and abs(dt) <= self.stdp_window:
                        delta_w -= self.stdp_A_minus * np.exp(dt / self.stdp_window)
            new_weight = np.clip(self.weights[i] + delta_w, self.min_weight, self.max_weight)
            self.weights[i] = new_weight
            if i < len(self.proximal_weights):
                self.proximal_weights[i] = new_weight
            else:
                self.distal_weights[i - len(self.proximal_weights)] = new_weight

    def get_state(self):
        return {
            "neuron_type": self.neuron_type,
            "region": self.region,
            "weights": self.weights.tolist(),
            "bias": self.bias,
            "membrane_potential": self.membrane_potential,
            "spike": self.spike,
            "is_excitatory": self.is_excitatory,
            "threshold": self.threshold,
            "refractory_time": self.refractory_time,
            "output_scaling": self.output_scaling,
            "burst_count": self.burst_count,
            "adaptation_current": self.adaptation_current
        }