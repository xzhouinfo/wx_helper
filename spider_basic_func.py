import requests
from bs4 import BeautifulSoup
from lxml import etree
from random_useragent.random_useragent import Randomize


def rand_header():
    r_agent = Randomize()
    ua = r_agent.random_agent('desktop', 'windows')
    ua = {'User-Agent': ua}
    # print(ua)
    return ua


def get_page(url):
    headers = rand_header()
    print(url)
    rsp = requests.get(url, headers)
    # print(rsp.cookies)
    rsp.encoding = rsp.apparent_encoding
    print(rsp.status_code)
    # if rsp.status_code == 404:
    #     rsp.text = None
    return rsp.text


def soup(page_text):
    sp = BeautifulSoup(page_text, 'lxml')
    return sp


def etree_obj(page_text):
    html = etree.HTML(page_text)
    return html


def test_pan_link(pan_link):
    # url = pan_link.rsplit('/')
    # pan_link = url[0] + '//' + url[2] + '/share/init?surl=' + url[-1][1:]
    # print(pan_link)
    page_text = get_page(pan_link)
    sop = soup(page_text)
    # print(sop)
    key_word = sop.find('div', id='share_nofound_des')
    if key_word:
        result = False
    else:
        result = True

    return result


if __name__ == '__main__':
    # url = 'https://pan.baidu.com/s/1wC6Iv4M_wy8WsCAu_gVHWg '
    # url2 = url.rsplit('/')
    # url3 = url2[0] + '//' + url2[2] + '/share/init?surl=' + url2[-1][1:]
    # print(url3)
    url = 'https://pan.baidu.com/s/1wC6Iv4M_wy8WsCAu_gVHWg'
    print(test_pan_link(url))
