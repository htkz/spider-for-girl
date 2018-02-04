import requests
from bs4 import BeautifulSoup

url_base = 'http://www.mmjpg.com/home/3'
seed_pool = []
image_url_pool = []

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'


def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def download_image(name, url, ref, cur_num):
    headers = {
        'User-Agent': user_agent,
        'Referer': ref
    }
    print('正在下载：{name}, {cur_num}/{total}'.format(cur_num=cur_num, total=len(image_url_pool), name=name))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open('imgs/page2/' + name + '.jpg', 'wb') as f:
            f.write(response.content)


def init():
    soup = get_soup(url_base)
    pics = soup.select('div.pic li > a')
    cur_num = 0

    # 初始化种子，也就是第一个页面里面所有的图片对应的链接列表
    for pic in pics:
        src = pic.get('href')
        seed_pool.append(src)

    # 添加每个种子对应的几十张图片的url到最终池子里面
    for seed in seed_pool:
        soup = get_soup(seed)
        page_num = int(soup.select('#page i')[0].next_sibling.text)
        for i in range(page_num):
            single_image_url = seed + '/' + str(i + 1)
            image_url_pool.append(single_image_url)

    # 从最终池子开始爬
    for url in image_url_pool:
        soup = get_soup(url)
        image = soup.select('#content img')[0]
        name = image.get('alt')
        src = image.get('src')
        refer = url
        cur_num += 1
        download_image(name, src, refer, cur_num)



def test():
    download_image('1234', 'http://img.mmjpg.com/2018/1220/4.jpg', 'http://www.mmjpg.com/mm/1220/4')


init()