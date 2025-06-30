import yfinance as yf

def get_current_price(symbol):
    try:
        if not symbol.endswith(".NS") and len(symbol) <= 5:
            symbol += ".NS"
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        current_price = data["Close"].iloc[-1]
        return round(current_price, 2)
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

