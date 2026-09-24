import hashlib
import json
from time import time


class MIIBlockchain:
    def __init__(self):
        self._mii_chain = [{
            'index': 0,
            'timestamp': time(),
            'transactions': [],
            'proof': 15102007,
            'previous_hash': 'maleshko',
        }]
        self._mii_current_transactions = []

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
        return len(self.mii_current_transactions)

    def mii_new_transaction(self, mii_sender, mii_recipient, mii_amount):
        self._mii_current_transactions.append({
            'sender': mii_sender,
            'recipient': mii_recipient,
            'amount': mii_amount
        })
        return self.mii_last_block['index'] + 1

    def mii_new_block(self, mii_previous_hash, mii_proof):
        block = {
            'index': self.mii_last_block['index'] + 1,
            'timestamp': time(),
            'transactions': self._mii_current_transactions,
            'proof': mii_proof,
            'previous_hash': mii_previous_hash,
        }
        self._mii_chain.append(block)
        self._mii_current_transactions = []
        return block

    def mii_proof_of_work(self, mii_last_proof):
        mii_proof = 0
        while not self.mii_valid_proof(mii_last_proof, mii_proof):
            mii_proof += 1
        return mii_proof

    @staticmethod
    def mii_valid_proof(mii_last_proof, mii_proof):
        mii_guess = f'{mii_last_proof}{mii_proof}'.encode()
        mii_guess_hash = hashlib.sha256(mii_guess).hexdigest()
        return mii_guess_hash[-2:] == "10"

    @staticmethod
    def mii_hash(mii_blok):
        mii_block_string = json.dumps(mii_blok, sort_keys=True).encode()
        return hashlib.sha256(mii_block_string).hexdigest()
