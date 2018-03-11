from flask import Flask, request, jsonify
from block import Block
import os
import json
import uuid
import requests
app = Flask(__name__)


blockchain = [Block.create_genesis_block()]
peer_nodes = []
transactions_in_node = []
miner_address = f"minder-{uuid.uuid4()}"
mining = True


def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor


def find_new_chains():
    other_chains = []
    for host in peer_nodes:
        url = f'{node_url}/blocks'
        r = requests.get(url)
        block = r.json()
        other_chains.append(block)
    return other_chains


def consensus():
    other_chains = find_new_chains()
    all_chains = other_chains + blockchain

    len_all_chains = [len(_) for _ in all_chains]
    max_index = len_all_chains.index(max(lan_all_chains))
    my_index = all_chain.index(blockchain)
    if max_index != my_index:
        print('my chain discarede')
    blockchain = all_chains[max_index]


@app.route('/mine', methods = ['GET'])
def mine():
    last_block = blockchain[-1]
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof)
    transactions_in_node.append(
        { "from": "network", "to": miner_address, "amount": 1 }
    )
    copied_transaction = [_ for _ in transactions_in_node]
    new_block_data = {
        "proof-of-work": proof,
        "transactions": copied_transaction
    }
    transactions_in_node[:] = []

    mined_block = last_block.next_block(new_block_data)
    blockchain.append(mined_block)
    return json.dumps(mined_block.to_json())


@app.route('/blocks', methods=['GET'])
def get_blocks():

    return json.dumps([_.to_json() for _ in blockchain])


@app.route('/txion', methods=['POST'])
def transaction():
    new_txion = request.get_json()
    print(f"Transaction: from:{new_txion['from']} to:{new_txion['to']} amount: {new_txion['amount']}")
    transactions_in_node.append(new_txion)
    return jsonify(success=True)


@app.route('/peers', methods=['POST'])
def post_peers():
    j = request.get_json()
    new_node = j['node']
    peer_nodes.append(new_node)
    return jsonify(peers=peer_nodes)


@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify(peers=peer_nodes)

port = int(os.environ.get('PORT', 5000))
app.run(port=port)
