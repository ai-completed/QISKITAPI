# Author: Jacob Thomas (Messer) Redmond
# Tustin, CA
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

from flask import Flask, jsonify, request, render_template, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sslify import SSLify
from qiskit import execute, Aer
from authentication import authenticate_user
from utilities import handle_error, validate_input, sanitize_parameter
import logging
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Enforce SSL/TLS
sslify = SSLify(app)

# Setup rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
logging.basicConfig(filename='web_interface.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    # Serve the main HTML page
    return render_template('index.html')

@app.route('/api/v1/execute', methods=['POST'])
@limiter.limit("10 per minute")
def execute_quantum_circuit():
    # Authenticate the user
    auth_header = request.headers.get('Authorization')
    if not auth_header or not authenticate_user(auth_header):
        return jsonify({"error": "Unauthorized"}), 401

    # Validate and sanitize input
    circuit_data = request.json.get('circuit')
    if not validate_input(circuit_data, dict):
        return jsonify({"error": "Invalid circuit data"}), 400
    sanitized_circuit_data = sanitize_parameter(circuit_data)

    # Create a quantum circuit from the sanitized input data
    # Placeholder: Convert the sanitized_circuit_data into a Qiskit QuantumCircuit object
    # circuit = convert_to_qiskit_circuit(sanitized_circuit_data)

    try:
        # Execute the quantum circuit
        backend = Aer.get_backend('qasm_simulator')
        job = execute(circuit, backend)
        result = job.result().get_counts(circuit)
        return jsonify(result)
    except Exception as e:
        handle_error(f"Quantum execution error: {e}", raise_exception=False)
        return jsonify({"error": "Internal server error"}), 500

def start_web_server():
    # Configure the Flask web server
    app.run(host='0.0.0.0', port=443, debug=True)

if __name__ == '__main__':
    start_web_server()
