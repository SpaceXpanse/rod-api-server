from server import cache
import config

class Esplora():
    @classmethod
    @cache.memoize(timeout=config.cache)
    def block(self, result):
        return {
            "id": result["hash"],
            "height": result["height"],
            "version": result["version"],
            "timestamp": result["time"],
            "tx_count": result["txcount"],
            "size": result["size"],
            "weight": result["weight"],
            "merkle_root": result["merkleroot"],
            "previousblockhash": result["previousblockhash"],
            "nonce": result["nonce"],
            "bits": int(result["bits"], 16),
            "difficulty": result["difficulty"]
        }

    @classmethod
    @cache.memoize(timeout=config.cache)
    def transaction(cls, result):
        # Input validation
        if not isinstance(result, dict):
            print(f"ERROR: Esplora.transaction received non-dict result: {type(result)}")
            return utils.dead_response("Invalid input type")

        # Check for required keys in the result
        required_keys = ["vin", "vout", "txid", "version", "locktime", "size"]
        for key in required_keys:
            if key not in result:
                print(f"ERROR: Esplora.transaction missing required key '{key}' in result: {result}")
                return {"error": f"Missing required key: {key}", "result": None}

        # Validate vin and vout are lists
        if not isinstance(result["vin"], list):
            print(f"ERROR: Esplora.transaction 'vin' is not a list: {type(result['vin'])}")
            return utils.dead_response("Invalid vin structure")

        if not isinstance(result["vout"], list):
            print(f"ERROR: Esplora.transaction 'vout' is not a list: {type(result['vout'])}")
            return utils.dead_response("Invalid vout structure")

        outputs = []
        inputs = []

        status = {"confirmed": False}
        outputs_amount = 0
        inputs_amount = 0
        coinbase = True
        fee = 0

        for i, vin in enumerate(result["vin"]):
            # Validate each vin entry
            if not isinstance(vin, dict):
                print(f"ERROR: Esplora.transaction vin[{i}] is not a dict: {type(vin)}")
                continue

            # Check for required keys in vin
            vin_required_keys = ["sequence"]
            for key in vin_required_keys:
                if key not in vin:
                    print(f"ERROR: Esplora.transaction vin[{i}] missing required key '{key}': {vin}")
                    continue

            input_data = {
                "txid": "0" * 64,
                "sequence": vin["sequence"],
                "prevout": None,
                "is_coinbase": True
            }

            if "txinwitness" in vin:
                input_data["witness"] = vin["txinwitness"]

            if "coinbase" not in vin:
                coinbase = False
                
                # Validate value exists in vin
                if "value" not in vin:
                    print(f"WARNING: Esplora.transaction vin[{i}] missing 'value', skipping input amount calculation")
                else:
                    inputs_amount += vin["value"]

                # Validate txid and vout exist in vin
                if "txid" not in vin or "vout" not in vin:
                    print(f"ERROR: Esplora.transaction vin[{i}] missing 'txid' or 'vout': {vin}")
                    continue

                input_data["txid"] = vin["txid"]
                input_data["vout"] = vin["vout"]
                input_data["is_coinbase"] = False
                
                # Validate scriptPubKey exists in vin
                if "scriptPubKey" not in vin:
                    print(f"ERROR: Esplora.transaction vin[{i}] missing 'scriptPubKey': {vin}")
                    continue

                # Validate scriptPubKey structure
                script_pub_key = vin["scriptPubKey"]
                if not isinstance(script_pub_key, dict):
                    print(f"ERROR: Esplora.transaction vin[{i}] 'scriptPubKey' is not a dict: {type(script_pub_key)}")
                    continue

                required_script_keys = ["hex", "asm", "type"]
                for key in required_script_keys:
                    if key not in script_pub_key:
                        print(f"ERROR: Esplora.transaction vin[{i}] 'scriptPubKey' missing key '{key}': {script_pub_key}")
                        continue

                # Validate addresses exist in scriptPubKey
                if "addresses" not in script_pub_key or not isinstance(script_pub_key["addresses"], list) or len(script_pub_key["addresses"]) == 0:
                    print(f"ERROR: Esplora.transaction vin[{i}] 'scriptPubKey' missing or invalid 'addresses': {script_pub_key}")
                    continue

                input_data["prevout"] = {
                    "scriptpubkey": script_pub_key["hex"],
                    "scriptpubkey_asm": script_pub_key["asm"],
                    "scriptpubkey_type": script_pub_key["type"],
                    "scriptpubkey_address": script_pub_key["addresses"][0],
                    "value": vin["value"] if "value" in vin else 0
                }

            inputs.append(input_data)

        for j, vout in enumerate(result["vout"]):
            # Validate each vout entry
            if not isinstance(vout, dict):
                print(f"ERROR: Esplora.transaction vout[{j}] is not a dict: {type(vout)}")
                continue

            # Validate value exists in vout
            if "value" not in vout:
                print(f"WARNING: Esplora.transaction vout[{j}] missing 'value', using 0")
                vout_value = 0
            else:
                vout_value = vout["value"]
                outputs_amount += vout_value

            output_data = {
                "scriptpubkey": "",
                "scriptpubkey_asm": "",
                "scriptpubkey_type": "",
                "value": 0
            }

            # Validate scriptPubKey exists in vout
            if "scriptPubKey" not in vout:
                print(f"ERROR: Esplora.transaction vout[{j}] missing 'scriptPubKey': {vout}")
                continue

            # Validate scriptPubKey structure
            script_pub_key = vout["scriptPubKey"]
            if not isinstance(script_pub_key, dict):
                print(f"ERROR: Esplora.transaction vout[{j}] 'scriptPubKey' is not a dict: {type(script_pub_key)}")
                continue

            # Set default values and validate keys
            output_data["scriptpubkey"] = script_pub_key.get("hex", "")
            output_data["scriptpubkey_asm"] = script_pub_key.get("asm", "")
            output_data["scriptpubkey_type"] = script_pub_key.get("type", "")

            if "addresses" in script_pub_key and isinstance(script_pub_key["addresses"], list) and len(script_pub_key["addresses"]) > 0:
                output_data["scriptpubkey_address"] = script_pub_key["addresses"][0]
            
            output_data["value"] = vout_value

            if output_data["scriptpubkey_type"] == "nulldata":
                output_data["scriptpubkey_type"] = "op_return"

            outputs.append(output_data)

        if not coinbase:
            fee = inputs_amount - outputs_amount

        if "blockhash" in result:
            status["confirmed"] = True
            # Validate height and blocktime exist if blockhash is present
            if "height" not in result:
                print(f"WARNING: Esplora.transaction result has 'blockhash' but missing 'height'")
            else:
                status["block_height"] = result["height"]
                
            status["block_hash"] = result["blockhash"]
            
            if "blocktime" not in result:
                print(f"WARNING: Esplora.transaction result has 'blockhash' but missing 'blocktime'")
            else:
                status["block_time"] = result["blocktime"]

        # Determine weight based on available fields
        if "weight" in result:
            weight = result["weight"]
        elif "vsize" in result:
            weight = result["vsize"]
        else:
            # Calculate a default weight if neither is available
            print(f"WARNING: Esplora.transaction result missing both 'weight' and 'vsize', using size as fallback")
            weight = result["size"]

        return {
            "txid": result["txid"],
            "version": result["version"],
            "locktime": result["locktime"],
            "size": result["size"],
            "weight": weight,
            "fee": fee,
            "vin": inputs,
            "vout": outputs,
            "status": status,
            "value": outputs_amount
        }
