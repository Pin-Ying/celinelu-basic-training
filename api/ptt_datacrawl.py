"""
要求

挑五個PTT版面，爬取過去一年資料，並定期取得新資料，注意爬文程式物件導向與抽象化
五個版面爬蟲需每小時定時執行一次（celery beat）
爬蟲需要可以穩定執行三天以上 (需有 log 佐證) (log 請存放在資料庫) (Hint：需要在資料庫當中建立資料表儲存)
"""

import requests
from bs4 import BeautifulSoup
from db.base import Database

# db = Database(
#     host='localhost',
#     user='test',
#     password='123456',
#     database='ptt'
# )


def get_soup(from_url):
    r = requests.get(from_url)
    if r.status_code == 200:
        return BeautifulSoup(r.text, "html.parser")
    return None


def get_one_article(a_tag):
    article_soup = get_soup("https://www.ptt.cc" + a_tag.get("href"))
    all_divs_tags = article_soup.select("div.article-metaline > span.article-meta-tag")
    all_divs_values = article_soup.select("div.article-metaline > span.article-meta-value")
    if len(all_divs_values) == 0:
        return None

    # 作者、標題、時間
    for div_tag, value in zip(all_divs_tags, all_divs_values):
        print(div_tag.text + ': ' + value.text)

    # 內文
    print(article_soup.text.split(all_divs_values[-1].text)[-1].split("※ 發信站:")[0])

    # 留言
    comments = article_soup.select("div.push")
    if len(comments) != 0:
        for comment in comments:
            print(comment.text)

        return None

    return None


# 目標看版 ['Stock','Baseball','NBA','HatePolitics','Lifeismoney']

all_boards = ['Stock', 'Baseball', 'NBA', 'HatePolitics', 'Lifeismoney']

# 某 <board> url(最新) https://www.ptt.cc/bbs/<board>/index.html

url = "https://www.ptt.cc/bbs/{board}/{page}"
for board in all_boards:
    soup = get_soup(url.format(board=board, page="index.html"))
    all_a_tags = soup.select("div.r-ent > .title > a")
    for tag in all_a_tags:
        get_one_article(tag)
