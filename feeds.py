import time

def get_all_data():
    # 模拟聚合数据返回结构
    return [{
        "burned": True,
        "frozen": False,
        "liquidity": "$320K",
        "marketcap": "$1.2M",
        "name": "PEPE",
        "no_owner": True,
        "score": 85,
        "socials": {
            "telegram": "https://t.me/pepecoin",
            "twitter": "https://twitter.com/pepecoin",
            "website": "https://pepe.com"
        },
        "symbol": "PEPE",
        "timestamp": int(time.time()),
        "top10_ratio": "24%"
    }]
