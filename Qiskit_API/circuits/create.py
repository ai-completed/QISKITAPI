from qiskit import QuantumCircuit, transpile
from qiskit.providers import JobStatus
from qiskit.visualization import circuit_drawer

class QiskitAPIWrapper:
    def __init__(self, provider):
        self.provider = provider

    def create_circuit(self, num_qubits=1):
        """
        Create a quantum circuit with the specified number of qubits.

        Args:
            num_qubits (int): Number of qubits in the circuit.

        Returns:
            QuantumCircuit: A quantum circuit object.
        """
        return QuantumCircuit(num_qubits)

    def transpile_circuit(self, circuit, backend):
        """
        Transpile a quantum circuit for a specific backend.

        Args:
            circuit (QuantumCircuit): The quantum circuit to transpile.
            backend (str): The target backend for transpilation.

        Returns:
            QuantumCircuit: The transpiled quantum circuit.
        """
        transpiled_circuit = transpile(circuit, backend=backend, optimization_level=3)
        return transpiled_circuit

    def visualize_circuit(self, circuit):
        """
        Visualize a quantum circuit.

        Args:
            circuit (QuantumCircuit): The quantum circuit to visualize.
        """
        circuit_drawer(circuit, output="mpl")

    def run_job(self, circuit, backend, shots=1024):
        """
        Run a quantum circuit on a specified backend.

        Args:
            circuit (QuantumCircuit): The quantum circuit to run.
            backend (str): The target backend for execution.
            shots (int): The number of measurement shots.

        Returns:
            Job: A Qiskit job object.
        """
        job = self.provider.run(circuit, backend, shots=shots)
        return job

    def get_job_status(self, job):
        """
        Get the status of a job.

        Args:
            job (Job): A Qiskit job object.

        Returns:
            JobStatus: The status of the job.
        """
        return job.status()

    def get_job_result(self, job):
        """
        Get the result of a completed job.

        Args:
            job (Job): A completed Qiskit job object.

        Returns:
            Result: The result of the job.
        """
        return job.result()
