import threading
from flask import Flask, jsonify
from web3 import Web3
import time

# Flask app setup
app = Flask(__name__)

# Initialize Web3 with the Polygon Mumbai RPC URL
w3 = Web3(Web3.HTTPProvider("https://bnb-mainnet.g.alchemy.com/v2/K-g36Q6qB-7NsX2OB5FcTs1Ok3i6ycAE"))

# Replace these with your actual private key and public key
private_key = 'de15d2f43192f331d7678c0ffa1a271308924ae60661f4bcc055a0179588a8d2'  # Replace with environment variables for security
pub_key = "0xA9BAF7e3B6A21E24E5450E23C921e60F5F1B99A4"
recipient_pub_key = "0x9BAbf3490ee292bAbFCcf6DF26475108D88eDfb2"

# Shared state for balance and transaction hash
state = {
    "balance": 0,
    "last_transaction_hash": None,
    "error": None
}

def loop():
    while True:
        try:
            # Check if Web3 is connected
            if not w3.is_connected():
                state["error"] = "Web3 is not connected to the network."
                break  # Exit the loop if the network is not connected

            # Get balance in wei (smallest unit of Ethereum/MATIC)
            balance = w3.eth.get_balance(pub_key)
            balance_in_ether = w3.from_wei(balance, 'ether')
            state["balance"] = balance_in_ether  # Update the state
            print(f"Balance: {balance_in_ether} BNB")
            
            # Fetch current gas price from the network
            gas_price = w3.eth.gas_price  # Get the current gas price in wei
            gas_limit = 21000  # Gas limit for a basic transaction (simple transfer)
            gas_cost = gas_limit * gas_price  # Total cost of gas in wei
            
            if balance > gas_cost:
                nonce = w3.eth.get_transaction_count(pub_key)  # Get the next available nonce

                # Construct the transaction object
                tx = {
                    'chainId': 56,  # Mumbai Testnet
                    'nonce': nonce,    # Dynamic nonce based on the transaction count
                    'to': recipient_pub_key,
                    'value': balance - gas_cost,  # Send all balance except for gas
                    'gas': gas_limit,
                    'gasPrice': gas_price
                }

                # Ensure private key is valid
                if private_key:
                    try:
                        # Sign the transaction
                        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
                        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                        state["last_transaction_hash"] = w3.to_hex(tx_hash)  # Update the state
                        print(f"Transaction Hash: {state['last_transaction_hash']}")
                    except Exception as e:
                        state["error"] = f"Error signing or sending transaction: {e}"
                        print(state["error"])
                else:
                    state["error"] = "Missing private key."
            
        except Exception as e:
            state["error"] = f"Error: {e}"
            print(state["error"])

        # Sleep for 5 seconds before checking balance again
        time.sleep(2)

# Flask route to get the current state
@app.route("/")
def index():
    return jsonify(state)

# Start the Web3 loop in a separate thread
threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    # Start the Flask app on the specified port
    app.run(host="0.0.0.0", port=5000)
