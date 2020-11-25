#!/usr/bin/env python3

import time
import requests
#import schedule
import urllib.request
from bs4 import BeautifulSoup
import subprocess

import lego_stock_checker_conf

EMAIL=lego_stock_checker_conf.EMAIL

NOT_AVAILABLE=(
    'Temporarily out of stock',
)

def is_available(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    product_avail = soup.find("p", {"data-test": "product-overview-availability"})
    if not product_avail:
        raise Exception('Could not find product-overview-availability.')
    avail = product_avail.find('span').text
    return avail not in NOT_AVAILABLE

def check(url: str):
    html = requests.get(url).text
    if is_available(html):
        print(url, 'is available')
        msg = url + ' is available'
        p = subprocess.Popen(['mail', '-s', 'LEGO in-stock notice', EMAIL,],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate(input=msg.encode('utf-8'))[0]
        print('sending email')
    else:
        print(url, 'is NOT available')


def job():

    URLS = lego_stock_checker_conf.URLS
    for url in URLS:
        check(url)

def main():
    job()
#    schedule.every(1).minute.do(job)
#    while True:
#        schedule.run_pending()
#        time.sleep(1)

if __name__ == '__main__':
    main()
