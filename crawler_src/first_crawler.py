import configparser
from selenium import webdriver
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read(filenames='../config.ini', encoding='utf8')
# set browser
browserPath = str(config['system']['browserPath'])
dirver = webdriver.PhantomJS(executable_path=browserPath)
# assign parser
parser = "html5lib"


def first_crawler(url: str):
    print(url)
    # 访问目标网页地址
    dirver.get(url)
    # 解析目标网页的 Html 源码
    bs_obj = BeautifulSoup(dirver.page_source, parser)
    divs = bs_obj.find(name='div', class_='list-wp')


if __name__ == '__main__':
    movies_type = str(config['douban']['type'])
    for t in movies_type.split('&'):
        type_url = 'https://movie.douban.com/explore#!type=movie&tag=' + t + '&sort=recommend&page_limit=20&page_start=0'
        first_crawler(url=type_url)
