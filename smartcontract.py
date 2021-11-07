import json
import base64
from algosdk import account
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn
import time

def simple_smart_contract():
  algod_token = "2f3203f21e738a1de6110eba6984f9d03e5a95d7a577b34616854064cf2c0e7b"
  algod_address = "https://academy-algod.dev.aws.algodev.network/"
  algod_client = algod.AlgodClient(algod_token, algod_address)

  #Generate new account for this transaction
  secret_key, my_address = account.generate_account()
  print("My address: {}".format(my_address))

  # Check your balance. It should be 0 microAlgos
  account_info = algod_client.account_info(my_address)
  print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

  #Fund the created account
  print('Fund the created account using testnet faucet: \n https://dispenser.testnet.aws.algodev.network/ ')

  completed = ""
  while completed.lower() != 'yes':
    completed = input("Type 'yes' once you funded the account: ");

  print('Fund transfer in process...')
  # Wait for the faucet to transfer funds
  time.sleep(10)
  
  print('Fund transferred!')
  # Check your balance. It should be 10000000 microAlgos
  account_info = algod_client.account_info(my_address)
  print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

  # build transaction
  print("Building transaction")
  params = algod_client.suggested_params()
  # comment out the next two (2) lines to use suggested fees
  params.flat_fee = True
  params.fee = 1000
  receiver = "QLCTCCR2O4YLGN2JME5OFHGPYSZYDJXGTPV33HMUELGDOC7AL4Q7HHSZJ4"
  note = "Transaction By Sukant Jha".encode()

  # Fifth argument is a close_remainder_to parameter that creates a payment txn that sends all of the remaining funds to the specified address. If you want to learn more, go to: https://developer.algorand.org/docs/reference/transactions/#payment-transaction
  unsigned_txn = PaymentTxn(my_address, params, receiver, 1000000, receiver, note)

  # sign transaction
  print("Signing transaction")
  signed_txn = unsigned_txn.sign(secret_key)
  print("Sending transaction")
  txid = algod_client.send_transaction(signed_txn)
  print('Transaction Info:')
  print("Signed transaction with txID: {}".format(txid))

  # wait for confirmation	
  try:
    print("Waiting for confirmation")
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
  except Exception as err:
    print(err)
    return

  print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))
  print("Decoded note: {}".format(base64.b64decode(
    confirmed_txn["txn"]["txn"]["note"]).decode()))

  account_info = algod_client.account_info(my_address)
  print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

# utility for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1;
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))

simple_smart_contract()
