import configparser
from urllib import request
from urllib.parse import quote
import json
import pymysql

config = configparser.ConfigParser()
config.read(filenames='../config.ini', encoding='utf8')


def db_manager():
    host = config['mysql']['host']
    user = config['mysql']['user']
    passwd = config['mysql']['passwd']
    database = config['mysql']['database']
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=database, charset='utf8')
    return db


def first_crawler(url: str):
    print(url)
    index = 0
    db = db_manager()
    cursor = db.cursor()
    while True:
        url += str(index)
        response = request.urlopen(url)
        context = response.read().decode('utf-8')
        json_obj = json.loads(context)
        subjects = json_obj['subjects']
        if len(subjects):
            for subject in subjects:
                title = subject['title']
                rate = subject['rate']
                movie_url = subject['url']
                cover_path = subject['cover']
                sql = "insert into movies(title,rate,movie_url,cover_path) values ('" + title + "','" + rate + "','" + movie_url + "','" + cover_path + "')"
                cursor.execute(sql)
                db.commit()
                index += 20
        else:
            break


if __name__ == '__main__':
    first_crawler(
        'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8A%A8%E4%BD%9C&sort=recommend&page_limit=20&page_start=')
    # movies_type = str(config['douban']['type'])
    # for t in movies_type.split('&'):
    #     type_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' + quote(
    #         t) + '&sort=recommend&page_limit=20&page_start=0'
    #     first_crawler(url=type_url)
