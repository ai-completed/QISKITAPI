from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Instruction, transpile, Aer, execute, qasm
import json

class QuantumCircuitBuilder:
    """
    QuantumCircuitBuilder class for constructing quantum circuits.

    Attributes:
        num_qubits (int): Number of qubits in the circuit.
        name (str): Name of the circuit.
        qregs (list): List of QuantumRegister objects.
        cregs (list): List of ClassicalRegister objects.
        circuit (QuantumCircuit): The quantum circuit being built.
    """

    def __init__(self, num_qubits=1, name="my_circuit"):
        """
        Initialize a QuantumCircuitBuilder instance.

        Args:
            num_qubits (int): Number of qubits in the circuit (default is 1).
            name (str): Name of the circuit (default is "my_circuit").
        """
        self.num_qubits = num_qubits
        self.name = name
        self.qregs = [QuantumRegister(num_qubits, f"q{i}") for i in range(num_qubits)]
        self.cregs = [ClassicalRegister(num_qubits, f"c{i}") for i in range(num_qubits)]
        self.circuit = QuantumCircuit(*self.qregs, *self.cregs, name=name)

    def add_hadamard(self, target_qubit):
        """
        Add a Hadamard gate to the circuit.

        Args:
            target_qubit (int): Index of the target qubit.
        """
        self.circuit.h(self.qregs[target_qubit])

    def add_cnot(self, control_qubit, target_qubit):
        """
        Add a CNOT gate to the circuit.

        Args:
            control_qubit (int): Index of the control qubit.
            target_qubit (int): Index of the target qubit.
        """
        self.circuit.cx(self.qregs[control_qubit], self.qregs[target_qubit])

    def add_measurement(self, qubit, bit):
        """
        Add a measurement operation to the circuit.

        Args:
            qubit (int): Index of the qubit to measure.
            bit (int): Index of the classical bit to store the measurement result.
        """
        self.circuit.measure(self.qregs[qubit], self.cregs[bit])

    def add_custom_gate(self, gate_name, qubits, parameters=None, condition_bits=None, condition_values=None):
        """
        Add a custom gate to the circuit.

        Args:
            gate_name (str): Name of the custom gate.
            qubits (list): List of qubit indices the gate acts on.
            parameters (list, optional): List of gate parameters (default is None).
            condition_bits (list, optional): List of condition qubit indices (default is None).
            condition_values (list, optional): List of condition values (default is None).
        """
        if parameters is None:
            parameters = []
        if condition_bits is None:
            condition_bits = []
        if condition_values is None:
            condition_values = []

        custom_gate = Instruction(gate_name, len(qubits), len(condition_bits), parameters, condition_bits, condition_values)
        self.circuit.append(custom_gate, qubits)

    def build(self):
        """
        Build and return the quantum circuit.

        Returns:
            QuantumCircuit: The constructed quantum circuit.
        """
        return self.circuit

    def export_to_qasm(self, filename):
        """
        Export the quantum circuit to a QASM file.

        Args:
            filename (str): Name of the QASM file to save.
        """
        qasm_str = qasm(self.circuit)
        with open(filename, 'w') as file:
            file.write(qasm_str)

    def export_to_json(self, filename):
        """
        Export the quantum circuit to a JSON file.

        Args:
            filename (str): Name of the JSON file to save.
        """
        circuit_dict = self.circuit.data(1)
        with open(filename, 'w') as file:
            json.dump(circuit_dict, file, indent=4)

def create_custom_circuit():
    """
    Create a custom quantum circuit.

    Returns:
        QuantumCircuit: The custom quantum circuit.
    """
    builder = QuantumCircuitBuilder(num_qubits=3, name="custom_circuit")
    
    # Build the circuit using high-level instructions
    builder.add_hadamard(0)
    builder.add_cnot(0, 1)
    builder.add_measurement(1, 1)
    
    # Add a custom gate with parameters and conditions
    builder.add_custom_gate("custom_gate", qubits=[0, 2], parameters=[1.57], condition_bits=[0], condition_values=[0])
    
    return builder.build()

def main():
    """
    Main function to demonstrate the usage of the script.
    """
    # Example usage:
    custom_circuit = create_custom_circuit()

    if custom_circuit:
        # Export the circuit to QASM and JSON formats
        custom_circuit.export_to_qasm("custom_circuit.qasm")
        custom_circuit.export_to_json("custom_circuit.json")

        print("Circuit exported to QASM and JSON files.")
    else:
        print("Circuit creation failed. Please handle the error accordingly.")

if __name__ == "__main__":
    main()
