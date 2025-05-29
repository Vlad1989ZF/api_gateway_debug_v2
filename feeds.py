# feeds.py
import time
import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("feeds")
logger.setLevel(logging.INFO)

def fetch_pump():
    out = []
    try:
        r = requests.get("https://pump.fun/api/trending", timeout=10)
        r.raise_for_status()
        data = r.json()
        for item in data:
            out.append({
                "symbol": item["symbol"],
                "name":   item.get("name", item["symbol"]),
                "pump_score": item.get("score", 0),
                "timestamp":  item.get("timestamp", int(time.time()))
            })
        logger.info(f"[Pump] fetched {len(out)} items")
    except Exception as e:
        logger.warning(f"[Pump] fetch error: {e}")
    return out

def fetch_dex():
    out = []
    try:
        url = "https://api.dexscreener.io/latest/dex/pairs/solana"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        pairs = r.json().get("pairs", [])
        for p in pairs:
            base = p.get("baseToken", {})
            out.append({
                "symbol":       base.get("symbol", ""),
                "name":         base.get("name", base.get("symbol", "")),
                "dex_liquidity": p.get("liquidity", {}).get("usd", 0),
                "dex_marketcap": p.get("fdv", 0),
                "dex_boosts":    p.get("boosts", 0),
                "timestamp":     int(time.time())
            })
        logger.info(f"[Dex] fetched {len(out)} items")
    except Exception as e:
        logger.warning(f"[Dex] fetch error: {e}")
    return out

def fetch_axiom():
    out = []
    try:
        r = requests.get("https://public-api.axiom.trade/solana/recent", timeout=10)
        r.raise_for_status()
        data = r.json()
        for item in data:
            out.append({
                "symbol":       item.get("symbol",""),
                "name":         item.get("name",""),
                "axiom_score":  item.get("score",0),
                "timestamp":    int(time.time())
            })
        logger.info(f"[Axiom] fetched {len(out)} items")
    except Exception as e:
        logger.warning(f"[Axiom] fetch error: {e}")
    return out

def fetch_gagn():
    out = []
    try:
        r = requests.get("https://api.gagn.ai/solana/metrics", timeout=10)
        r.raise_for_status()
        data = r.json()
        for item in data:
            out.append({
                "symbol":      item.get("symbol",""),
                "name":        item.get("name",""),
                "top10_ratio": item.get("top10_pct",""),
                "no_owner":    item.get("no_rug", False),
                "burned":      item.get("burned", False),
                "frozen":      item.get("no_freeze", False),
                "timestamp":   int(time.time())
            })
        logger.info(f"[GAGN] fetched {len(out)} items")
    except Exception as e:
        logger.warning(f"[GAGN] fetch error: {e}")
    return out

def get_all_data():
    merged = {}
    for fn in (fetch_pump, fetch_dex, fetch_axiom, fetch_gagn):
        for item in fn():
            sym = item.get("symbol")
            if not sym:
                continue
            # 同一个 symbol 的字段累加到一个 dict
            merged.setdefault(sym, {}).update(item)
    result = list(merged.values())
    logger.info(f"[Aggregator] returning {len(result)} total items")
    return result
