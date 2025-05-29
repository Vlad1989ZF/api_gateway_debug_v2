import time
import requests
from bs4 import BeautifulSoup

def fetch_pump():
    url = "https://pump.fun/api/trending"  # 修正后的API路径
    out = []
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        for item in data:
            name = item.get("tokenName") or item.get("name", "")
            score = item.get("score", 0)
            out.append({
                "symbol": name,
                "name": name,
                "pump_score": score,
                "timestamp": int(time.time())
            })
    except Exception as e:
        print(f"[Pump] fetch error: {e}")
    return out

def fetch_dex():
    url = "https://api.dexscreener.com/latest/dex/pairs/solana"
    out = []
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json().get("pairs", [])
        for p in data:
            base = p.get("baseToken", {})
            out.append({
                "symbol": base.get("symbol", ""),
                "name": base.get("name", ""),
                "dex_liquidity": p.get("liquidity", {}).get("usd", ""),
                "dex_marketcap": p.get("fdv", ""),
                "dex_boosts": p.get("boosts", 0),
                "timestamp": int(time.time())
            })
    except Exception as e:
        print(f"[Dex] fetch error: {e}")
    return out

def get_all_data():
    merged = {}
    for fetch in (fetch_pump, fetch_dex):
        for item in fetch():
            sym = item.get("symbol")
            if not sym: continue
            merged.setdefault(sym, {}).update(item)
    return list(merged.values())
