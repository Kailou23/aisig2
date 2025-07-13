
import ccxt
import pandas as pd
import pandas_ta as ta
import requests
import time

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram error:", e)

def get_signal(symbol):
    try:
        exchange = ccxt.binance()
        bars = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=100)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        df.set_index('time', inplace=True)
        df['ema20'] = ta.ema(df['close'], length=20)
        df['rsi'] = ta.rsi(df['close'], length=14)
        last = df.iloc[-1]
        if last['close'] > last['ema20'] and last['rsi'] < 70:
            return f"🔔 BUY Signal on {symbol} | Price: {last['close']:.2f} | RSI: {last['rsi']:.2f}"
        elif last['close'] < last['ema20'] and last['rsi'] > 30:
            return f"⚠️ SELL Signal on {symbol} | Price: {last['close']:.2f} | RSI: {last['rsi']:.2f}"
    except Exception as e:
        return f"Error processing {symbol}: {e}"
    return None

SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"]

while True:
    for symbol in SYMBOLS:
        signal = get_signal(symbol)
        if signal:
            print(signal)
            send_telegram(signal)
        else:
            print(f"{symbol} skipped — no signal.")
    print("⏱️ Sleeping 10 minutes...")
    time.sleep(600)
