from server import utils

class Address():
    @classmethod
    def balance(cls, address: str):
        # Check if the method is available, if not return error
        data = utils.make_request("getaddressbalance", [address])
        if data["error"] and data["error"]["code"] == -32601:
            # Method not found, return a proper error response
            return utils.dead_response("Address indexing not available on this node")
        return data

    @classmethod
    def mempool(cls, address: str, raw=False):
        # Check if the method is available, if not return error
        data = utils.make_request("getaddressmempool", [address])
        if data["error"] and data["error"]["code"] == -32601:
            # Method not found, return a proper error response
            return utils.dead_response("Address indexing not available on this node")

        if data["error"] is None:
            total = len(data["result"])

            if raw:
                transactions = []
                for index, tx in enumerate(data["result"]):
                    transactions.append(tx["txid"])

            else:
                transactions = data["result"]
                for index, tx in enumerate(transactions):
                    transactions[index].pop("address")

            data.pop("result")
            data["result"] = {}
            data["result"]["tx"] = transactions
            data["result"]["txcount"] = total

        return data

    @classmethod
    def unspent(cls, address: str, amount: int):
        # Check if the method is available, if not return error
        data = utils.make_request("getaddressutxos", [address, utils.amount(amount)])
        if data["error"] and data["error"]["code"] == -32601:
            # Method not found, return a proper error response
            return utils.dead_response("Address indexing not available on this node")

        if data["error"] is None:
            utxos = []
            for index, utxo in enumerate(data["result"]):
                utxos.append({
                    "txid": utxo["txid"],
                    "index": utxo["outputIndex"],
                    "script": utxo["script"],
                    "value": utxo["satoshis"],
                    "height": utxo["height"]
                })

            data["result"] = utxos

        return data

    @classmethod
    def history(cls, address: str):
        # Check if the method is available, if not return error
        data = utils.make_request("getaddresstxids", [address])
        if data["error"] and data["error"]["code"] == -32601:
            # Method not found, return a proper error response
            return utils.dead_response("Address indexing not available on this node")

        if data["error"] is None:
            data["result"] = data["result"][::-1]
            total = len(data["result"])
            transactions = data["result"]
            data.pop("result")
            data["result"] = {}
            data["result"]["tx"] = transactions
            data["result"]["txcount"] = total

        return data

    @classmethod
    def check(cls, addresses: list):
        addresses = list(set(addresses))
        result = []
        for address in addresses:
            # Check if the method is available, if not return error
            data = utils.make_request("getaddresstxids", [address])
            if data["error"] and data["error"]["code"] == -32601:
                # Method not found, return a proper error response
                return utils.dead_response("Address indexing not available on this node")
            if len(data["result"]) > 0:
                result.append(address)

        return utils.response(result)
