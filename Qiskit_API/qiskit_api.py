# Author: Jacob Thomas (Legally Messer) Redmond
# Tustin, CA: Please send help and Arrest Gary Messer 
# MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ
from qiskit.visualization import plot_histogram
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.providers.aer import noise
from .authentication import authenticate_user
from .utilities import handle_error

def create_quantum_circuit(qubits, name="QuantumCircuit", parameterized=False):
    """
    Creates a quantum circuit with the given number of qubits and an optional name.
    Can also create a parameterized circuit for use in variational algorithms.

    Parameters:
        qubits (int): Number of qubits for the circuit.
        name (str): Name for the circuit.
        parameterized (bool): Flag to create a parameterized circuit.

    Returns:
        QuantumCircuit: A new or parameterized QuantumCircuit object.
    """
    if qubits <= 0:
        raise ValueError("Number of qubits must be a positive integer")
    circuit = QuantumCircuit(qubits, qubits, name=name)  # Create a circuit with classical bits equal to qubits for measurement
    if parameterized:
        # Add a parameterized gate or operation here
        pass
    return circuit

def run_quantum_circuit(circuit, backend_name='qasm_simulator', shots=1024, token=None, async_mode=False):
    """
    Executes the given quantum circuit on the specified backend. Can run in asynchronous mode.

    Parameters:
        circuit (QuantumCircuit): The quantum circuit to run.
        backend_name (str): The name of the backend to run the circuit on.
        shots (int): The number of times to run the circuit.
        token (str): IBMQ token for accessing IBMQ backends.
        async_mode (bool): Run in asynchronous mode.

    Returns:
        dict or Job: The result counts or a Job object for the execution.
    """
    try:
        if token:
            # Authenticate the user with the provided token
            authenticate_user(token)
            IBMQ.load_account()
            provider = IBMQ.get_provider(hub='ibm-q')
            backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= circuit.num_qubits and
                                                not x.configuration().simulator and x.status().operational==True))
        else:
            backend = Aer.get_backend(backend_name)

        # Transpile the circuit for the backend
        transpiled_circuit = transpile(circuit, backend)
        qobj = assemble(transpiled_circuit, backend, shots=shots)

        if async_mode:
            # Return the job for asynchronous handling
            return backend.run(qobj)
        else:
            # Execute the circuit synchronously
            job = backend.run(qobj)
            job_monitor(job)  # Optional: monitor the job's execution
            results = job.result().get_counts(circuit)
            return results
    except Exception as e:
        handle_error(f"Error during quantum circuit execution: {e}", raise_exception=True)

def visualize_circuit(circuit):
    """
    Generates a visualization for the provided quantum circuit.

    Parameters:
        circuit (QuantumCircuit): The quantum circuit to visualize.

    Returns:
        Figure: A matplotlib figure representing the circuit.
    """
    return circuit.draw(output='mpl')

def visualize_results(results):
    """
    Generates a histogram visualization for the results of a quantum circuit execution.

    Parameters:
        results (dict): The result counts from the circuit execution.

    Returns:
        Figure: A matplotlib figure representing the histogram of results.
    """
    return plot_histogram(results)

# Additional functions for error mitigation, backend recommendations, etc., can be implemented here.
