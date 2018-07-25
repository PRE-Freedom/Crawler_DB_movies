import configparser
from urllib import request
from urllib.parse import quote
import json


# config = configparser.ConfigParser()
# config.read(filenames='../config.ini', encoding='utf8')
# # set browser
# browserPath = str(config['system']['browserPath'])
# dirver = webdriver.PhantomJS(executable_path=browserPath)
# # assign parser
# parser = "html5lib"


def first_crawler(url: str):
    print(url)
    # 访问目标网页地址
    response = request.urlopen(url)
    context = response.read().decode('utf-8')
    json_obj = json.loads(context)
    pass


if __name__ == '__main__':
    first_crawler(
        'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8A%A8%E4%BD%9C&sort=recommend&page_limit=20&page_start=240')
    # movies_type = str(config['douban']['type'])
    # for t in movies_type.split('&'):
    #     type_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' + quote(
    #         t) + '&sort=recommend&page_limit=20&page_start=0'
    #     first_crawler(url=type_url)
