from server import utils
from server import cache
import requests
import config

class General():
    @classmethod
    def info(cls):
        data = utils.make_request("getblockchaininfo")

        if data["error"] is None:
            #data["result"]["supply"] = utils.supply(data["result"]["blocks"])["supply"]
            #data["result"]["reward"] = utils.reward2(data["result"]["blocks"])
            #data["result"]["supply"] = utils.supply(data["result"]["blocks"])["supply"]
            data["result"]["reward"] = utils.reward2(data["result"]["blocks"])
            # Add supply information
            supply_info = utils.supply(data["result"]["blocks"])
            data["result"]["supply"] = supply_info["supply"]
            data["result"]["max_supply"] = supply_info["total/max supply"]
            data["result"].pop("verificationprogress", None)
            data["result"].pop("initialblockdownload", None)
            data["result"].pop("pruned", None)
            data["result"].pop("softforks", None)
            # Check if key exists before trying to pop it
            data["result"].pop("bip9_softforks", None)
            data["result"].pop("warnings", None)
            data["result"].pop("size_on_disk", None)

            nethash = utils.make_request("getnetworkhashps", [config.spend_confirmations, data["result"]["blocks"]])
            if nethash["error"] is None:
                # Handle nethash result properly - it might be a dict
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

        return data

    @classmethod
    @cache.memoize(timeout=config.cache)
    def supply(cls):
        data = utils.make_request("getblockchaininfo")
        print(data)
        #height = data["result"]["blocks"]
        height = data["result"]["blocks"]
        result = utils.supply(height)
        result["height"] = height

        return result
    
    @classmethod
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
            "blocks": config.spend_confirmations
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
        # Use Coinpaprika API instead of CoinGecko
        try:
            import urllib.request
            import urllib.error
            import json
            
            url = "https://api.coinpaprika.com/v1/tickers/rod-spacexpanse"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            try:
                response = urllib.request.urlopen(req, timeout=10)
                data = response.read()
                price_data = json.loads(data)
            except urllib.error.URLError as e:
                # Try without SSL verification
                import ssl
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                response = urllib.request.urlopen(req, timeout=10, context=context)
                data = response.read()
                price_data = json.loads(data)
            
            # Extract price data from Coinpaprika format
            if price_data and not price_data.get('error'):
                quotes = price_data.get("quotes", {})
                usd_data = quotes.get("USD", {})
                usd_price = usd_data.get("price", 0)
                btc_price = 0.0  # BTC price not available in Coinpaprika response
                
                return {
                    "rodchain": {
                        "usd": usd_price,
                        "btc": btc_price
                    }
                }
            else:
                return {"rodchain": {"usd": 0, "btc": 0}}
        except Exception:
            return {"rodchain": {"usd": 0, "btc": 0}}
