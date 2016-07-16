import time
import schedule
import urllib.request
from bs4 import BeautifulSoup
import subprocess

EMAIL='davidgrant@gmail.com'

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
                    return False
    return True

def check(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
    if is_available(html):
        print(url, 'is available')
        mail_command = 'echo "%s" |mail -s "Disk Space Full" %s'
        msg = url + ' is available'
        p = subprocess.Popen(['mail -s "LEGO in-stock notice" %s' % (EMAIL,)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate(input=msg)[0]
        print('out=', out)
    else:
        print(url, 'is NOT available')


def job():

    URLS = (
#        'http://shop.lego.com/en-CA/Porsche-911-GT3-RS-42056',
        'http://shop.lego.com/en-CA/Hydroplane-Racer-42045',
#        'http://shop.lego.com/en-CA/Volkswagen-Beetle-10252',
        )
    for url in URLS:
        check(url)

def main():
    job()
    schedule.every(1).minute.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
