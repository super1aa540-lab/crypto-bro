import ccxt
import pandas as pd
import pandas_ta as ta
import time
import requests
from threading import Thread
from flask import Flask

app = Flask(__name__)

# Flask Server (Render အတွက် Port ပေးထားခြင်း)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- Trading Bot Logic ---
TELEGRAM_TOKEN = "8625385968:AAHpcmv0AhsNyEw8WcOaqciKk1XE0zBioc8"
CHAT_ID = "5425783496"
SYMBOLS = ['SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'ETH/USDT']

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(url)

def check_signals():
    exchange = ccxt.binance()
    for symbol in SYMBOLS:
        try:
            bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=50)
            df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            st = df.ta.supertrend(length=10, multiplier=3.0)
            if st.iloc[-1]['SUPERTd_10_3.0'] == 1 and st.iloc[-2]['SUPERTd_10_3.0'] == -1:
                send_telegram(f"🚀 Buy Signal: {symbol} (1H)")
            elif st.iloc[-1]['SUPERTd_10_3.0'] == -1 and st.iloc[-2]['SUPERTd_10_3.0'] == 1:
                send_telegram(f"📉 Sell Signal: {symbol} (1H)")
        except: pass

def run_bot():
    while True:
        check_signals()
        time.sleep(3600)

if __name__ == "__main__":
    # Flask နဲ့ Bot ကို တစ်ပြိုင်တည်း Run မယ်
    Thread(target=run_flask).start()
    run_bot()

