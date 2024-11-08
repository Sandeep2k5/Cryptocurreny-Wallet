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
This project is licensed under the MIT License.s
