import requests
import time

import config

class BinanceAPI:
  def __init__(self):
    self.max_requests_per_sec = config.BINANCE_MRPS
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
      url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()
      self.requests_made += 1
      return float(data['price'])
    except Exception as e:
      print(f"An error occurred: {e}")
      return None

  def get_spot_symbol(self, base, quote):
    return base.upper() + quote.upper()

# symbol = 'BTCUSDT'