import time
#import schedule
import urllib.request
from bs4 import BeautifulSoup
import subprocess

import lego_stock_checker_conf

EMAIL=lego_stock_checker_conf.EMAIL

NOT_AVAILABLE=(
    'availability-questionable',
    'availability-future',
)

def is_available(html):
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find(id='product-info').find_all('li')
    for li in lis:
        if li.get('class'):
            for class_name in li['class']:
                if class_name in NOT_AVAILABLE:
                    #                    print('class_name=', class_name)
                    return False
    return True

def check(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
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
