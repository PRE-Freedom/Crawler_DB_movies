import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

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
    time.sleep(100)
    a_more = dirver.find_elements(By.CLASS_NAME, 'more')[0]
    flag = True
    while flag:
        if a_more.text == '加载更多':
            a_more.click()
        else:
            flag = False
    # 解析目标网页的 Html 源码
    bs_obj = BeautifulSoup(dirver.page_source, parser)
    a_more = bs_obj.find(name='a', class_='more', href='javascript:;')


if __name__ == '__main__':
    movies_type = str(config['douban']['type'])
    for t in movies_type.split('&'):
        type_url = 'https://movie.douban.com/explore#!type=movie&tag=' + t + '&sort=recommend&page_limit=20&page_start=0'
        first_crawler(url=type_url)
