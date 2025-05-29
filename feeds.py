import time
import requests

def fetch_dex():
    url = "https://api.dexscreener.com/latest/dex/search/?q=solana"
    out = []
    try:
        data = requests.get(url, timeout=10).json().get("pairs", [])
        for p in data:
            base = p.get("baseToken", {})
            out.append({
                "symbol": base.get("symbol", ""),
                "name": base.get("name", ""),
                "dex_liquidity": p.get("liquidity", {}).get("usd", ""),
                "dex_marketcap": p.get("fdv", ""),
                "dex_volume": p.get("volume", {}).get("h24", ""),
                "timestamp": int(time.time())
            })
    except Exception as e:
        print(f"[Dex] fetch error: {e}")
    return out

def get_all_data():
    merged = {}
    for fetch in (fetch_dex,):
        for item in fetch():
            sym = item.get("symbol")
            if not sym: continue
            merged.setdefault(sym, {}).update(item)
    return list(merged.values())
