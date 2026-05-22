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

# Optional ElectrumX settings for address-index endpoints
# Defaults are used if these are omitted
electrumx_host = "45.148.31.13"
electrumx_port = 50001
electrumx_timeout = 10
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

## Address-index backend behavior

- Address endpoints (`/balance/<address>`, `/history/<address>`, `/mempool/<address>`, `/unspent/<address>`) are served through ElectrumX script-hash queries.
- Non-address endpoints continue using ROD Core JSON-RPC via `endpoint`.
- The API documentation burn/script sample address `XXXXXXXXXXXXXXXXXXXXXXXXXXXXarcLhe` is intentional.
- Current limitation: Bech32 `rod1` addresses are not supported in address-to-scripthash conversion yet.

### Startup probe note

After starting the server with `python app.py`, wait at least **5-8 seconds** before probing endpoints to avoid false negatives during early startup.

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
