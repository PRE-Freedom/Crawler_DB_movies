from urllib import request
from first_crawler import Database
import os
from bs4 import BeautifulSoup


def second_crawler_for_cover(movie_type: str, title: str, cover_path: str, storge_path):
    """
    download the cover of the movie

    :param movie_type:
    :param title: name of movie
    :param cover_path: picture of movie
    :param storge_path:
    :return: None
    """
    types = movie_type.split('&')
    # could be improved
    # deal the multiple type but should new single folder
    for m_type in types:
        folder_name = storge_path + m_type + "/"
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        cover_name = folder_name + title + ".jpg"
        if not os.path.exists(cover_name):
            request.urlretrieve(cover_path, cover_name)


def second_crawler_for_abstract(movie_url: str):
    """
    obtain the abstract of movie
    :param movie_url:
    :return:
    """
    with request.urlopen(movie_url) as resp:
        bs4_obj = BeautifulSoup(resp.read().decode('utf-8'), 'html5lib')
    span = bs4_obj.find(name='span', property='v:summary')
    try:
        context = str(span.get_text()).replace('\n', '').replace(' ', '').replace("'", "`")
    except AttributeError:
        context = 'this movies has no abstract'
    return context


if __name__ == '__main__':
    db_obj = Database()
    db, cursor = db_obj.db_manager()
    sql = "select id,movie_type,title,movie_url,cover_path from movies where flag=0"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        movie_id, movie_type, title, movie_url, cover_path = result[0], result[1], result[2], result[3], result[4]

        print(movie_type + ' : ' + title)

        # store the picture
        second_crawler_for_cover(movie_type, title, cover_path, '../movies_cover/')
        # gain the abstract
        abstract = second_crawler_for_abstract(movie_url)
        # store the abstract into database
        if abstract is not None and len(abstract) != 0:
            sql = "update movies set flag=1,abstract='" + abstract + "' where id=" + str(movie_id)
            cursor.execute(sql)
            db.commit()
    cursor.close()
    db.close()
