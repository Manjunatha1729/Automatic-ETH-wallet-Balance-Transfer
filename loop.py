# import threading
# from tracemalloc import stop
# from web3 import Web3
# w3 = Web3(Web3.HTTPProvider("https://www.alchemy.com/..."))
# private_key = "4e752d04017a5a9ef9726b0ee262566562d6ef7e8a6c02529ebacb1ec1c38a2d"
# pub_key ="0x9BAbf3490ee292bAbFCcf6DF26475108D88eDfb2"

# recipient_pub_key = "0xA9BAF7e3B6A21E24E5450E23C921e60F5F1B99A4"
# def loop():
#     while True:
#         balance = w3.eth.get_balance(pub_key)
#         print()
#         print(balance)
#         gasPrice = w3.toWei('1100', 'gwei')
#         gasLimit = 21000
#         nonce = w3.eth.getTransactionCount(pub_key)
#         tx = {
#             'chainId': 3,
#             'nonce': nonce,
#             'to': recipient_pub_key,
#             'value': balance-gasLimit*gasPrice,
#             'gas': gasLimit,
#             'gasPrice': gasPrice
#         }

#         try:
#          if balance > 0:
#             signed_tx = w3.eth.account.sign_transaction(tx, private_key)
#             tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
#             print(w3.toHex(tx_hash))
#         except:
#             print("insufficient funds")

# threading.Thread(target=loop, daemon=True).start()
# input('Press Enter to exit.')







import threading
import time
from web3 import Web3

# Connect to Binance Smart Chain
w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))

# Sensitive data: Use environment variables or secure storage in production
private_key = "de15d2f43192f331d7678c0ffa1a271308924ae60661f4bcc055a0179588a8d2"
pub_key = "0xA9BAF7e3B6A21E24E5450E23C921e60F5F1B99A4"
recipient_pub_key = "0x9BAbf3490ee292bAbFCcf6DF26475108D88eDfb2"

def loop():
    while True:
        try:
            
            balance = w3.eth.get_balance(pub_key)
            print(f"Current Balance: {w3.from_wei(balance, 'ether')} BNB")
            
            # Gas settings
            gas_price = w3.eth.gas_price  # Fetch current gas price dynamically
            gas_limit = 21000
            
            # Ensure balance can cover gas cost
            gas_cost = gas_limit * gas_price
            if balance <= gas_cost:
                print("Insufficient funds for gas. Waiting...")
                time.sleep(5)  # Retry after 60 seconds
                continue

            # Transaction settings
            nonce = w3.eth.get_transaction_count(pub_key)
            tx = {
                'chainId': 56,  # BSC Mainnet Chain ID
                'nonce': nonce,
                'to': recipient_pub_key,
                'value': balance - gas_cost,  # Deduct gas cost from the balance
                'gas': gas_limit,
                'gasPrice': gas_price
            }

            # Sign and send transaction
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"Transaction sent: {w3.toHex(tx_hash)}")

        except Exception as e:
            print(f"Error: {e}")
        
        # Avoid overloading the network
        time.sleep(60)

# Start the loop in a separate thread
threading.Thread(target=loop, daemon=True).start()
input('Press Enter to exit.')
