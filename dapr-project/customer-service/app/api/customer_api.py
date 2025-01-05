from dapr.clients import DaprClient
from flask import Flask, Blueprint, request, jsonify

# Create a Blueprint for the customer service
customer_blueprint = Blueprint('customer', __name__)

# Initialize the Dapr client
client = DaprClient()

# Add a new customer to the database using Dapr binding
@customer_blueprint.route('/customer', methods=['POST'])
def add_customer():
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields: 'name' and 'email'"}), 400

    # Prepare the SQL query for inserting the customer
    sql = f"INSERT INTO customers (name, email) VALUES ('{data['name']}', '{data['email']}') RETURNING id"

    try:
        # Use the Dapr client to invoke the 'postgres-binding' with 'exec' operation
        response = client.invoke_binding(
            binding_name="postgres-binding",  # The binding name defined in Dapr component
            operation="exec",  # Operation type (exec for executing SQL)
            data=sql,  # SQL query passed as string data
            binding_metadata={"sql": sql}  # Pass SQL query as binding metadata
        )

        # Inspect the response to see if it contains the expected values
        print("Response from Dapr:", response)
        return jsonify({"status": "Customer added"}), 201
    except Exception as e:
        # Handle any exceptions that occur
        return jsonify({"error": "Request to Dapr failed", "details": str(e)}), 500

# Get a customer by ID using Dapr binding
@customer_blueprint.route('/customer/get/<int:id>', methods=['GET'])
def get_customer(id):
    sql = f"SELECT id, name, email FROM customers WHERE id = {id}"

    try:
        # Use the Dapr client to invoke the 'postgres-binding' with 'query' operation
        response = client.invoke_binding(
            binding_name="postgres-binding",  # The binding name defined in Dapr component
            operation="query",  # Operation type (query for querying data)
            data=sql,  # SQL query passed as string data
            binding_metadata={"sql": sql}  # Pass SQL query as binding metadata
        )

        # Inspect the response to see if it contains the expected values
        print("Response from Dapr:", response)

        if response.data:
            customer_data = response.data.decode("utf-8")  # Decode response data
            return jsonify({"customer": customer_data}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        # Handle any exceptions
        return jsonify({"error": "Request to Dapr failed", "details": str(e)}), 500

# Update a customer by ID using Dapr binding
@customer_blueprint.route('/customer/update/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields: 'name' and 'email'"}), 400

    sql = f"UPDATE customers SET name = '{data['name']}', email = '{data['email']}' WHERE id = {id}"

    try:
        # Use the Dapr client to invoke the 'postgres-binding' with 'exec' operation
        response = client.invoke_binding(
            binding_name="postgres-binding",  # The binding name defined in Dapr component
            operation="exec",  # Operation type (exec for executing SQL)
            data=sql,  # SQL query passed as string data
            binding_metadata={"sql": sql}  # Pass SQL query as binding metadata
        )

        return jsonify({"status": "Customer updated"}), 200
    except Exception as e:
        # Handle any exceptions
        return jsonify({"error": "Request to Dapr failed", "details": str(e)}), 500
    
# Delete a customer by ID using Dapr binding
@customer_blueprint.route('/customer/delete/<int:id>', methods=['DELETE'])
def delete_customer(id):
    sql = f"DELETE FROM customers WHERE id = {id}"

    try:
        # Use the Dapr client to invoke the 'postgres-binding' with 'exec' operation
        response = client.invoke_binding(
            binding_name="postgres-binding",  # The binding name defined in Dapr component
            operation="exec",  # Operation type (exec for executing SQL)
            data=sql,  # SQL query passed as string data
            binding_metadata={"sql": sql}  # Pass SQL query as binding metadata
        )

        return jsonify({"status": "Customer deleted"}), 204
    except Exception as e:
        # Handle any exceptions
        return jsonify({"error": "Request to Dapr failed", "details": str(e)}), 500