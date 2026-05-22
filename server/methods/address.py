from server import utils

class Address():
    @classmethod
    def balance(cls, address: str):
        try:
            script_hash = utils.address_to_electrum_scripthash(address)
        except ValueError as error:
            return utils.dead_response(str(error))

        data = utils.make_electrumx_request("blockchain.scripthash.get_balance", [script_hash])
        if data["error"] is None and isinstance(data.get("result"), dict):
            data["result"] = {
                "balance": int(data["result"].get("confirmed", 0) or 0),
                "received": int(data["result"].get("confirmed", 0) or 0),
                "unconfirmed": int(data["result"].get("unconfirmed", 0) or 0),
            }

        return data

    @classmethod
    def mempool(cls, address: str, raw=False):
        try:
            script_hash = utils.address_to_electrum_scripthash(address)
        except ValueError as error:
            return utils.dead_response(str(error))

        data = utils.make_electrumx_request("blockchain.scripthash.get_mempool", [script_hash])

        if data["error"] is None and isinstance(data.get("result"), list):
            total = len(data["result"])
            transactions = [tx["txid"] for tx in data["result"]] if raw else data["result"]
            data["result"] = {"tx": transactions, "txcount": total}

        return data

    @classmethod
    def unspent(cls, address: str, amount: int):
        try:
            script_hash = utils.address_to_electrum_scripthash(address)
        except ValueError as error:
            return utils.dead_response(str(error))

        data = utils.make_electrumx_request("blockchain.scripthash.listunspent", [script_hash])

        if data["error"] is None:
            utxos = []
            for utxo in data["result"]:
                value_satoshis = int(utxo.get("value", 0) or 0)
                if value_satoshis < int(amount):
                    continue
                utxos.append({
                    "txid": utxo.get("tx_hash") or utxo.get("txid"),
                    "index": utxo.get("tx_pos"),
                    "script": utxo.get("script"),
                    "value": value_satoshis,
                    "height": utxo.get("height"),
                })
            data["result"] = utxos

        return data

    @classmethod
    def history(cls, address: str):
        try:
            script_hash = utils.address_to_electrum_scripthash(address)
        except ValueError as error:
            return utils.dead_response(str(error))

        data = utils.make_electrumx_request("blockchain.scripthash.get_history", [script_hash])

        if data["error"] is None and isinstance(data.get("result"), list):
            history_entries = data["result"][::-1]
            total = len(history_entries)
            transactions = [
                entry["tx_hash"] for entry in history_entries
                if isinstance(entry, dict) and "tx_hash" in entry
            ]
            data["result"] = {"tx": transactions, "txcount": total}

        return data

    @classmethod
    def check(cls, addresses: list):
        addresses = list(set(addresses))
        result = []
        address_pairs = []

        for address in addresses:
            try:
                script_hash = utils.address_to_electrum_scripthash(address)
            except ValueError:
                continue
            address_pairs.append((address, script_hash))

        batch_responses = utils.make_electrumx_batch_request(
            "blockchain.scripthash.get_history",
            [[script_hash] for _, script_hash in address_pairs],
        )

        for index, response in enumerate(batch_responses):
            if index >= len(address_pairs):
                break
            address, _ = address_pairs[index]
            if response.get("error") is None and isinstance(response.get("result"), list) and len(response["result"]) > 0:
                result.append(address)

        return utils.response(result)
