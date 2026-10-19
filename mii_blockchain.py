import hashlib
import json
from time import time
from urllib.parse import urlparse

import requests


class MIIBlockchain:
    def __init__(self):
        self._mii_chain = [{
            'index': 0,
            'timestamp': time(),
            'transactions': [],
            'merkle_root': '',
            'proof': 15102007,
            'previous_hash': 'maleshko',
        }]
        self._mii_current_transactions = []
        self._mii_nodes = set()

    @property
    def mii_chain(self):
        return self._mii_chain

    @property
    def mii_last_block(self):
        return self._mii_chain[-1]

    @property
    def mii_last_block_hash(self):
        return self.mii_hash(self.mii_last_block)

    @property
    def mii_last_block_proof(self):
        return self.mii_last_block['proof']

    @property
    def mii_current_transactions(self):
        return self._mii_current_transactions

    @property
    def mii_current_transactions_len(self):
        return len(self._mii_current_transactions)

    @property
    def mii_nodes(self):
        return self._mii_nodes

    def mii_new_transaction(self, sender, recipient, amount):
        self._mii_current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.mii_last_block['index'] + 1

    def mii_new_block(self, previous_hash, proof):
        block = {
            'index': self.mii_last_block['index'] + 1,
            'timestamp': time(),
            'transactions': self._mii_current_transactions,
            'merkle_root': self.mii_merkle_tree(
                [self.mii_hash(transaction) for transaction in self._mii_current_transactions]),
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self._mii_chain.append(block)
        self._mii_current_transactions = []
        return block

    def mii_merkle_tree(self, current_transactions_hashes):
        if not current_transactions_hashes:
            return ''

        if len(current_transactions_hashes) == 1:
            return current_transactions_hashes[0]

        if len(current_transactions_hashes) % 2 != 0:
            current_transactions_hashes.append(current_transactions_hashes[-1])

        next_level = []
        for i in range(0, len(current_transactions_hashes), 2):
            combined = (current_transactions_hashes[i] + current_transactions_hashes[i + 1]).encode()
            next_level.append(hashlib.sha256(combined).hexdigest())

        return self.mii_merkle_tree(next_level)

    def mii_proof_of_work(self, last_proof):
        proof = 0
        while not self.mii_valid_proof(last_proof, proof):
            proof += 1
        return proof

    def mii_register_node(self, address):
        parsed_url = urlparse(address)
        self._mii_nodes.add(parsed_url.netloc)

    def mii_resolve_conflict(self):
        neighbours = self._mii_nodes
        new_chain = None
        max_length = len(self._mii_chain)
        for node in neighbours:
            response = requests.get(f"http://{node}/chain")
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.mii_valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self._mii_chain = new_chain
            return True

        return False

    @staticmethod
    def mii_valid_chain(chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            current_block = chain[current_index]
            print(f"{last_block}")
            print(f"{current_block}")
            print("\n-----------\n")
            if current_block['previous_hash'] != MIIBlockchain.mii_hash(last_block):
                return False
            if not MIIBlockchain.mii_valid_proof(last_block['proof'], current_block['proof']):
                return False
            last_block = current_block
            current_index += 1

        return True

    @staticmethod
    def mii_valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        is_valid = guess_hash[-2:] == "10"

        if is_valid:
            print("Proof: " + str(proof))
            print("Хеш: " + guess_hash)
            return True

        return False

    @staticmethod
    def mii_hash(data):
        block_string = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
