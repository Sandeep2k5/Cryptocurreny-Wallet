Cryptocurrency Wallet & Blockchain System
This project is a basic cryptocurrency wallet and blockchain system with a client-server setup. It includes a graphical user interface (GUI) for managing blockchain accounts, viewing balances, and conducting transactions using a Proof-of-Work (PoW) blockchain. The project allows blockchain data synchronization between clients and a server.

Table of Contents
Features
Project Structure
Prerequisites
Installation
Usage
Server Setup
Client Setup
Contributing
License
Features
Blockchain Implementation: Basic blockchain structure with a Genesis block, block mining, and chain verification.
Proof of Work (PoW): Simple PoW mechanism with adjustable difficulty.
Account Management: Create and manage accounts with private and public keys.
Transaction Management: Validate and conduct transactions between accounts.
Client-Server Synchronization: Sync blockchain data between client and server.
Project Structure
graphql
Copy code
.
├── main.py                 # Main GUI client for wallet and blockchain operations
├── server.py               # Server for receiving blockchain data
├── blockchain.py           # Blockchain implementation (Blocks, Blockchain, Account classes)
├── blockchain.json         # JSON file to persist the blockchain
├── accounts.json           # JSON file to persist user accounts
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
Prerequisites
Python 3.x
PyQt5 for the GUI application
Basic knowledge of blockchain and Python socket programming is helpful.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/cryptocurrency-wallet-blockchain.git
cd cryptocurrency-wallet-blockchain
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
1. Start the Server
To start the server and enable blockchain data synchronization:

bash
Copy code
python server.py
The server listens on localhost:5000 by default. It will receive and store the blockchain data sent by clients.

2. Start the Client (Wallet)
To run the wallet GUI and interact with the blockchain:

bash
Copy code
python main.py
This opens a GUI that allows you to:

Create accounts with a randomly generated private key.
Conduct transactions by entering the sender's and recipient's public keys, amount, and the sender’s private key.
View account balances.
Send blockchain data to the server for synchronization.
Server Setup
The server code (server.py) listens for incoming blockchain data from clients. When data is received, the server updates its blockchain based on the received data. This enables multiple clients to synchronize their blockchain data through a central server.

Running the Server
bash
Copy code
python server.py
Client Setup
The client code (main.py) provides a GUI for account and transaction management, and an option to send blockchain data to the server.

Creating Accounts: Enter an account holder's name and initial balance, then click "Create Account" to generate a new account. The client will display the public key and private key.
Making Transactions: Enter the sender and recipient public keys, amount, and sender’s private key, then click "Make Transaction" to complete a transaction.
Sending Blockchain Data to Server: To synchronize the blockchain with the server, use the send_blockchain_data function in the main script.
Example Usage
To send blockchain data from the client:

python
Copy code
send_blockchain_data("localhost", 5000, blockchain_app)
Contributing
Contributions are welcome! Please open an issue to discuss what you’d like to contribute or improve, and feel free to submit a pull request with your changes.

License
This project is licensed under the MIT License.
