from server.methods.transaction import Transaction
from server import utils
from server import cache
import config

class Block():
    @classmethod
    def height(cls, height: int):
        data = utils.make_request("getblockhash", [height])

        if data["error"] is None:
            txid = data["result"]
            data.pop("result")
            data["result"] = utils.make_request("getblock", [txid])["result"]
            data["result"]["txcount"] = data["result"]["nTx"]
            data["result"].pop("nTx")

        return data

    @classmethod
    def hash(cls, bhash: str):
        data = utils.make_request("getblock", [bhash])

        if data["error"] is None:
            data["result"]["txcount"] = data["result"]["nTx"]
            data["result"].pop("nTx")

        return data

    @classmethod
    @cache.memoize(timeout=config.cache)
    def get(cls, height: int):
        return utils.make_request("getblockhash", [height])

    @classmethod
    def range(cls, height: int, offset: int):
        result = []
        for block in range(height - (offset - 1), height + 1):
            data = utils.make_request("getblockhash", [block])
            nethash = utils.make_request("getnetworkhashps", [120, block])

            if data["error"] is None and nethash["error"] is None:
                bhash = data["result"]
                data.pop("result")

                block_data = utils.make_request("getblock", [bhash])
                if block_data["error"] is not None:
                    continue

                data["result"] = block_data["result"]
                # Handle nethash result properly - it's a dict with sha256d and neoscrypt keys
                nethash_value = 0
                try:
                    if isinstance(nethash["result"], dict):
                        # Take the sum of both hash rates or just one of them
                        if "sha256d" in nethash["result"]:
                            nethash_value += float(nethash["result"]["sha256d"])
                        if "neoscrypt" in nethash["result"]:
                            nethash_value += float(nethash["result"]["neoscrypt"])
                    else:
                        nethash_value = float(nethash["result"])
                except (ValueError, TypeError, KeyError):
                    nethash_value = 0
                
                # Convert to int if possible
                try:
                    data["result"]["nethash"] = int(nethash_value)
                except (ValueError, TypeError):
                    data["result"]["nethash"] = 0
                    
                data["result"]["txcount"] = data["result"]["nTx"]
                data["result"].pop("nTx")

                result.append(data["result"])

        return result[::-1]

    @classmethod
    @cache.memoize(timeout=config.cache)
    def inputs(cls, bhash: str):
        data = cls.hash(bhash)
        return Transaction().addresses(data["result"]["tx"])
