# Binance Algorithmic Trading Bot using REST APIs

This repository contains a **Python-based algorithmic trading bot** that interacts with the **Binance Futures Testnet**.  
It uses REST APIs to execute trading strategies on the **BTC/USDT** trading pair. The bot monitors market conditions, fetches data, calculates signals based on custom rules (e.g., CryptoQuant data), and automatically places market orders based on the analysis.

---

## Features

- **Automated Trading**: Trades are placed automatically based on signals derived from exchange inflows and outflows.
- **Real-time Market Data**: Fetches real-time futures price data using Binance REST APIs.
- **Customizable Parameters**: Modify trading parameters such as leverage, margin type, buy/sell thresholds, and more.
- **Wallet Management**: Dynamically adjusts position size based on wallet balance.
- **Leverage & Margin Support**: Supports setting custom leverage and cross-margin or isolated-margin modes.
- **Error Handling**: Implements basic error handling for API requests and server time adjustments.

---

## Setup Instructions

### Prerequisites

- Python 3.11.9
- A Binance account (Testnet for development; main account for live trading)
- API keys for Binance Futures (Use testnet API for development and testing)
- Required Python libraries:
  - `requests`
  - `hmac`
  - `hashlib`
  - `datetime`
  - `numpy`

To install the required dependencies, run:

```bash
pip install requests numpy
```

## Getting Binance API Keys

### To trade on Binance Futures Testnet:
1. Sign up for a [Binance Testnet Account](https://testnet.binancefuture.com).
2. Create API keys from your account. Store them safely.

### For real trading:
1. Sign up for a [Binance account](https://www.binance.com).
2. Create API keys from your live account.  
   **Use with caution for real trading**.

---

## Configuration

Clone this repository:

```bash
git clone https://github.com/yourusername/Binance-Algo-Trade-using-REST-APIs.git
cd Binance-Algo-Trade-using-REST-APIs
```

### Update the API keys in the Python script:

```python
BINANCE_API_KEY = 'your_binance_api_key'
BINANCE_SECRET_KEY = 'your_binance_secret_key'
```

### You can modify trading parameters such as:

- **`SYMBOL`**: Trading pair (e.g., `BTCUSDT`)
- **`POSITION_PERCENTAGE`**: Percentage of your wallet balance to trade per position.
- **`LEVERAGE`**: The leverage to use for trades (e.g., `100x`).
- **`TIMEFRAME`**: The timeframe for fetching candles (e.g., `1h`).
- **`INTERVAL_SECONDS`**: The interval at which to check signals (in seconds).

### Running the Bot

To run the bot:

```bash
python binance_algo_trade.py
```

The bot will:

- Fetch your current wallet balance and set up the margin mode and leverage.
- Fetch CryptoQuant-like data (simulated in this version) to calculate buy/sell signals.
- Automatically place market orders based on the signals.
- Run indefinitely, checking for new signals every minute.

### Binance API Endpoints Used

| **Endpoint**                    | **Description**                                      |
|----------------------------------|------------------------------------------------------|
| `GET /fapi/v1/ticker/price`      | Fetches the current futures price.                   |
| `GET /fapi/v1/klines`            | Fetches historical candlestick data.                 |
| `POST /fapi/v1/order`            | Places a market order.                              |
| `POST /fapi/v1/leverage`         | Sets leverage for a specific symbol.                |
| `GET /fapi/v2/account`           | Fetches wallet balance.                             |
| `POST /fapi/v1/marginType`       | Sets cross or isolated margin mode.                 |

### Error Handling

The bot includes basic error handling, such as:

- Retries for failed API requests.
- Checks for mismatches between local time and Binance server time.
- Ensuring margin type and leverage are correctly set before trading.

### Disclaimer

> **Trading cryptocurrencies involves substantial risk, and this bot is meant for educational purposes only.  
> Be cautious when running this on real accounts, and ensure proper risk management strategies are in place.**

---

### Contributing

Feel free to **fork** this repository and make improvements or customizations.  
Pull requests are welcome!

---

### License

This project is licensed under the **Apache License**.

---

**Happy trading!**  
If you encounter any issues, please [raise an issue](#) in the repository or contact me for support.

