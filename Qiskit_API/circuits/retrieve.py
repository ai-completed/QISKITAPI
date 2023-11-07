import json
from qiskit import available_backends, get_backend, IBMQ
from qiskit.providers.ibmq.exceptions import IBMQAccountError, IBMQBackendError

def list_available_backends():
    """
    List all available quantum circuit backends using Qiskit.

    Returns:
        list: A list of available backend names.
    """
    return [backend.name() for backend in available_backends()]

def retrieve_backend_info(backend_name):
    """
    Retrieve information about a specific quantum circuit backend using Qiskit.

    Args:
        backend_name (str): Name of the backend to retrieve information about.

    Returns:
        dict: Information about the specified backend, including its name, status, configuration, and properties.
              Returns None if the backend does not exist.
    """
    try:
        backend = get_backend(backend_name)
        backend_info = {
            "name": backend.name(),
            "status": backend.status().to_dict(),
            "configuration": backend.configuration().to_dict(),
            "properties": backend.properties().to_dict(),
        }
        return backend_info
    except IBMQBackendError as e:
        print(f"IBM Quantum Experience Backend Error: {str(e)}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

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
        print(f"IBM Quantum Experience Account Error: {str(e)}")
        return []

def retrieve_ibmq_account_info(provider_name):
    """
    Retrieve information about a specific IBM Quantum Experience provider.

    Args:
        provider_name (str): Name of the IBM Quantum Experience provider to retrieve information about.

    Returns:
        dict: Information about the specified provider, including its name and status.
              Returns None if the provider does not exist.
    """
    try:
        provider = IBMQ.get_provider(hub=provider_name)
        provider_info = {
            "name": provider.credentials.hub,
            "status": provider.status().to_dict(),
        }
        return provider_info
    except IBMQAccountError as e:
        print(f"IBM Quantum Experience Account Error: {str(e)}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def export_to_json(data, filename):
    """
    Export data to a JSON file.

    Args:
        data (dict): Data to be exported.
        filename (str): Name of the JSON file to save.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    """
    Main function to retrieve information about quantum circuit backends and IBM Quantum Experience accounts.
    """
    try:
        print("Listing available quantum circuit backends:")
        available_backends_list = list_available_backends()

        if available_backends_list:
            for idx, backend_name in enumerate(available_backends_list):
                print(f"{idx + 1}. {backend_name}")

            selected_idx = input("Enter the number of the backend you want to retrieve information about (or 0 to exit): ")

            if selected_idx.isdigit():
                selected_idx = int(selected_idx)
                if 0 <= selected_idx <= len(available_backends_list):
                    if selected_idx == 0:
                        print("Exiting the program.")
                        return

                    selected_backend_name = available_backends_list[selected_idx - 1]
                    backend_info = retrieve_backend_info(selected_backend_name)

                    if backend_info:
                        print(f"Backend: {backend_info['name']}")
                        print(f"Status: {backend_info['status']['status']}")
                        print(f"Configuration: {backend_info['configuration']['n_qubits']} qubits")
                        print(f"Properties: {backend_info['properties']['total_qubits']} qubits, {backend_info['properties']['gates']} gates")

                        export_option = input("Do you want to export this information to a JSON file? (yes/no): ").strip().lower()
                        if export_option == "yes":
                            json_filename = input("Enter the name of the JSON file (e.g., backend_info.json): ").strip()
                            export_to_json(backend_info, json_filename)
                            print(f"Backend information exported to {json_filename}")
                    else:
                        print("Backend not found.")
                else:
                    print("Invalid selection. Please enter a valid number.")
            else:
                print("Invalid input. Please enter a number.")
        else:
            print("No quantum circuit backends available.")

        print("\nListing available IBM Quantum Experience accounts:")
        ibmq_accounts = list_ibmq_accounts()

        if ibmq_accounts:
            for idx, provider in enumerate(ibmq_accounts):
                print(f"{idx + 1}. {provider.credentials.hub}")

            selected_idx = input("Enter the number of the IBM Quantum Experience account you want to retrieve information about (or 0 to exit): ")

            if selected_idx.isdigit():
                selected_idx = int(selected_idx)
                if 0 <= selected_idx <= len(ibmq_accounts):
                    if selected_idx == 0:
                        print("Exiting the program.")
                        return

                    selected_provider_name = ibmq_accounts[selected_idx - 1].credentials.hub
                    provider_info = retrieve_ibmq_account_info(selected_provider_name)

                    if provider_info:
                        print(f"Provider: {provider_info['name']}")
                        print(f"Status: {provider_info['status']['status']}")

                        export_option = input("Do you want to export this information to a JSON file? (yes/no): ").strip().lower()
                        if export_option == "yes":
                            json_filename = input("Enter the name of the JSON file (e.g., provider_info.json): ").strip()
                            export_to_json(provider_info, json_filename)
                            print(f"Provider information exported to {json_filename}")
                    else:
                        print("Provider not found.")
                else:
                    print("Invalid selection. Please enter a valid number.")
            else:
                print("Invalid input. Please enter a number.")
        else:
            print("No IBM Quantum Experience accounts loaded.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
