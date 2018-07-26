import configparser
import json
from urllib import request
from urllib.parse import quote

import pymysql
from pymysql.err import IntegrityError

config = configparser.ConfigParser()
config.read(filenames='../config.ini', encoding='utf8')


class Database:
    def __init__(self):
        self.host = config['mysql']['host']
        self.user = config['mysql']['user']
        self.passwd = config['mysql']['passwd']
        self.database = config['mysql']['database']

    def db_manager(self):
        """
        manager the database
        :return: db object
        """
        db = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.database, charset='utf8')
        cursor = db.cursor()
        return db, cursor

    @staticmethod
    def close_db(db, cursor):
        cursor.close()
        db.close()


def first_crawler(url: str, movie_type: str):
    """
    crawl the fundamental info of movies
    :param url: incomplete url, must add the index
    :param movie_type:
    :return:
    """
    index = 0
    # get the ability to operate the database
    db_obj = Database()
    db, cursor = db_obj.db_manager()
    while True:
        real_url = url + str(index)

        print(real_url)

        # request the url with internet and get response

        with request.urlopen(real_url) as response:
            context = response.read().decode('utf-8')
            # parser the response to json(dict)
            json_obj = json.loads(context)
        subjects = json_obj['subjects']
        if len(subjects):
            for subject in subjects:
                title = subject['title']
                rate = subject['rate']
                movie_url = subject['url']
                cover_path = subject['cover']
                movie_id = subject['id']
                # record the movie's info into database
                sql = "insert into movies(movie_id,movie_type,title,rate,movie_url,cover_path) values ('" + \
                      movie_id + "','" + movie_type + "','" + title + "','" + rate + "','" + movie_url + "','" + \
                      cover_path + "')"
                try:
                    cursor.execute(sql)
                    db.commit()
                except IntegrityError:
                    # deal the repetitive movie
                    sql = "select movie_type from movies where movie_id='" + movie_id + "'"
                    cursor.execute(sql)
                    movie_type_old = cursor.fetchone()[0]
                    if movie_type not in movie_type_old:
                        update_mv_type = movie_type_old + '&' + movie_type
                        sql = "update movies set movie_type='" + update_mv_type + "' where movie_id='" + movie_id + "'"
                        cursor.execute(sql)
                        db.commit()
                    else:
                        pass
            index += 20
        else:
            break
    Database.close_db(db, cursor)


if __name__ == '__main__':
    movies_type = str(config['douban']['type'])
    for t in movies_type.split('&'):
        print(t)
        type_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' + quote(
            t) + '&sort=recommend&page_limit=20&page_start='
        first_crawler(url=type_url, movie_type=t)
