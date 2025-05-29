import time
import requests
from bs4 import BeautifulSoup

def fetch_pump():
    url = "https://pump.fun/trending"
    out = []
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        for card in soup.select(".token-card"):
            name = card.select_one(".token-name").get_text(strip=True)
            score = int(card.select_one(".token-score").get_text(strip=True))
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
        data = requests.get(url, timeout=10).json().get("pairs", [])
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

def fetch_axiom():
    out = []
    try:
        resp = requests.get("https://api.axiom.trade/solana/recent", timeout=10)
        data = resp.json()
        for item in data:
            out.append({
                "symbol": item.get("symbol", ""),
                "name": item.get("name", ""),
                "axiom_score": item.get("score", 0),
                "timestamp": int(time.time())
            })
    except Exception as e:
        print(f"[Axiom] fetch error: {e}")
    return out

def fetch_gagn():
    out = []
    try:
        resp = requests.get("https://api.gagn.ai/solana/metrics", timeout=10)
        data = resp.json()
        for item in data:
            out.append({
                "symbol": item.get("symbol", ""),
                "name": item.get("name", ""),
                "top10_ratio": item.get("top10_pct", ""),
                "no_owner": item.get("no_rug", False),
                "burned": item.get("burned", False),
                "frozen": item.get("no_freeze", False),
                "timestamp": int(time.time())
            })
    except Exception as e:
        print(f"[GAGN] fetch error: {e}")
    return out

def get_all_data():
    merged = {}
    for fetch in (fetch_pump, fetch_dex, fetch_axiom, fetch_gagn):
        for item in fetch():
            sym = item.get("symbol")
            if not sym: continue
            merged.setdefault(sym, {}).update(item)
    return list(merged.values())
