from src.visualize_network import visualize_network
from src.visualize_neuron import visualize_neuron

def main():
    print("Running network visualization...")
    visualize_network()
    
    print("\nRunning single neuron visualization...")
    visualize_neuron()

if __name__ == "__main__":
    main()