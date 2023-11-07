from qiskit import available_backends, get_backend, IBMQ
from qiskit.providers.ibmq.exceptions import IBMQAccountError

def list_quantum_circuits(backend_name=None):
    """
    List the available quantum circuits using Qiskit.

    Args:
        backend_name (str, optional): Name of the backend to list. If None, lists all available backends.

    Returns:
        list: A list of available quantum circuits (backend names and additional information).
    """
    if backend_name:
        backend = get_backend(backend_name)
        backend_info = {
            "name": backend.name(),
            "status": backend.status().to_dict(),
            "configuration": backend.configuration().to_dict(),
            "properties": backend.properties().to_dict(),
        }
        return [backend_info]
    else:
        return [
            {
                "name": backend.name(),
                "status": backend.status().to_dict(),
                "configuration": backend.configuration().to_dict(),
                "properties": backend.properties().to_dict(),
            }
            for backend in available_backends()
        ]

def list_ibmq_accounts():
    """
    List the available IBM Quantum Experience accounts.

    Returns:
        list: A list of IBM Quantum Experience account names.
    """
    try:
        IBMQ.load_account()
        return IBMQ.providers()
    except IBMQAccountError as e:
        return []

def main():
    """
    Main function to list available quantum circuits and IBM Quantum Experience accounts.
    """
    try:
        print("Listing available quantum circuits:")
        quantum_circuits = list_quantum_circuits()
        
        if quantum_circuits:
            for backend_info in quantum_circuits:
                print(f"Backend: {backend_info['name']}")
                print(f"Status: {backend_info['status']['status']}")
                print(f"Configuration: {backend_info['configuration']['n_qubits']} qubits")
                print(f"Properties: {backend_info['properties']['total_qubits']} qubits, {backend_info['properties']['gates']} gates")
                print()
        else:
            print("No quantum circuits available.")
        
        print("Listing available IBM Quantum Experience accounts:")
        ibmq_accounts = list_ibmq_accounts()
        
        if ibmq_accounts:
            for account in ibmq_accounts:
                print(account)
        else:
            print("No IBM Quantum Experience accounts loaded.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
