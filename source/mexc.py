import requests
import time
import config

class MEXCAPI:
  def __init__(self):
    self.max_requests_per_sec = config.MEXC_MRPS
    self.requests_made = 0
    self.start_time = time.time()

  def get_spot_price(self, symbol):
    current_time = time.time()
    elapsed_time = current_time - self.start_time

    if elapsed_time < 1:
      if self.requests_made >= self.max_requests_per_sec:
        sleep_time = 1 - elapsed_time
        time.sleep(sleep_time)
        self.start_time = time.time()
        self.requests_made = 0
    else:
      self.start_time = current_time
      self.requests_made = 0

    try:
      url = f"https://www.mexc.com/open/api/v2/market/ticker?symbol={symbol}"
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()
      self.requests_made += 1
      return float(data['data'][0]['last'])
    except Exception as e:
      print(f"An error occurred: {e}")
      return None

  def get_spot_symbol(self, base, quote):
    return base.upper() + '_' + quote.upper()

if __name__ == "__main__":
  mexc_api = MEXCAPI()
  symbol = mexc_api.get_spot_symbol('BTC', 'USDT')
  price = mexc_api.get_spot_price(symbol)
  if price:
    print(f"The spot price for {symbol} is {price}")
  else:
    print("Failed to fetch the spot price.")
