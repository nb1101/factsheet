#!/usr/bin/env python

import os
import sys
import datetime
import requests
import termplotlib as tpl
from collections import OrderedDict
from millify import millify
from colorama import Fore, Back, Style


def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0


def fetch(**kwargs):
    url = 'https://www.alphavantage.co/query'
    kwargs['apikey'] = os.getenv('ALPHAVANTAGE_APIKEY')
    with requests.get(url, params=kwargs) as response:
        if response.status_code == 200:
            json_msg = response.json()
            if not json_msg:
                raise Exception('Unknown symbol')
            elif 'Note' in json_msg:
                raise Exception(f'{json_msg["Note"]}')
            else:
                return json_msg
        else:
            raise Exception(
                f'Failed to fetch {function} for {symbol}: {response.text()}')


def get_daily_timeseries(symbol):
    return fetch(
        symbol=symbol,
        function='TIME_SERIES_DAILY_ADJUSTED',
        outputsize='full')['Time Series (Daily)']


def get_business_day_data(ts_data, date):
    date_str = date.strftime('%Y-%m-%d')
    if date_str in ts_data:
        return {k.split(" ", 1)[-1]: convert_to_float(v) for k, v in ts_data[date_str].items()}

    return get_business_day_data(ts_data, date - datetime.timedelta(days=1))


def get_returns(ts_data):
    returns = {}
    today = datetime.datetime.today()

    # Last close
    data = get_business_day_data(ts_data, today)
    last_close = data['adjusted close']

    # 1 week return
    date_before_1w = today - datetime.timedelta(days=7)
    data = get_business_day_data(ts_data, date_before_1w)
    returns['1w'] = ((last_close - data['adjusted close']) / data['adjusted close']) * 100

    # 1 month return
    date_before_1m = today - datetime.timedelta(days=30)
    data = get_business_day_data(ts_data, date_before_1m)
    returns['1m'] = ((last_close - data['adjusted close']) / data['adjusted close']) * 100

    # 3 month return
    date_before_3m = today - datetime.timedelta(days=90)
    data = get_business_day_data(ts_data, date_before_3m)
    returns['3m'] = ((last_close - data['adjusted close']) / data['adjusted close']) * 100

    # 1 year return
    date_before_1y = today - datetime.timedelta(days=365)
    data = get_business_day_data(ts_data, date_before_1y)
    returns['1y'] = ((last_close - data['adjusted close']) / data['adjusted close']) * 100

    # 3 year return
    date_before_3y = today - datetime.timedelta(days=3*365)
    data = get_business_day_data(ts_data, date_before_3y)
    returns['3y'] = ((last_close - data['adjusted close']) / data['adjusted close']) * 100

    # 5 year return
    date_before_5y = today - datetime.timedelta(days=5*365)
    data = get_business_day_data(ts_data, date_before_5y)
    returns['5y'] = ((last_close - data['adjusted close']) / data['adjusted close']) * 100

    return returns


def get_highs(ts_data):
    highs = {
        '1w': 0.0,
        '1m': 0.0,
        '3m': 0.0,
        '1y': 0.0,
        '3y': 0.0,
        '5y': 0.0
    }

    today = datetime.datetime.today()
    latest_data = get_business_day_data(ts_data, today)

    # 1 week high
    highs['1w'] = latest_data['high']
    for date in (today - datetime.timedelta(n) for n in range(7)):
        date_str = date.strftime('%Y-%m-%d')
        day_high = convert_to_float(ts_data.get(date_str, {}).get('2. high', 0.0))
        if day_high > highs['1w']:
            highs['1w'] = day_high

    # 1 month high
    highs['1m'] = highs['1w']
    date_before_1w = today - datetime.timedelta(days=7)
    for date in (date_before_1w - datetime.timedelta(n) for n in range(30 - 7)):
        date_str = date.strftime('%Y-%m-%d')
        day_high = convert_to_float(ts_data.get(date_str, {}).get('2. high', 0.0))
        if day_high > highs['1m']:
            highs['1m'] = day_high

    # 3 month high
    highs['3m'] = highs['1m']
    date_before_1m = today - datetime.timedelta(days=30)
    for date in (date_before_1m - datetime.timedelta(n) for n in range(90 - 30)):
        date_str = date.strftime('%Y-%m-%d')
        day_high = convert_to_float(ts_data.get(date_str, {}).get('2. high', 0.0))
        if day_high > highs['3m']:
            highs['3m'] = day_high

    # 1 year high
    highs['1y'] = highs['3m']
    date_before_3m = today - datetime.timedelta(days=90)
    for date in (date_before_1m - datetime.timedelta(n) for n in range(365 - 90)):
        date_str = date.strftime('%Y-%m-%d')
        day_high = convert_to_float(ts_data.get(date_str, {}).get('2. high', 0.0))
        if day_high > highs['1y']:
            highs['1y'] = day_high

    # 3 year high
    highs['3y'] = highs['1y']
    date_before_1y = today - datetime.timedelta(days=365)
    for date in (date_before_1y - datetime.timedelta(n) for n in range(3 * 365 - 365)):
        date_str = date.strftime('%Y-%m-%d')
        day_high = convert_to_float(ts_data.get(date_str, {}).get('2. high', 0.0))
        if day_high > highs['3y']:
            highs['3y'] = day_high

    # 5 year high
    highs['5y'] = highs['3y']
    date_before_3y = today - datetime.timedelta(days=3*365)
    for date in (date_before_3y - datetime.timedelta(n) for n in range(5 * 365 - 3 * 365)):
        date_str = date.strftime('%Y-%m-%d')
        day_high = convert_to_float(ts_data.get(date_str, {}).get('2. high', 0.0))
        if day_high > highs['5y']:
            highs['5y'] = day_high

    return highs

def get_lows(ts_data):
    today = datetime.datetime.today()
    latest_data = get_business_day_data(ts_data, today)

    lows = {
        '1w': latest_data['low'],
        '1m': latest_data['low'],
        '3m': latest_data['low'],
        '1y': latest_data['low'],
        '3y': latest_data['low'],
        '5y': latest_data['low']
    }

    # 1 week low
    lows['1w'] = latest_data['low']
    for date in (today - datetime.timedelta(n) for n in range(7)):
        date_str = date.strftime('%Y-%m-%d')
        day_low = convert_to_float(ts_data.get(date_str, {}).get('3. low', latest_data['low']))
        if day_low < lows['1w']:
            lows['1w'] = day_low

    # 1 month low
    lows['1m'] = lows['1w']
    date_before_1w = today - datetime.timedelta(days=7)
    for date in (date_before_1w - datetime.timedelta(n) for n in range(30 - 7)):
        date_str = date.strftime('%Y-%m-%d')
        day_low = convert_to_float(ts_data.get(date_str, {}).get('3. low', latest_data['low']))
        if day_low < lows['1m']:
            lows['1m'] = day_low

    # 3 month low
    lows['3m'] = lows['1m']
    date_before_1m = today - datetime.timedelta(days=30)
    for date in (date_before_1m - datetime.timedelta(n) for n in range(90 - 30)):
        date_str = date.strftime('%Y-%m-%d')
        day_low = convert_to_float(ts_data.get(date_str, {}).get('3. low', latest_data['low']))
        if day_low < lows['3m']:
            lows['3m'] = day_low

    # 1 year low
    lows['1y'] = lows['3m']
    date_before_3m = today - datetime.timedelta(days=90)
    for date in (date_before_1m - datetime.timedelta(n) for n in range(365 - 90)):
        date_str = date.strftime('%Y-%m-%d')
        day_low = convert_to_float(ts_data.get(date_str, {}).get('3. low', latest_data['low']))
        if day_low < lows['1y']:
            lows['1y'] = day_low

    # 3 year low
    lows['3y'] = lows['1y']
    date_before_1y = today - datetime.timedelta(days=365)
    for date in (date_before_1y - datetime.timedelta(n) for n in range(3 * 365 - 365)):
        date_str = date.strftime('%Y-%m-%d')
        day_low = convert_to_float(ts_data.get(date_str, {}).get('3. low', latest_data['low']))
        if day_low < lows['3y']:
            lows['3y'] = day_low

    # 5 year low
    lows['5y'] = lows['3y']
    date_before_3y = today - datetime.timedelta(days=3*365)
    for date in (date_before_3y - datetime.timedelta(n) for n in range(5 * 365 - 3 * 365)):
        date_str = date.strftime('%Y-%m-%d')
        day_low = convert_to_float(ts_data.get(date_str, {}).get("3. low", latest_data['low']))
        if day_low < lows['5y']:
            lows['5y'] = day_low

    return lows


def get_overview(symbol):
    return fetch(symbol=symbol, function='OVERVIEW')


def get_quote(symbol):
    return {k.split(" ", 1)[-1]: v for k, v in fetch(
        symbol=symbol, function='GLOBAL_QUOTE')['Global Quote'].items()}


def filter_data(ts_data, start=None, days=365):
    if start is None:
        start = datetime.datetime.today() - datetime.timedelta(days=days)

    data = OrderedDict()

    for date in (start + datetime.timedelta(n) for n in range(days)):
        date_str = date.strftime('%Y-%m-%d')
        if date_str in ts_data:
            data[date] = {
                k.split(" ", 1)[-1]: convert_to_float(
                    v) for k, v in ts_data[date_str].items()}

    return data


def print_usage():
    print('Usage:')
    print('factsheet <TICKER SYMBOL>')
    print('Example: factsheet TSLA')


def main():
    try:
        if len(sys.argv) < 2:
            print_usage()
            return

        symbol = sys.argv[1]
        overview = get_overview(symbol)
        quote = get_quote(symbol)

        # Title
        print(
            Style.NORMAL +
            f'{overview["Symbol"]} | {overview["Name"]} | {overview["Sector"]}')

        # Details
        print(Style.DIM + f'{overview["AssetType"]}' + Style.RESET_ALL, end='\n\n')

        # Price
        price = convert_to_float(quote["price"])
        print(Style.BRIGHT + f'{price:.2f}' + Style.RESET_ALL, end=' ')

        previous_close = convert_to_float(quote["previous close"])
        difference = price - previous_close
        difference_percentage = (difference / previous_close) * 100
        if price < previous_close:
            print(
                Fore.RED +
                f'{difference:.2f} ({difference_percentage:.2f}%)' +
                Fore.RESET)
        else:
            print(
                Fore.GREEN +
                f'+{difference:.2f} ({difference_percentage:.2f}%)' +
                Fore.RESET)

        # Price details
        print(
            Style.DIM +
            f'{quote["latest trading day"]} | {overview["Currency"]} | {overview["Exchange"]}' +
            Style.RESET_ALL,
            end='\n\n')

        # Summary
        days_range_text = "Day's Range"
        days_range = f'{convert_to_float(quote["low"]):.2f}-{convert_to_float(quote["high"]):.2f}'
        fifty_two_week_range = f'{convert_to_float(overview["52WeekLow"]):.2f}-{convert_to_float(overview["52WeekHigh"]):.2f}'
        print(f'{"Previous Close":<15} {previous_close:>15}', end=' | ')
        print(f'{"Market Cap":<15} {millify(overview["MarketCapitalization"], precision=2):>15}')
        print(f'{"Open":<15} {quote["open"]:>15}', end=' | ')
        beta = f'{convert_to_float(overview["Beta"]):.2f}'
        print(f'{"Beta":<15} {beta:>15}')
        print(f'{days_range_text:<15} {days_range:>15}', end=' | ')
        pe_ratio = f'{convert_to_float(overview["PERatio"]):.2f}'
        print(f'{"PE Ratio":<15} {pe_ratio:>15}')
        print(f'{"52 Week Range":<15} {fifty_two_week_range:>15}', end=' | ')
        eps = f'{convert_to_float(overview["EPS"]):.2f}'
        print(f'{"EPS":<15} {eps:>15}')
        print(f'{"Volume":<15} {millify(quote["volume"], precision=2):>15}', end= ' | ')
        dividend = f'{convert_to_float(overview["ForwardAnnualDividendRate"]):.2f}'
        print(f'{"Dividend":<15} {dividend:>15}')
        print()

        # Historic data
        ts_data = get_daily_timeseries(symbol)

        print(f'{"":<15} {"1 Week":>15} {"1 Month":>15} {"3 Months":>15} {"1 Year":>15} {"3 Years":>15} {"5 Years":>15}')

        # Returns
        returns = get_returns(ts_data)
        print(f'{"Performance":<15}', end=' ')

        if returns['1w'] < 0:
            print(Fore.RED, end='')
        else:
            print(Fore.GREEN, end='')
        return_1w = f'{returns["1w"]:.2f}%'
        print(f'{return_1w:>15}' + Fore.RESET, end=' ')

        if returns['1m'] < 0:
            print(Fore.RED, end='')
        else:
            print(Fore.GREEN, end='')
        return_1m = f'{returns["1m"]:.2f}%'
        print(f'{return_1m:>15}' + Fore.RESET, end=' ')

        if returns['3m'] < 0:
            print(Fore.RED, end='')
        else:
            print(Fore.GREEN, end='')
        return_3m = f'{returns["3m"]:.2f}%'
        print(f'{return_3m:>15}' + Fore.RESET, end=' ')

        if returns['1y'] < 0:
            print(Fore.RED, end='')
        else:
            print(Fore.GREEN, end='')
        return_1y = f'{returns["1y"]:.2f}%'
        print(f'{return_1y:>15}' + Fore.RESET, end=' ')

        if returns['3y'] < 0:
            print(Fore.RED, end='')
        else:
            print(Fore.GREEN, end='')
        return_3y = f'{returns["3y"]:.2f}%'
        print(f'{return_3y:>15}' + Fore.RESET, end=' ')

        if returns['5y'] < 0:
            print(Fore.RED, end='')
        else:
            print(Fore.GREEN, end='')
        return_5y = f'{returns["5y"]:.2f}%'
        print(f'{return_5y:>15}' + Fore.RESET)

        highs = get_highs(ts_data)
        highs = {k: f'{v:.2f}' for k, v in highs.items()}
        print(
            f'{"High":<15} {highs["1w"]:>15} {highs["1m"]:>15} '
            f'{highs["3m"]:>15} {highs["1y"]:>15} {highs["3y"]:>15} '
            f'{highs["5y"]:>15}')

        lows = get_lows(ts_data)
        lows = {k: f'{v:.2f}' for k, v in lows.items()}
        print(
            f'{"Low":<15} {lows["1w"]:>15} {lows["1m"]:>15} '
            f'{lows["3m"]:>15} {lows["1y"]:>15} {lows["3y"]:>15} '
            f'{lows["5y"]:>15}',
            end='\n\n')

        print("Chart: 1 Year", end='\n\n')

        data = filter_data(ts_data)

        x = []
        y = []
        for k, v in data.items():
            x.append(k.timestamp())
            y.append(v['adjusted close'])

        fig = tpl.figure()
        fig.plot(x, y, label=overview["Name"], width=150, height=50)
        fig.show()
    except Exception as ex:
        print(f'Failed to fetch data for {symbol}: {str(ex)}')
    finally:
        print(Fore.RESET + Style.RESET_ALL)

if __name__ == '__main__':
    main()
