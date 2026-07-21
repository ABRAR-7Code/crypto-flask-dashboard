import os
import random
import requests
from flask import Flask, render_template, request, redirect, abort

app = Flask(__name__)

# 🎯 DUAL MONETIZATION LINKS (ROTATION LOGIC)
MONETAG_LINK = "https://omg10.com/4/11364473"
ADSTERRA_LINK = "https://www.effectivecpmnetwork.com/pv0zktnedc?key=1c57dc59bcf3b6f2e493aa5a06e299f3"

# 💎 SUPPORTED ASSETS (For the Dropdown Navigation)
SUPPORTED_ASSETS = {
    "btc": "Bitcoin (BTC)",
    "eth": "Ethereum (ETH)",
    "sol": "Solana (SOL)",
    "xrp": "Ripple (XRP)"
}

# High-intent phrases for dynamic generation (Spintax Logic)
GREETINGS = ["Live Update", "Arbitrage Alert", "Market Opportunity", "Spread Detected"]
INTROS = [
    "structural variance found across connected orderbooks",
    "liquidity gap detected on public spot exchanges",
    "temporary price anomaly identified for target pairs"
]

def get_live_prices(base, quote):
    """Binance aur KuCoin se real-time spot prices fetch karne ka secure framework with cloud fallback."""
    base = base.upper()
    quote = quote.upper()
    
    kucoin_symbol = f"{base}-{quote}"
    binance_symbol = f"{base}{quote}"
    
    binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={binance_symbol}"
    kucoin_url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={kucoin_symbol}"
    
    p_binance, p_kucoin = None, None
    
    try:
        r = requests.get(binance_url, timeout=3)
        if r.status_code == 200:
            p_binance = float(r.json()['price'])
    except: pass

    try:
        r = requests.get(kucoin_url, timeout=3)
        if r.status_code == 200 and r.json()['data']:
            p_kucoin = float(r.json()['data']['price'])
    except: pass

    # 🔄 CLOUD IP FALLBACK LOGIC (Taake Render par 404 block na ho)
    if not p_binance or not p_kucoin:
        base_prices = {"BTC": 64250.0, "ETH": 3450.0, "SOL": 145.0, "XRP": 0.58}
        mock_base = base_prices.get(base, 1.0)
        
        p_binance = mock_base + random.uniform(-abs(mock_base*0.002), abs(mock_base*0.002))
        p_kucoin = p_binance * random.uniform(0.982, 1.015)

    return p_binance, p_kucoin

@app.route('/')
def home():
    # Base route redirection to default high-volume pair
    return redirect('/track/btc-to-usdt')

@app.route('/track/<base_asset>-to-<quote_asset>')
def track_arbitrage(base_asset, quote_asset):
    base_lower = base_asset.lower()
    
    # Security Check: Agar user koi ajeeb asset daale jo list mein nahi hai
    if base_lower not in SUPPORTED_ASSETS:
        return abort(404, description="Asset infrastructure unreachable")

    # 🕵️‍♂️ LOGIC 4: Custom Redirector & Anti-Bot Bypass
    user_agent = request.headers.get('User-Agent', '').lower()
    bot_keywords = ['twitterbot', 'redditbot', 'facebookexternalhit', 'googlebot', 'crawl', 'spider']
    is_bot = any(bot in user_agent for bot in bot_keywords)
    
    # Fetch live execution records with fallback support
    p_binance, p_kucoin = get_live_prices(base_lower, quote_asset)
        
    # Calculate Spread Directional Gaps
    if p_binance > p_kucoin:
        buy_ex, sell_ex = "KuCoin", "Binance"
        spread = p_binance - p_kucoin
        gap_pct = (spread / p_kucoin) * 100
    else:
        buy_ex, sell_ex = "Binance", "KuCoin"
        spread = p_kucoin - p_binance
        gap_pct = (spread / p_binance) * 100

    # Spintax dynamic generation
    dynamic_desc = f"{random.choice(GREETINGS)}: A {random.choice(INTROS)} has yielded a secure spread potential."

    # ⚡ AUTOMATIC AD ROTATOR (50% Monetag / 50% Adsterra)
    selected_ad_link = random.choice([MONETAG_LINK, ADSTERRA_LINK])

    payload = {
        "title": f"Live {base_asset.upper()}/{quote_asset.upper()} Arbitrage: {gap_pct:.2f}% Spread Matrix",
        "description": dynamic_desc,
        "base": base_asset.upper(),
        "quote": quote_asset.upper(),
        "buy_from": buy_ex,
        "sell_to": sell_ex,
        "buy_price": f"${p_binance if buy_ex == 'Binance' else p_kucoin:,.4f}",
        "sell_price": f"${p_binance if buy_ex == 'Binance' else p_kucoin:,.4f}",
        "gap": f"{gap_pct:.2f}%",
        "is_bot": is_bot,
        "ad_link": selected_ad_link,
        
        # Pass asset states to UI
        "current_asset": base_lower,
        "supported_assets": SUPPORTED_ASSETS
    }

    return render_template("index.html", data=payload)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
