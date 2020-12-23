import os
import sys
import ccxt
from pathlib import Path
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Example
# BINANCE:BTCUSDTPERP
output_path = './generated/'
exchange_types = ['spot','future']


def write_watchlist(exchange, ex_type):
    print("fetching for ", exchange)
    tickers = get_active_tickers(exchange, ex_type)    
    if tickers:
        file_name = f"{exchange}_{ex_type}.txt"
        out_file_with_ex = Path(output_path,'exchange_embedded_symbols', file_name)
        out_file_without_ex = Path(output_path, 'generic_symbols', file_name)
        with open(out_file_with_ex, 'w') as f:
            for symbol in tickers:
                if (exchange == 'binance') and (ex_type == 'future'):
                        f.write(f"{exchange.upper()}:{symbol}PERP\n")
                else:
                    f.write(f"{exchange.upper()}:{symbol}\n")
        with open(out_file_without_ex, 'w') as f:
            for symbol in tickers:
                f.write(f"{symbol}\n")
    else:
        print(f"Sorry, couldn't connect to: {exchange}_{ex_type}")

def get_active_tickers(name,ex_type):
    exchange = getattr(ccxt, name)
    active_symbols = []
    # print(f"trying for {name}")
    try:
        markets = exchange({
            'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
            'options': {
                'defaultType': ex_type,
            }
        }).load_markets()
        for key in markets:
            if markets[key]['active'] == True:
                record = "" # needed? idk..
                clean_ticker = key.replace(r'/','')
                active_symbols.append(clean_ticker)
        return (active_symbols)
    except:
        print("Oops! ", exchange, " no workie!")
        return(False)

for exchange_type in exchange_types:
    for exchange in ccxt.exchanges:
        write_watchlist(exchange,exchange_type)
