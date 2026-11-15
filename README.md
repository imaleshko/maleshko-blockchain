# MII Blockchain

A Python-based blockchain prototype featuring Proof of Work, Merkle tree hashing, decentralized node consensus, and both
a REST API and an interactive CLI.

## Features

- Block forging with SHA-256 hashing and Proof of Work validation
- Merkle root calculation for block transactions
- Transaction management with unique UUID identifiers and mining rewards
- Bidirectional peer node registration with loop protection
- Longest-chain conflict resolution with orphaned transaction recovery to the mempool

## Modes & Endpoints

### REST API (`mii_app.py`)

- `POST /transactions/new` — add a new transaction to the mempool
- `GET /mine` — mine a new block and receive the mining reward
- `GET /chain` — retrieve the full blockchain and its length
- `POST /nodes/register` — mutually register neighboring nodes
- `GET /nodes/resolve` — synchronize and resolve chain conflicts across registered peers

### Interactive CLI (`mii_run.py`)

- Terminal menu for creating transactions, automatic block mining, and inspecting the mempool or chain

## Tech Stack

- Python
- Flask
- Requests
