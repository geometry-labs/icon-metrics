import json

import requests

from icon_metrics.config import settings
from icon_metrics.log import logger


def post_rpc(payload: dict):
    r = requests.post(settings.ICON_NODE_URL, data=json.dumps(payload))

    if r.status_code != 200:
        logger.info(f"Error {r.status_code} with payload {payload}")
        r = requests.post(settings.BACKUP_ICON_NODE_URL, data=json.dumps(payload))
        if r.status_code != 200:
            logger.info(f"Error {r.status_code} with payload {payload} to backup")
            return
        return r.json()["result"]

    # x = int(r.json()["result"], 16)

    return r.json()["result"]


def icx_getTransactionResult(txHash: str):
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_getTransactionResult",
        "id": 1234,
        "params": {"txHash": txHash},
    }
    return post_rpc(payload)


def getPReps():
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {
                "method": "getPReps",
                "params": {"startRanking": "0x1", "endRanking": "0xaaa"},
                # Should be all preps
            },
        },
    }
    return post_rpc(payload)


def getBalance(address: str):
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_getBalance",
        "id": 1234,
        "params": {"address": address},
    }
    return post_rpc(payload)


def getStake(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {
                "method": "getStake",
                "params": {"address": address},
            },
        },
    }
    return post_rpc(payload)


def getTotalSupply():
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_getTotalSupply",
        "id": 1234,
    }
    return post_rpc(payload)
