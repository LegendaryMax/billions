import csv
import os

from bs4 import BeautifulSoup
import requests


headers_m = {
    'cookie': 'pv_date=Sun Sep 18 2022 11:31:51 GMT+0300 (Moscow Standard Time); _gid=GA1.2.1124243769.1663489912; usprivacy=1---; qcSxc=1663489911812; __qca=P0-1756902514-1663489911805; _admrla=2.2-a0b07e82f8d8902a-6127a615-372c-11ed-84f5-db6b19132dba; screenerUrl=screener.ashx?v=110&f=ind_silver&t=WPM; pv_count=12; _ga_ZT9VQEWD4N=GS1.1.1663489911.1.1.1663491213.0.0.0; _ga=GA1.2.2124241916.1663489912; _awl=2.1663491222.0.5-c04f0abdc5ab4c4efc9987168baa00d6-6763652d6575726f70652d7765737431-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

def get_html(url):
    response = requests.get(url, headers=headers_m)

    if response.ok:
        return response.text
    print(response.status_code)


def write_csv(data, filename, order):
    with open(filename, 'a', newline="\n", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def read_csv(filename, order):
    with open(filename, encoding="utf-8", errors='ignore') as file:
        reader = csv.DictReader(file, fieldnames=order)
        return list(reader)


def get_tickers_list():
    arr = read_csv('tickers.csv', ['ticker'])
    return list(set([i['ticker'].split()[0] for i in arr]))


def get_ticker_data(t):
    soup = BeautifulSoup(get_html(f'https://finviz.com/quote.ashx?t={t}'), 'lxml')
    rows = soup.find_all('tr', {'class': 'table-dark-row'})
    name = soup.find('div', {'class': 'content', 'data-testid': 'quote-data-content'}).find('table').find('b').text
    data = {
        'name': name
    }
    for row in rows:
        tds_cp = row.find_all('td', {'class': 'snapshot-td2-cp'})
        tds = row.find_all('td', {'class': 'snapshot-td2'})
        for idx, i in enumerate(tds_cp):
            data[i.text] = tds[idx].text
    return data

if __name__ == '__main__':


    tickers = get_tickers_list()
    for t in tickers:
        try:
            data = get_ticker_data(t)
            data['ticker'] = t
            if os.stat("data.csv").st_size == 0:
                print(data.keys())
                write_csv({i: i for i in data.keys()}, 'data.csv', data.keys())
            write_csv(data, 'data.csv', data.keys())
        except:
            write_csv({'ticker': t}, 'no_data.csv', ['ticker'])
            print('error ', t)
            continue



