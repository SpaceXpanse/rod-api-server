from server import utils
from server import cache
import config
import json

class Transaction():
    @classmethod
    def broadcast(cls, raw: str):
        return utils.make_request("sendrawtransaction", [raw])

    @classmethod
    @cache.memoize(timeout=config.cache)
    def decode(cls, raw: str):
        return utils.make_request("decoderawtransaction", [raw])

    @classmethod
    @cache.memoize(timeout=config.cache)
    def info(cls, thash: str):
        try:
            data = utils.make_request("getrawtransaction", [thash, True])
            
            # Check if the response is valid
            if not isinstance(data, dict):
                print(f"ERROR: Invalid response from getrawtransaction for {thash}: {data}")
                return {"error": "Invalid response from RPC", "result": None}
                
            if "error" not in data:
                print(f"WARNING: Response from getrawtransaction for {thash} missing 'error' field: {data}")
                return {"error": "Malformed response from RPC", "result": None}
                
            if data["error"] is not None:
                print(f"RPC ERROR in Transaction.info for {thash}: {data['error']}")
                return data  # Return the error as-is
                
            # Check if result exists and is valid
            if "result" not in data or not isinstance(data["result"], dict):
                print(f"ERROR: Missing or invalid 'result' in Transaction.info for {thash}: {data}")
                return {"error": "Invalid transaction data", "result": None}

            if "blockhash" in data["result"]:
                block_response = utils.make_request("getblock", [data["result"]["blockhash"]])
                if isinstance(block_response, dict) and "result" in block_response and block_response["result"] is not None:
                    block = block_response["result"]
                    data["result"]["height"] = block["height"]
                else:
                    print(f"ERROR: Could not get block data for {data['result']['blockhash']} in Transaction.info for {thash}")
                    data["result"]["height"] = -1
            else:
                data["result"]["height"] = -1

            if data["result"]["height"] != 0:
                for index, vin in enumerate(data["result"]["vin"]):
                    if "txid" in vin:
                        vin_data = utils.make_request("getrawtransaction", [vin["txid"], True])
                        
                        # Validate vin_data response
                        if not isinstance(vin_data, dict) or "error" not in vin_data:
                            print(f"ERROR: Invalid response from getrawtransaction for vin {vin['txid']} in Transaction.info for {thash}")
                            continue
                            
                        if vin_data["error"] is None:
                            if "result" not in vin_data or not isinstance(vin_data["result"], dict):
                                print(f"ERROR: Missing or invalid 'result' in vin data for {vin['txid']} in Transaction.info for {thash}")
                                continue
                                
                            if "vout" not in vin_data["result"] or not isinstance(vin_data["result"]["vout"], list):
                                print(f"ERROR: Missing or invalid 'vout' in vin data for {vin['txid']} in Transaction.info for {thash}")
                                continue
                                
                            if vin["vout"] >= len(vin_data["result"]["vout"]):
                                print(f"ERROR: Invalid vout index {vin['vout']} for vin {vin['txid']} in Transaction.info for {thash}")
                                continue
                                
                            data["result"]["vin"][index]["scriptPubKey"] = vin_data["result"]["vout"][vin["vout"]]["scriptPubKey"]
                            data["result"]["vin"][index]["value"] = utils.satoshis(vin_data["result"]["vout"][vin["vout"]]["value"])

            amount = 0
            for index, vout in enumerate(data["result"]["vout"]):
                if "value" in vout:
                    data["result"]["vout"][index]["value"] = utils.satoshis(vout["value"])
                    amount += vout["value"]
                else:
                    print(f"WARNING: Missing 'value' in vout {index} for transaction {thash}")

            data["result"]["amount"] = amount

        except Exception as e:
            print(f"EXCEPTION in Transaction.info for {thash}: {e}")
            return {"error": f"Exception occurred: {str(e)}", "result": None}

        return data

    @classmethod
    @cache.memoize(timeout=config.cache)
    def addresses(cls, tx_data):
        updates = {}
        for tx in tx_data:
            transaction = Transaction().info(tx)
            vin = transaction["result"]["vin"]
            vout = transaction["result"]["vout"]

            for info in vin:
                if "scriptPubKey" in info:
                    if "addresses" in info["scriptPubKey"]:
                        for address in info["scriptPubKey"]["addresses"]:
                            if address in updates:
                                updates[address].append(tx)
                                updates[address] = list(set(updates[address]))
                            else:
                                updates[address] = [tx]

            for info in vout:
                if "scriptPubKey" in info:
                    if "addresses" in info["scriptPubKey"]:
                        for address in info["scriptPubKey"]["addresses"]:
                            if address in updates:
                                updates[address].append(tx)
                                updates[address] = list(set(updates[address]))
                            else:
                                updates[address] = [tx]

        return updates

    @classmethod
    def spent(cls, txid: str):
        return utils.make_request("getspentinfo", [txid])
