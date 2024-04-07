import sys
import hashlib
import json
import random
import time
import os
import socket
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListView,
    QMessageBox,
)

def send_blockchain_data(host, port, blockchain):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = {
            "type": "blockchain_data",
            "data": [block._dict_ for block in blockchain.chain],
        }
        s.sendall(json.dumps(data).encode())
        response = s.recv(1024)
        print(response.decode())

class Block:
    def _init_(self, index, previous_hash, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = self.get_timestamp()
        self.nonce = nonce  # Nonce for PoW
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "data": self.data,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        return hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()

    def get_timestamp(self):
        return time.time()

class BlockchainAccount:
    def _init_(self, name, balance, private_key):
        self.private_key = private_key
        self.public_key = hashlib.sha256(str(private_key).encode()).hexdigest()
        self.name = name
        self.balance = balance

class Blockchain:
    def _init_(self):
        self.chain = self.load_blockchain()
        self.accounts = self.load_accounts()
        self.difficulty = 4  # Difficulty for PoW (number of leading zeros required in hash)

    def load_blockchain(self):
        if os.path.exists("blockchain.json"):
            try:
                with open("blockchain.json", "r") as json_file:
                    blockchain_data = json.load(json_file)
                    return [Block(b["index"], b["previous_hash"], b["data"], b["nonce"]) for b in blockchain_data]
            except Exception as e:
                print("Error loading blockchain data:", str(e))
                blockchain_data = []
        else:
            blockchain_data = []

        return [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block")

    def save_blockchain(self):
        blockchain_data = [{"index": block.index, "previous_hash": block.previous_hash, "data": block.data, "nonce": block.nonce} for block in self.chain]
        with open("blockchain.json", "w") as f:
            json.dump(blockchain_data, f, indent=4)

    def load_accounts(self):
        if os.path.exists("accounts.json"):
            try:
                with open("accounts.json", "r") as json_file:
                    accounts_data = json.load(json_file)
                    return {account["public_key"]: BlockchainAccount(account["name"], account["balance"], account["private_key"]) for account in accounts_data}
            except Exception as e:
                print("Error loading accounts data:", str(e))
                accounts_data = {}
        return {}

    def save_accounts(self):
        with open("accounts.json", "w") as f:
            accounts_data = [{"name": account.name, "balance": account.balance, "private_key": account.private_key, "public_key": public_key} for public_key, account in self.accounts.items()]
            json.dump(accounts_data, f, indent=4)

    def create_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(previous_block.index + 1, previous_block.hash, data)
        return new_block

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, block):
        self.mine_block(block)

    def mine_block(self, block):
        while True:
            block.nonce = random.randint(0, 2**32)
            block_hash = block.calculate_hash()
            if block_hash[:self.difficulty] == "0" * self.difficulty:
                self.chain.append(block)
                self.save_blockchain()
                break

    def verify_transaction(self, sender, recipient, amount, sender_private_key):
        if sender in self.accounts and recipient in self.accounts:
            sender_account = self.accounts[sender]
            if sender_account.balance >= amount and sender_account.private_key == sender_private_key:
                return True
        return False

    def update_account_balances(self, sender, recipient, amount):
        self.accounts[sender].balance -= amount
        self.accounts[recipient].balance += amount

    def add_transaction(self, sender, recipient, amount, sender_private_key):
        if self.verify_transaction(sender, recipient, amount, sender_private_key):
            self.update_account_balances(sender, recipient, amount)
            transaction = {
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
            }
            new_block = self.create_block(transaction)
            if new_block:
                self.add_block(new_block)  # Add the new block to the blockchain
                self.save_accounts()  # Save the accounts
                return True
        else:
            print("Transaction failed: Insufficient balance, invalid data, or incorrect private key.")

class CryptocurrencyWallet(QMainWindow):
    def _init_(self, blockchain):
        super()._init_()

        self.blockchain = blockchain

        self.setWindowTitle("Cryptocurrency Wallet")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Apply styles to labels
        self.account_label = QLabel("Account Holder's Name:")
        self.account_label.setStyleSheet("font-size: 16px; color: #333;")

        # Apply styles to inputs
        self.account_name_input = QLineEdit()
        self.account_name_input.setStyleSheet("font-size: 14px; padding: 5px;")
        self.balance_input = QLineEdit()
        self.balance_input.setStyleSheet("font-size: 14px; padding: 5px;")

        # Apply styles to buttons
        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.setStyleSheet("font-size: 16px; background-color: #4CAF50; color: white; padding: 10px; border: none;")
        self.create_account_button.clicked.connect(self.create_account)

        # Add widgets to layout
        self.layout.addWidget(self.account_label)
        self.layout.addWidget(self.account_name_input)
        self.layout.addWidget(self.balance_input)
        self.layout.addWidget(self.create_account_button)

        self.account_model = QStandardItemModel()
        self.account_list = QListView()
        self.account_list.setModel(self.account_model)

        # Apply styles to transaction labels
        self.transaction_label = QLabel("Make Transaction:")
        self.transaction_label.setStyleSheet("font-size: 18px; color: #333;")

        # Apply styles to sender input
        self.sender_label = QLabel("Sender Public Key:")
        self.sender_label.setStyleSheet("font-size: 14px; color: #333;")
        self.sender_input = QLineEdit()
        self.sender_input.setStyleSheet("font-size: 14px; padding: 5px;")

        # Apply styles to recipient input
        self.recipient_label = QLabel("Recipient Public Key:")
        self.recipient_label.setStyleSheet("font-size: 14px; color: #333;")
        self.recipient_input = QLineEdit()
        self.recipient_input.setStyleSheet("font-size: 14px; padding: 5px;")

        # Apply styles to amount input
        self.amount_label = QLabel("Amount:")
        self.amount_label.setStyleSheet("font-size: 14px; color: #333;")
        self.amount_input = QLineEdit()
        self.amount_input.setStyleSheet("font-size: 14px; padding: 5px;")

        # Apply styles to private key input
        self.private_key_label = QLabel("Private Key:")
        self.private_key_label.setStyleSheet("font-size: 14px; color: #333;")
        self.private_key_input = QLineEdit()
        self.private_key_input.setStyleSheet("font-size: 14px; padding: 5px;")

        # Apply styles to transaction button
        self.make_transaction_button = QPushButton("Make Transaction")
        self.make_transaction_button.setStyleSheet("font-size: 16px; background-color: #007BFF; color: white; padding: 10px; border: none;")
        self.make_transaction_button.clicked.connect(self.make_transaction)

        # Add transaction widgets to layout
        self.layout.addWidget(self.account_list)
        self.layout.addWidget(self.transaction_label)
        self.layout.addWidget(self.sender_label)
        self.layout.addWidget(self.sender_input)
        self.layout.addWidget(self.recipient_label)
        self.layout.addWidget(self.recipient_input)
        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_input)
        self.layout.addWidget(self.private_key_label)
        self.layout.addWidget(self.private_key_input)
        self.layout.addWidget(self.make_transaction_button)

        # Apply styles to view balance button
        self.view_balance_button = QPushButton("View Balance")
        self.view_balance_button.setStyleSheet("font-size: 16px; background-color: #f39c12; color: white; padding: 10px; border: none;")
        self.view_balance_button.clicked.connect(self.view_balance)

        # Add view balance button to layout
        self.layout.addWidget(self.view_balance_button)

        self.central_widget.setLayout(self.layout)

    def create_account(self):
        name = self.account_name_input.text()
        balance = float(self.balance_input.text())
        private_key = random.randint(1, 2**256)  # Generate a random private key
        account = BlockchainAccount(name, balance, private_key)
        self.blockchain.accounts[account.public_key] = account
        self.blockchain.save_accounts()
        self.account_model.appendRow(QStandardItem(f"Name: {account.name}, Public Key: {account.public_key}, Balance: {account.balance} BTC"))
        self.show_message("Account key", f"private key for the account is {private_key}")

    def make_transaction(self):
        sender_public_key = self.sender_input.text()
        recipient_public_key = self.recipient_input.text()
        amount = float(self.amount_input.text())
        private_key = int(self.private_key_input.text())  # Convert private key input to integer

        if self.blockchain.add_transaction(sender_public_key, recipient_public_key, amount, private_key):
            self.sender_input.clear()
            self.recipient_input.clear()
            self.amount_input.clear()
            self.private_key_input.clear()  # Clear private key input
            self.show_message("Transaction Completed", "Transaction completed successfully!")
        else:
            self.show_message("Transaction Failed", "Transaction failed: Insufficient balance, invalid data, or incorrect private key.")

    def view_balance(self):
        public_key = self.sender_input.text()
        private_key_str = self.private_key_input.text()

        if not public_key or not private_key_str:
            self.show_message("Input Error", "Please enter both a valid public key and private key.")
            return

        try:
            private_key = int(private_key_str)
        except ValueError:
            self.show_message("Input Error", "Private key must be a valid integer.")
            return

        if public_key in self.blockchain.accounts:
            account = self.blockchain.accounts[public_key]
            if account.private_key == private_key:
                self.show_message("Account Balance",
                                  f"Account Balance for Public Key {public_key}: {account.balance} BTC")
            else:
                self.show_message("Invalid Private Key", "Private key does not match the provided public key.")
        else:
            self.show_message("Account Not Found", "Account with the provided public key does not exist.")
            
    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


def main():
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
        QListView, QMessageBox
    from PyQt5.QtGui import QStandardItemModel, QStandardItem
    # Existing code for creating a QApplication and the CryptocurrencyWallet
    app = QApplication(sys.argv)
    blockchain_app = Blockchain()
    wallet = CryptocurrencyWallet(blockchain_app)
    
    # Receive blockchain data from the other laptop
    send_blockchain_data("localhost", 5000, blockchain_app)
    
    wallet.show()
    sys.exit(app.exec_())

if _name_ == "_main_":
    main(