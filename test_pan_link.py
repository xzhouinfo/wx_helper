import requests
from bs4 import BeautifulSoup
from random_useragent.random_useragent import Randomize

r_agent = Randomize()
ua = r_agent.random_agent('desktop', 'windows')
ub = {'User-Agent': ua}


def test_pan_link(link):
    r = requests.get(url=link, headers=ub)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    key_word = soup.find('dl', class_='pickpw clearfix')
    if key_word:
        result = True
    else:
        result = False

    return result


if __name__ == '__main__':
    link = 'https://pan.baidu.com/s/1MoNTM1WsTdAz1CgJHu4IpA'
    print(test_pan_link(link))