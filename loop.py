import threading
from web3 import Web3
import time

# Initialize Web3 with the Polygon Mumbai RPC URL
w3 = Web3(Web3.HTTPProvider("https://rpc.cardona.zkevm-rpc.com"))

# Replace these with your actual private key and public key
private_key = '3ddc37fdcd6ba99f9a16206467e459d4009ab30b3b4909a5ba0ca50ea40d2624'  # Replace with environment variables for security
pub_key = "0x242F5c9a1D42e962A1c6B479349FFAf188163757"
recipient_pub_key ="0x9BAbf3490ee292bAbFCcf6DF26475108D88eDfb2"

def loop():
    while True:
        try:
            # Check if Web3 is connected


            # Get balance in wei (smallest unit of Ethereum/MATIC)
            balance = w3.eth.get_balance(pub_key)
            balance_in_ether = w3.from_wei(balance, 'ether')
            print(f"{balance_in_ether}")

            # Fetch current gas price from the network
            gas_price = w3.eth.gas_price  # Get the current gas price in wei
            gas_limit = 21000  # Gas limit for a basic transaction (simple transfer)
            gas_cost = gas_limit * gas_price  # Total cost of gas in wei
            if balance > gas_cost:
                nonce = w3.eth.get_transaction_count(pub_key)  # Get the next available nonce

                # Construct the transaction object
                tx = {
                    'chainId': 2442,  # Mumbai Testnet
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
                        print(f"{w3.to_hex(tx_hash)}")
                    except Exception as e:
                        print(f"Error signing or sending transaction: {e}")
                else:
                    print("Error: Missing private key.")

        except Exception as e:
            print(f"Error: {e}")

        # Sleep for 5 seconds before checking balance again
        time.sleep(5)

# Run the loop in a separate thread to allow continuous execution
threading.Thread(target=loop, daemon=True).start()

# Keep the script running
input('Enter')
