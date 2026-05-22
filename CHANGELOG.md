# Changelog

## 2026-05-22

### Added
- ElectrumX address-index integration in [`server/utils.py`](server/utils.py) with:
  - JSON-lines TCP request helper.
  - Default ElectrumX config fallback (`45.148.31.13:50001`, timeout `10s`).
  - Base58Check address decoding and address-to-scripthash conversion for ROD prefixes `60` (P2PKH) and `75` (P2SH/script).

### Changed
- Migrated address endpoints in [`server/methods/address.py`](server/methods/address.py) from unavailable ROD Core addressindex RPC methods to ElectrumX script-hash methods:
  - `/balance/<address>` -> `blockchain.scripthash.get_balance`
  - `/history/<address>` -> `blockchain.scripthash.get_history`
  - `/mempool/<address>` -> `blockchain.scripthash.get_mempool`
  - `/unspent/<address>` -> `blockchain.scripthash.listunspent`
- Updated [`check()`](server/methods/address.py:96) to use ElectrumX history presence checks.
- Updated project docs in [`README.md`](README.md) with ElectrumX configuration and startup probe guidance.

### Verified
- Compile proof: `python -m py_compile server\utils.py server\methods\address.py`.
- Live endpoint proof for burn/script sample address `XXXXXXXXXXXXXXXXXXXXXXXXXXXXarcLhe`:
  - `/balance/...` returns `error: null` with balance data.
  - `/history/...` returns `error: null` with transaction list and count.
  - `/mempool/...` returns `error: null`.
  - `/unspent/...` returns `error: null` with UTXOs.

### Known Limitations
- Bech32 `rod1` address-to-scripthash conversion is currently unsupported.
- `balance.received` currently aliases confirmed balance due to ElectrumX response model.
