from uuid import uuid4

from flask import Flask
from flask import request

from mii_blockchain import MIIBlockchain

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = MIIBlockchain()


@app.post('/transactions/new')
def mii_new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Пропущено значення', 400
    index = blockchain.mii_new_transaction(
        values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Транзакція буде додана до блоку {index}'}
    return response, 201


@app.get('/mine')
def mii_mine():
    last_proof = blockchain.mii_last_block_proof
    proof = blockchain.mii_proof_of_work(last_proof)
    blockchain.mii_new_transaction("0", node_identifier, 15)
    previous_hash = blockchain.mii_last_block_hash
    block = blockchain.mii_new_block(previous_hash, proof)
    response = {
        'message': f'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'merkle_root': block['merkle_root'],
        'proof': proof,
        'previous_hash': block['previous_hash']
    }
    return response, 200


@app.get('/chain')
def mii_chain():
    response = {
        'chain': blockchain.mii_chain,
        'length': len(blockchain.mii_chain)
    }
    return response


@app.post('/nodes/register')
def mii_register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Помилка: надайте список вузлів", 400
    for node in nodes:
        blockchain.mii_register_node(node)
    response = {
        'message': 'Додано нові вузли',
        'total_nodes': list(blockchain.mii_nodes)
    }
    return response, 201


@app.get('/nodes/resolve')
def mii_consensus():
    replaced = blockchain.mii_resolve_conflict()
    if replaced:
        response = {
            'message': 'Наш ланцюг було замінено',
            'new_chain': blockchain.mii_chain
        }
    else:
        response = {
            'message': 'Наш ланцюг залишився',
            'chain': blockchain.mii_chain
        }
    return response, 200
