import requests
from config import RUGCHECK_API, SOLANA_SNIFFER_API

def format_token_alert(token, source):
    symbol = token.get("symbol") or token.get("ticker") or "?"
    name = token.get("name") or token.get("tokenName") or "?"
    price = token.get("price_usd") or token.get("price") or "?"
    address = token.get("address") or token.get("tokenAddress") or "?"
    market_cap = token.get("market_cap") or token.get("marketCap") or "?"
    volume = token.get("volume_24h") or token.get("volume24h") or "?"

    return (f"✅ New SAFE Token on {source.upper()}\n"
            f"**Name**: {name}\n"
            f"**Ticker**: ${symbol}\n"
            f"**Price**: ${price}\n"
            f"**Market Cap**: ${market_cap}\n"
            f"**24h Volume**: ${volume}\n"
            f"**Address**: `{address}`")

def is_safe_token(address):
    try:
        rugcheck_score = requests.get(RUGCHECK_API.format(address)).json().get("safety_score", 0)
        sniffer_score = requests.get(SOLANA_SNIFFER_API.format(address)).json().get("safety_score", 0)
        average_score = (rugcheck_score + sniffer_score) / 2
        return average_score >= 85
    except Exception as e:
        print(f"Safety check error for {address}: {e}")
        return False
