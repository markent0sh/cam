# Crypto Arbitrage Monitor

## Overview

**CAM** displays real-time prices for specified cryptocurrency pairs from multiple exchanges (Binance, Huobi, OKX, MEXC). It updates and displays the prices, along with delta and delta percentage.

## Features

- Fetches real-time cryptocurrency prices from multiple exchanges.
- Displays prices, delta, and delta percentage.
- Dark-themed interface using PyQt5.
- Handles absent listing by displaying `'-'`.

## Requirements

- Python 3.x
- PyQt5
- requests

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/markent0sh/cam.git
   cd cam
   ```
2. Install the required packages:

   ```sh
   pip install PyQt5 requests
   ```
3. Modify a `config.py` file with the following content:

   ```python
   OKX_MRPS = 5
   MEXC_MRPS = 5
   ```

## Usage

Run the application with the desired base and quote currencies:

```python
python source/main.py <BASE> <QUOTE>
```

For example:

```
python source/main.py ETH USDT
```

## Code Structure

- **main.py**: Contains the main application code.
- **binance.py, huobi.py, okx.py, mexc.py**: Modules for fetching prices from respective exchanges.
- **config.py**: Configuration file for rate limits.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
