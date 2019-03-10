import spider_basic_func
import re
from urllib.parse import unquote_to_bytes
import random
import string


def rand_file_name():
    file_name = random.sample(string.digits + string.ascii_letters, 5)
    return str(file_name)


def transcoding(text):
    _list = unquote_to_bytes(text).split(b'\n')
    result = []
    for line in _list:
        try:
            result.append(line.decode('utf-8'))

        except UnicodeDecodeError:
            result.append(line.decode('gbk'))
    result = ''.join(result)
    return result


def get_us_tv(key):
    pan_text = ''
    mag_list = []
    ed2k_list = []

    link_pattern = re.compile('http://www.panyouwang.com/dianyingwangpan.*?html')
    pan_link_pattern = re.compile('https?\:\/\/pan.baidu.com\/s\/[a-zA-Z0-9\_\-]{6,23}')
    pw_pattern = re.compile('[密\s码密码提取码][:：].*?[0-9a-zA-Z]{4}')
    ed2k_pattern = re.compile('(ed2k[^"]+)')
    tv_list = []
    url = 'http://www.qwspcz.com/?s={}'.format(key)
    r = spider_basic_func.get_page(url)
    soup = spider_basic_func.soup(r)
    name = soup.h1.text

    if soup.find(class_='f404'):
        print('yes')
        return []
        print('测试11111111')
    else:
        if '的搜索结果' not in name:
            print('in page_url')
            pan_data = soup.find('blockquote')
            pan_link = re.findall(pan_link_pattern,str(pan_data))
            pan_pw = re.findall(pw_pattern, str(pan_data))
            if len(pan_link) == 0:
                pan_text = '没有网盘资源'
            else:
                if len(pan_link) == 1:
                    pan_passwd =['提取码：' + pan_pw[0][-4:]]
                    pan_text = '\n'.join(pan_link + pan_passwd)
                    print('111111', pan_text)
                # print(pan_link, pan_pw)
                else:
                    print('have two pan_link')
                    pp = list(zip(pan_link, pan_pw))
                    pan_num = len(pan_link)
                    print('page_url_two_pan_link_pp:', pp)
                    if pan_num:
                        pan_list = []
                        for p in pp:
                            p = [i.replace('码', '提取码') for i in p ]
                            pan_text = '\n'.join(p)
                            pan_list.append(pan_text)
                    print(pan_list)
            mag_etree = spider_basic_func.etree_obj(r)
            ed2k_datas = [[transcoding(i.split('|')[2]), i] for i in mag_etree.xpath('//a/@href') if 'ed2k' in i]
            ed2k_list = []
            for data in ed2k_datas:
                ed2k_text = '\n\n'.join(data)
                ed2k_list.append(ed2k_text)
            mag_datas = [[i.text, i['href']] for i in soup.find_all('a') if 'magnet' in i['href']]
            mag_list = []
            for data in mag_datas:
                mag_str = '\n\n'.join(data)
                mag_list.append(mag_str)
            # file_name = '{}.txt'.format(rand_file_name())
            with open('download_link.txt', 'w', encoding= 'utf-8') as f:
                f.write('\n'.join(mag_list + ed2k_list))
            print(len(mag_list))
            print(len(ed2k_list))

        else:
            print('in page_list_url')
            dd = [i.a['href'] for i in soup.find_all('h2') if key in re.split(r'[\s:：]', i.a.text)]
            print(dd)
            for i in soup.find_all('h2'):
                print(i.a.text.split(' '))
            print('测试222222')
            print(dd)
            if not dd:
                return []
            for i in dd:
                print('in dd')
                r = spider_basic_func.get_page(i)
                soup = spider_basic_func.soup(r)
                name = soup.h1.text
                pan_data = soup.find('blockquote')
                pan_link = re.findall(pan_link_pattern, str(pan_data))
                pan_pw = re.findall(pw_pattern, str(pan_data))
                if len(pan_link) == 0:
                    pan_text = '没有网盘资源'
                else:
                    if len(pan_link) == 1:
                        pan_passwd = ['提取码：' + pan_pw[0][-4:]]
                        print(type(pan_link))
                        pan_text = '\n'.join(pan_link + pan_passwd)
                        print('111111', pan_text)
                    else:
                        pp = list(zip(pan_link, pan_pw))
                        print('in pp :', pp)
                        pan_num = len(pan_link)
                        if pan_num:
                            pan_list = []
                            for p in pp:
                                p = [i.replace('码', '提取码') for i in p]
                                pan_text = '\n'.join(p)
                                pan_list.append(pan_text)

                mag_etree = spider_basic_func.etree_obj(r)
                ed2k_datas = [[transcoding(i.split('|')[2]), i] for i in mag_etree.xpath('//a/@href') if 'ed2k' in i]
                ed2k_list = []
                for data in ed2k_datas:
                    ed2k_text = '\n\n'.join(data)
                    ed2k_list.append(ed2k_text)
                mag_datas = [[i.text, i['href']] for i in soup.find_all('a') if 'magnet' in i['href']]
                mag_list = []
                for data in mag_datas:
                    mag_str = '\n\n'.join(data)
                    mag_list.append(mag_str)
                    # file_name = '{}.txt'.format(rand_file_name())
                with open('download_link.txt', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(mag_list + ed2k_list))
                print(len(mag_list))
                print(len(ed2k_list))

    return '\n'.join(pan_list), '\n\n\n{}\n'.format('*'*60).join(mag_list), '\n\n\n{}\n'.format('*'*60).join(ed2k_list)


if __name__=='__main__':
    print(get_us_tv('虚假新闻'))
