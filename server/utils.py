import config
import math
import json
import requests
import socket
import hashlib
from datetime import datetime, timedelta

RPC_TIMEOUT_SECONDS = getattr(config, "rpc_timeout", 10)
MARKET_TIMEOUT_SECONDS = getattr(config, "market_timeout", 10)
ELECTRUMX_HOST = getattr(config, "electrumx_host", "45.148.31.13")
ELECTRUMX_PORT = int(getattr(config, "electrumx_port", 50001))
ELECTRUMX_TIMEOUT_SECONDS = float(getattr(config, "electrumx_timeout", 10))
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE58_ALPHABET_MAP = {character: index for index, character in enumerate(BASE58_ALPHABET)}

ROD_PRE_RELEASE_BLOCKS = 55560
ROD_PRE_RELEASE_REWARD = 1.0
ROD_STANDARD_REWARD = 800.0
ROD_HALVING_INTERVAL = 1054080
ROD_HALVING_PERIODS = 5
ROD_ANNUAL_INFLATION = 0.03
ROD_POST_HALVING_YEARS = 59
ROD_SECONDS_PER_BLOCK = 30
ROD_BLOCKS_PER_YEAR = int((365 * 24 * 60 * 60) / ROD_SECONDS_PER_BLOCK)
ROD_MAX_SUPPLY = 4615066365


def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}

def response(result, error=None, rid=config.rid):
    return {"error": error, "id": rid, "result": result}

def make_request(method, params=None):
    if params is None:
        params = []

    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(
            config.endpoint,
            headers=headers,
            data=data,
            timeout=RPC_TIMEOUT_SECONDS,
        ).json()
    except Exception:
        return dead_response()

def make_electrumx_request(method, params=None):
    if params is None:
        params = []

    payload = json.dumps({"id": config.rid, "method": method, "params": params}) + "\n"

    try:
        with socket.create_connection((ELECTRUMX_HOST, ELECTRUMX_PORT), timeout=ELECTRUMX_TIMEOUT_SECONDS) as electrumx_socket:
            electrumx_socket.settimeout(ELECTRUMX_TIMEOUT_SECONDS)
            return _electrumx_send_request(electrumx_socket, payload)
    except Exception:
        return dead_response("ElectrumX request failed")

def make_electrumx_batch_request(method, params_list):
    try:
        with socket.create_connection((ELECTRUMX_HOST, ELECTRUMX_PORT), timeout=ELECTRUMX_TIMEOUT_SECONDS) as electrumx_socket:
            electrumx_socket.settimeout(ELECTRUMX_TIMEOUT_SECONDS)
            responses = []
            for params in params_list:
                payload = json.dumps({"id": config.rid, "method": method, "params": params}) + "\n"
                responses.append(_electrumx_send_request(electrumx_socket, payload))
            return responses
    except Exception:
        return []

def _electrumx_send_request(electrumx_socket, payload):
    electrumx_socket.sendall(payload.encode("utf-8"))

    received_chunks = []
    while True:
        chunk = electrumx_socket.recv(4096)
        if not chunk:
            break
        received_chunks.append(chunk)
        if b"\n" in chunk:
            break

    if not received_chunks:
        return dead_response("ElectrumX empty response")

    response_line = b"".join(received_chunks).split(b"\n", 1)[0].decode("utf-8")
    response_json = json.loads(response_line)
    if "error" not in response_json:
        response_json["error"] = None
    if "id" not in response_json:
        response_json["id"] = config.rid
    return response_json

def address_to_electrum_scripthash(address):
    normalized = address.strip() if isinstance(address, str) else ""
    if not normalized:
        raise ValueError("Invalid address")

    if normalized.startswith("rod1"):
        raise ValueError("Unsupported address format: Bech32 (rod1)")

    decoded = _base58check_decode(normalized)
    version = decoded[0]
    payload = decoded[1:]

    if version == 60:
        script_pubkey = bytes.fromhex("76a914") + payload + bytes.fromhex("88ac")
    elif version == 75:
        script_pubkey = bytes.fromhex("a914") + payload + bytes.fromhex("87")
    else:
        raise ValueError("Unsupported address prefix")

    script_hash = hashlib.sha256(script_pubkey).digest()[::-1].hex()
    return script_hash

def _base58check_decode(value):
    decoded_number = 0
    for character in value:
        decoded_number *= 58
        if character not in BASE58_ALPHABET_MAP:
            raise ValueError("Invalid base58 character")
        decoded_number += BASE58_ALPHABET_MAP[character]

    full_data = decoded_number.to_bytes((decoded_number.bit_length() + 7) // 8, byteorder="big")
    leading_zeros = len(value) - len(value.lstrip("1"))
    full_data = (b"\x00" * leading_zeros) + full_data

    if len(full_data) < 5:
        raise ValueError("Invalid address length")

    payload, checksum = full_data[:-4], full_data[-4:]
    expected_checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    if checksum != expected_checksum:
        raise ValueError("Invalid address checksum")

    if len(payload) != 21:
        raise ValueError("Unsupported address payload length")

    return payload

def reward(height):
    if height <= 0:
        return 0
    if height <= ROD_PRE_RELEASE_BLOCKS:
        return satoshis(ROD_PRE_RELEASE_REWARD)

    effective_height = height - ROD_PRE_RELEASE_BLOCKS
    halving_index = (effective_height - 1) // ROD_HALVING_INTERVAL

    if halving_index < ROD_HALVING_PERIODS:
        current_reward = ROD_STANDARD_REWARD / (2 ** halving_index)
        return satoshis(current_reward)

    years_after_halving = (effective_height - (ROD_HALVING_INTERVAL * ROD_HALVING_PERIODS)) / ROD_BLOCKS_PER_YEAR
    inflation_multiplier = (1 + ROD_ANNUAL_INFLATION) ** max(0.0, years_after_halving)
    inflationary_reward = (ROD_STANDARD_REWARD / (2 ** ROD_HALVING_PERIODS)) * inflation_multiplier
    return satoshis(inflationary_reward)

def reward2(blockHeight):
    return format(amount(reward(blockHeight)), '.8f')

def supply(height):
    if height <= 0:
        return {
            "halvings": 0,
            "supply": 0,
            "total/max supply": satoshis(ROD_MAX_SUPPLY),
            "policy": "spacexpanse-rod",
            "inflation_model": "approximate_3_percent_annual_post_halving",
        }

    total_supply = 0.0
    remaining_blocks = int(height)

    pre_release_blocks = min(remaining_blocks, ROD_PRE_RELEASE_BLOCKS)
    total_supply += pre_release_blocks * ROD_PRE_RELEASE_REWARD
    remaining_blocks -= pre_release_blocks

    completed_halvings = 0
    for halving_index in range(ROD_HALVING_PERIODS):
        if remaining_blocks <= 0:
            break
        phase_blocks = min(remaining_blocks, ROD_HALVING_INTERVAL)
        phase_reward = ROD_STANDARD_REWARD / (2 ** halving_index)
        total_supply += phase_blocks * phase_reward
        remaining_blocks -= phase_blocks
        if phase_blocks == ROD_HALVING_INTERVAL:
            completed_halvings = halving_index + 1

    if remaining_blocks > 0:
        inflationary_base_reward = ROD_STANDARD_REWARD / (2 ** ROD_HALVING_PERIODS)

        for year_index in range(ROD_POST_HALVING_YEARS):
            if remaining_blocks <= 0:
                break
            blocks_this_year = min(remaining_blocks, ROD_BLOCKS_PER_YEAR)
            inflationary_reward = inflationary_base_reward * ((1 + ROD_ANNUAL_INFLATION) ** year_index)
            total_supply += blocks_this_year * inflationary_reward
            remaining_blocks -= blocks_this_year

        if remaining_blocks > 0:
            final_year_reward = inflationary_base_reward * ((1 + ROD_ANNUAL_INFLATION) ** (ROD_POST_HALVING_YEARS - 1))
            total_supply += remaining_blocks * final_year_reward

    return {
        "halvings": int(completed_halvings),
        "supply": satoshis(total_supply),
        "total/max supply": satoshis(ROD_MAX_SUPPLY),
        "policy": "spacexpanse-rod",
        "inflation_model": "approximate_3_percent_annual_post_halving",
    }

def satoshis(value):
    return math.ceil(value * math.pow(10, 8))

def amount(value):
    return round(value / math.pow(10, 8), 8)

def is_plausible_rod_address(address):
    if not isinstance(address, str):
        return False

    normalized = address.strip()
    if len(normalized) < 26 or len(normalized) > 90:
        return False

    if normalized.startswith("rod1"):
        return True

    return normalized.startswith("R")

def getprice():
    coin_name = "spacexpanse"
    coin_paprika_id = "rod-spacexpanse"

    btc = 0.0
    usd = 0.0
    msg = "Error market cap connection"

    try:
        price = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_name}&vs_currencies=usd,btc",
            timeout=MARKET_TIMEOUT_SECONDS,
        ).json()
        if isinstance(price, dict) and coin_name in price:
            btc = float(price[coin_name].get("btc", 0) or 0)
            usd = float(price[coin_name].get("usd", 0) or 0)
            msg = "Active"
    except Exception:
        pass

    if msg != "Active":
        try:
            price2 = requests.get(
                f"https://api.coinpaprika.com/v1/tickers/{coin_paprika_id}",
                timeout=MARKET_TIMEOUT_SECONDS,
            ).json()
            if isinstance(price2, dict):
                quotes = price2.get("quotes", {}).get("USD", {})
                usd = float(quotes.get("price", 0) or 0)
                btc = float(price2.get("price_btc", 0) or 0)
                if usd > 0 or btc > 0:
                    msg = "Active"
        except Exception:
            pass

    return {
        "price_btc": ('%.8f' % btc),
        "price_usd": ('%.8f' % usd),
        "status": msg
    }

