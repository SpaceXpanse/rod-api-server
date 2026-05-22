# ROD API Server

Python Flask/SocketIO middleware API for the SpaceXpanse ROD blockchain.

## Getting started

Create a `config.py` file in the project root:

```python
rid = "api-server"
cache = 3600  # Cache request for 1 hour
secret = "YOU SHOULD HAVE A VERY STRONG PASSWORD HERE"
endpoint = "http://rpcuser:rpcpassword@127.0.0.1:11999/"  # ROD RPC
host = "0.0.0.0"
port = 1234
debug = False
block_page = 10
tx_page = 25
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## API response envelope

- `result`: list or object containing requested data
- `error`: error message when a request fails
- `id`: API server identifier from `config.py`

All amounts are represented in **satoshis** (10^-8 ROD).

## SpaceXpanse ROD network facts (reference)

- Name: SpaceXpanse
- Ticker: ROD
- Symbol: Ɍ
- Address letter: `R`
- P2PKH prefix: `60`
- P2SH prefix: `75`
- Mainnet bech32 HRP: `rod`
- P2P port: `11998`
- RPC port: `11999`
- AuxPoW chain ID: `1899`
- PoW algorithms: `neoscrypt-xaya` and `SHA-256d` (merged mining)
- Target block time: ~30 seconds
- Target algorithm distribution: 75% `neoscrypt-xaya` / 25% `SHA-256d`
- Standard block reward: `800 ROD`
- Pre-release phase: `55,560` blocks at `1 ROD`
- Halving interval: `1,054,080` blocks for 5 years
- Post-halving monetary phase: ~3% inflation for 59 years
- Name/value storage limits: names `256` bytes, values `2,048` bytes
