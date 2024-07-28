import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QThread, pyqtSignal

import huobi
import okx
import binance
import mexc

class PriceUpdateThread(QThread):
  updated = pyqtSignal(dict)

  def __init__(self, base, quote):
    super().__init__()
    self.base = base
    self.quote = quote
    self.prices = {
      'Binance': {'pair': f'{base}/{quote}', 'price': 0.0},
      'Huobi': {'pair': f'{base}/{quote}', 'price': 0.0},
      'OKX': {'pair': f'{base}/{quote}', 'price': 0.0},
      'MEXC': {'pair': f'{base}/{quote}', 'price': 0.0},
    }
    self.exchanges = {
      'Binance': binance.BinanceAPI(),
      'Huobi': huobi.HuobiAPI(),
      'OKX': okx.OKXAPI(),
      'MEXC': mexc.MEXCAPI()
    }
    self.running = True

  def run(self):
    while self.running:
      for exchange in self.prices:
        ticker = self.exchanges[exchange].get_spot_symbol(self.base, self.quote)
        price = self.exchanges[exchange].get_spot_price(ticker)
        self.prices[exchange]['price'] = price if price is not None else '-'
        self.updated.emit(self.prices)

  def stop(self):
    self.running = False

class CryptoPriceDisplay(QWidget):
  def __init__(self, base, quote):
    super().__init__()
    self.base = base
    self.quote = quote
    self.initUI()
    self.price_thread = PriceUpdateThread(base, quote)
    self.price_thread.updated.connect(self.update_table)
    self.price_thread.start()

  def initUI(self):
    self.setWindowTitle(f'Crypto Prices - {self.base}/{self.quote}')
    self.setGeometry(100, 100, 1000, 300)

    self.layout = QVBoxLayout()
    self.table = QTableWidget()
    self.table.setColumnCount(5)
    self.table.setHorizontalHeaderLabels(['Exchange', 'Pair', 'Price', 'Delta', 'Delta (%)'])
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.layout.addWidget(self.table)

    self.setLayout(self.layout)

    self.setStyleSheet("""
      QWidget {
        background-color: #2E2E2E;
        color: #FFFFFF;
      }
      QTableWidget {
        gridline-color: #444444;
      }
      QHeaderView::section {
        background-color: #444444;
        color: #FFFFFF;
        padding: 4px;
        border: 1px solid #6c6c6c;
      }
      QTableWidgetItem {
        color: #FFFFFF;
      }
    """)

  def update_table(self, prices):
    sorted_prices = sorted(prices.items(), key=lambda x: float(x[1]['price']) if x[1]['price'] != '-' else float('-inf'), reverse=True)
    self.table.setRowCount(len(sorted_prices))

    if sorted_prices:
      top_price = next((x[1]['price'] for x in sorted_prices if x[1]['price'] != '-'), None)
      top_price = float(top_price) if top_price is not None else None

      for row, (exchange, data) in enumerate(sorted_prices):
        self.table.setItem(row, 0, QTableWidgetItem(exchange))
        self.table.setItem(row, 1, QTableWidgetItem(data['pair']))
        self.table.setItem(row, 2, QTableWidgetItem(f"{data['price']:.10f}" if data['price'] != '-' else '-'))
        if top_price is not None and data['price'] != '-':
          delta = top_price - float(data['price'])
          delta_percent = (delta / top_price) * 100 if top_price != 0 else 0
          self.table.setItem(row, 3, QTableWidgetItem(f"{delta:.10f}"))
          self.table.setItem(row, 4, QTableWidgetItem(f"{delta_percent:.2f}%"))
        else:
          self.table.setItem(row, 3, QTableWidgetItem('-'))
          self.table.setItem(row, 4, QTableWidgetItem('-'))

  def closeEvent(self, event):
    self.price_thread.stop()
    self.price_thread.wait()

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Usage: python arb.py <BASE> <QUOTE>")
    sys.exit(1)

  base_currency = sys.argv[1].upper()
  quote_currency = sys.argv[2].upper()

  app = QApplication(sys.argv)
  display = CryptoPriceDisplay(base_currency, quote_currency)
  display.show()
  sys.exit(app.exec_())
