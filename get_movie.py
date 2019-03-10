import spider_basic_func
import re
import test_pan_link
import get_us_tv

def panyouwang(key):
    link_pattern = re.compile('http://www.panyouwang.com/dianyingwangpan.*?html')
    pan_link_pattern = re.compile('https?\:\/\/pan.baidu.com\/s\/[a-zA-Z0-9\_\-]{23}')
    pw_pattern = re.compile('[密\s码密码提取码][:：].*?[0-9a-zA-Z]{4}')
    ed2k_pattern = re.compile('(ed2k[^"]+)')
    movie_pages = []
    url = r'http://www.panyouwang.com/plus/search.php?kwtype=0&keyword={}'.format(key)
    page_text = spider_basic_func.get_page(url)
    soup = spider_basic_func.soup(page_text)
    all_h3 = soup.find_all('h3')
    all_link = re.findall(link_pattern, str(all_h3))
    print(all_link)
    if len(all_h3) == 1:
        result = False
    else:
        if all_link:
            for url in all_link:
                page_text = spider_basic_func.get_page(url)
                soup = spider_basic_func.soup(page_text)
                all_p = soup.find_all('p')
                pan_link = re.findall(pan_link_pattern, str(all_p))
                pan_pw = re.findall(pw_pattern, str(all_p))
                name = [soup.h1.text]
                print(name)
                if pan_link:
                    movie_pages.append('\n'.join(name + pan_link + pan_pw))
                    # print(movie_pages)
                else:
                    ed2k_link = re.findall(ed2k_pattern,str(all_p))
                    movie_pages.append('\n'.join(name + ed2k_link))
            result = '\n'.join(movie_pages)
            return result

def zhongzisou_mag(key):
    url = 'https://www.zhongziso.com/list/{}/1'.format(key)
    page_text = spider_basic_func.get_page(url)
    soup = spider_basic_func.soup(page_text)
    all_data = soup.find_all('td')
    nn = len(all_data)
    data = []
    for m in range(0, nn, 6):
        move_name = all_data[m].get_text()[4:]
        mag = all_data[m-2].a['href']
        heat = all_data[m-3].get_text()
        size = all_data[m-4].get_text()
        creation_date = all_data[m-5].get_text()
        # print(all_data[m].get_text())
        data.append([move_name, mag, heat, size, creation_date])
    return data


def get(key):
    get_us_tv_str = get_us_tv.get_us_tv(key)
    if get_us_tv_str:
        if 'pan.baidu.com' in get_us_tv_str[0] and get_us_tv_str[1] != '' or get_us_tv_str[2] != '':
            result_text = get_us_tv_str[0] + '\n' + '下面文件有ed2k或者magnet链接，\n可以百度离线下载或者用下载软件下载。'
        else:
            result_text = '暂时没网盘资源。\n下面文件有ed2k或者magnet链接，\n可以百度离线下载或者用下载软件下载。'
            text = '\n{}\n'.format('-'*30).join(list(get_us_tv_str))
            with open('download_link.txt', 'w', encoding='utf-8') as f:
                f.write(text)
    else:
        pengyouwang = panyouwang(key)
        print('这是pengyou----', pengyouwang)
        print(pengyouwang is None)
        if pengyouwang is not None:
            result_text = ''.join(pengyouwang)
        else:
            tt = []
            zhongzisou = zhongzisou_mag(key)
            if zhongzisou:
                for i in zhongzisou:
                    for y in i:
                        tt.append(y)
                    tt.append('\n\n')

                text = '\n'.join(tt)
                with open('download_link.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
                result_text = '你需要的下载链接在下面的文本文件里，\n可以百度离线下载或者用下载软件下载\n,如果好用，帮我推荐给你朋友吧，谢谢。'
            else:
                result_text = '主人技术太菜，没能匹配到更多的内容'
            print(result_text)
    return result_text

if __name__ == '__main__':
    result = zhongzisou_mag('草b')
    for i in result:
        print(i)



