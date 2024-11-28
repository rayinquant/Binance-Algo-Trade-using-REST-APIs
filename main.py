import requests
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from datetime import datetime
import numpy as np


# Binance API credentials (use environment variables)
load_dotenv()
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.environ.get('BINANCE_SECRET_KEY')
BASE_URL = 'https://testnet.binancefuture.com'  # Binance Futures API endpoint
CRYPTOQUANT_API_KEY = os.environ.get('CRYPTOQUANT_API_KEY')
CRYPTOQUANT_BASE_URL = 'https://api.cryptoquant.com/v1'  # Replace with actual API base if different


# Trading parameters
SYMBOL = 'BTCUSDT'                 # Binance futures trading symbol
POSITION_PERCENTAGE = 10           # 10% of your wallet balance for position size
BUY_THRESHOLD = 0.6                # Buy threshold for signal
SELL_THRESHOLD = 0.4               # Sell threshold for signal
LEVERAGE = 100                     # Leverage to be used (e.g., 10x)
TIMEFRAME = '1h'                   # Timeframe for the strategy (1-hour)
INTERVAL_SECONDS = 60              # Check interval (1 minute)
MARGIN_TYPE = 'CROSSED'            # 'CROSSED' or 'ISOLATED'

# Generate signature for the request
def generate_signature(query_string, secret_key):
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# Set leverage for a futures symbol
def set_futures_leverage(symbol, leverage):
    endpoint = '/fapi/v1/leverage'
    timestamp = int(time.time() * 1000)

    params = {
        'symbol': symbol,
        'leverage': leverage,
        'timestamp': timestamp
    }

    query_string = urlencode(params)
    signature = generate_signature(query_string, BINANCE_SECRET_KEY)

    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"

    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        print(f"Leverage set to {leverage}x for {symbol}")
    else:
        print(f"Failed to set leverage: {response.status_code} {response.text}")

# Function to get Binance server time
def get_binance_server_time():
    try:
        endpoint = '/fapi/v1/time'
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['serverTime']
        else:
            print(f"Failed to fetch server time: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching server time: {e}")
        return None

# Adjust your timestamp function with server time difference
def get_adjusted_timestamp():
    server_time = get_binance_server_time()
    if server_time:
        local_time = int(time.time() * 1000)
        time_diff = server_time - local_time
        return int(time.time() * 1000 + time_diff)
    else:
        return int(time.time() * 1000)

# Set margin type (Cross or Isolated) for a futures symbol with adjusted timestamp and increased recvWindow
def set_margin_type(symbol, margin_type):
    endpoint = '/fapi/v1/marginType'
    timestamp = get_adjusted_timestamp()

    params = {
        'symbol': symbol,
        'marginType': margin_type,
        'timestamp': timestamp,
        'recvWindow': 60000  # Increased recvWindow to 60 seconds
    }

    query_string = urlencode(params)
    signature = generate_signature(query_string, BINANCE_SECRET_KEY)

    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"

    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }
    if margin_type == 'CROSSED':
        print("Margin type is set to 'CROSSED'")
    else:
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            print(f"Margin mode set to {margin_type} for {symbol}")
        else:
            print(f"Failed to set margin type: {response.status_code} {response.text}")

# Send POST request to create a market order on Binance Futures
def create_futures_market_order(symbol, side, quantity):
    endpoint = '/fapi/v1/order'
    timestamp = int(time.time() * 1000)
    
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
        'timestamp': timestamp
    }

    query_string = urlencode(params)
    signature = generate_signature(query_string, BINANCE_SECRET_KEY)
    
    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
    
    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }

    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Market order placed: {response.json()}")
    else:
        print(f"Failed to place order: {response.status_code} {response.text}")

# Simulated function to fetch CryptoQuant data
def fetch_cryptoquant_data():
    
    endpoint = '/btc/market-data/taker-buy-sell-stats?window=day&exchange=binance'
    params = {
        'window':'day',
        'exchange':'binance'
    }

    url = f"{CRYPTOQUANT_BASE_URL}{endpoint}"
    headers = {
        'X-API-KEY': CRYPTOQUANT_API_KEY
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}, {response.text}')
        return None
    
    # data = {
    #     'exchange_inflow': 500,
    #     'exchange_outflow': 300
    # }
    # return data

# Calculate signal from the CryptoQuant data
def calculate_signal(data):
    exchange_inflow = data['exchange_inflow']
    exchange_outflow = data['exchange_outflow']
    
    signal_strength = exchange_inflow / (exchange_inflow + exchange_outflow)
    
    action = np.where(signal_strength > BUY_THRESHOLD, 'buy',
                      np.where(signal_strength < SELL_THRESHOLD, 'sell', 'hold'))
    
    return action[()], signal_strength

# Fetch the wallet balance from Binance Futures
def get_futures_balance(asset):
    endpoint = '/fapi/v2/account'
    timestamp = int(time.time() * 1000)
    
    params = {
        'timestamp': timestamp
    }
    
    query_string = urlencode(params)
    signature = generate_signature(query_string, BINANCE_SECRET_KEY)
    
    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
    
    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        account_data = response.json()
        for balance in account_data['assets']:
            if balance['asset'] == asset:
                return float(balance['walletBalance'])
    else:
        print(f"Failed to fetch balance: {response.status_code} {response.text}")
        return None

# Fetch the current price of the futures symbol
def get_current_futures_price(symbol):
    endpoint = '/fapi/v1/ticker/price'
    params = {'symbol': symbol}
    url = f"{BASE_URL}{endpoint}"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return float(response.json()['price'])
    else:
        print(f"Failed to fetch price: {response.status_code} {response.text}")
        return None

# Calculate the position size dynamically based on wallet balance
def calculate_position_size(balance):
    current_price = get_current_futures_price(SYMBOL)
    if current_price:
        position_size = round((balance * POSITION_PERCENTAGE) / current_price, 3)
        return position_size
    return None

# Fetch 1-hour candles from Binance Futures
def get_futures_candles(symbol, interval):
    endpoint = '/fapi/v1/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1
    }
    url = f"{BASE_URL}{endpoint}"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Main trading function
def main():
    last_candle_time = None

    # Set leverage and margin type before trading
    set_futures_leverage(SYMBOL, LEVERAGE)
    set_margin_type(SYMBOL, MARGIN_TYPE)

    # Fetch the USDT wallet balance
    usdt_balance = get_futures_balance('USDT')
    
    if usdt_balance is not None:
        print(f"Current wallet balance (USDT): {usdt_balance}")
    else:
        print("Failed to fetch wallet balance.")
        return  # Exit if unable to get the wallet balance

    while True:
        candles = get_futures_candles(SYMBOL, TIMEFRAME)

        if candles:
            latest_candle = candles[-1]
            candle_time = datetime.fromtimestamp(latest_candle[0] / 1000)

            if last_candle_time is None or candle_time > last_candle_time:
                data = fetch_cryptoquant_data()

                if data:
                    action, signal_strength = calculate_signal(data)

                    if usdt_balance and action != 'hold':
                        position_size = calculate_position_size(usdt_balance)

                        if position_size:
                            if action == 'buy':
                                create_futures_market_order(SYMBOL, 'BUY', position_size)
                            elif action == 'sell':
                                create_futures_market_order(SYMBOL, 'SELL', position_size)

                last_candle_time = candle_time

        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
