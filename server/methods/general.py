from server import utils
from server import cache
import config

class General():
    @classmethod
    def info(cls):
        data = utils.make_request("getblockchaininfo")

        if data["error"] is None:
            data["result"]["supply"] = utils.supply(data["result"]["blocks"])["supply"]
            data["result"]["reward"] = utils.reward2(data["result"]["blocks"])
            keys_to_remove = [
                "verificationprogress",
                "initialblockdownload",
                "pruned",
                "softforks",
                "bip9_softforks",
                "warnings",
                "size_on_disk",
            ]
            for field_name in keys_to_remove:
                if field_name in data["result"]:
                    del data["result"][field_name]

            nethash = utils.make_request("getnetworkhashps", [120, data["result"]["blocks"]])
            if nethash["error"] is None:
                network_hash_result = nethash.get("result")
                if isinstance(network_hash_result, dict):
                    data["result"]["nethash"] = int(sum(network_hash_result.values()))
                else:
                    data["result"]["nethash"] = int(network_hash_result)

        return data

    @classmethod
    @cache.memoize(timeout=config.cache)
    def supply(cls):
        data = utils.make_request("getblockchaininfo")
        result_data = data.get("result") if isinstance(data, dict) else None
        if data.get("error") is not None or not isinstance(result_data, dict) or "blocks" not in result_data:
            return {
                "halvings": 0,
                "supply": 0,
                "total/max supply": utils.satoshis(utils.ROD_MAX_SUPPLY),
                "policy": "spacexpanse-rod",
                "inflation_model": "approximate_3_percent_annual_post_halving",
                "height": 0,
            }
        height = result_data["blocks"]
        result = utils.supply(height)
        result["height"] = height

        return result
    
    @classmethod
    @cache.memoize(timeout=1)
    def getprice(cls):
        result = utils.getprice()
        return result

    @classmethod
    def fee(cls):
        # ToDo: Fix me

        # data = utils.make_request("estimatesmartfee", [6])

        # if data["error"] is None:
        #   data["result"]["feerate"] = utils.satoshis(data["result"]["feerate"])

        # return data

        return utils.response({
            "feerate": utils.satoshis(0.0001),
            "blocks": 6
        })

    @classmethod
    def mempool(cls):
        data = utils.make_request("getmempoolinfo")

        if data["error"] is None:
            if data["result"]["size"] > 0:
                mempool = utils.make_request("getrawmempool")["result"]
                data["result"]["tx"] = mempool
            else:
                data["result"]["tx"] = []

        return data

    @classmethod
    @cache.memoize(timeout=600)
    def price(cls):
        fallback_price = cls.getprice()
        return {
            "spacexpanse": {
                "usd": float(fallback_price.get("price_usd", 0) or 0),
                "btc": float(fallback_price.get("price_btc", 0) or 0),
            }
        }
