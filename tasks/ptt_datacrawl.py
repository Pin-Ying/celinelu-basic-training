"""
要求
挑五個PTT版面，爬取過去一年資料，並定期取得新資料，注意爬文程式物件導向與抽象化
五個版面爬蟲需每小時定時執行一次（celery beat）
爬蟲需要可以穩定執行三天以上 (需有 log 佐證) (log 請存放在資料庫) (Hint：需要在資料庫當中建立資料表儲存)
"""

import requests
from bs4 import BeautifulSoup
from sqlalchemy import false

from schema.ptt_content import PostInput
from datetime import datetime, timedelta
from db.database import engine, SessionLocal, Base
from db.crud import seed_boards, create_post_with_comments
from pydantic import ValidationError


def get_soup(from_url):
    r = requests.get(from_url)
    if r.status_code == 200:
        return BeautifulSoup(r.text, "html.parser")
    return None


def get_one_article(a_tag, board_id):
    raw_post = {"board_id": board_id}
    article_soup = get_soup("https://www.ptt.cc" + a_tag.get("href"))
    all_divs_tags = article_soup.select("div.article-metaline > span.article-meta-tag")
    all_divs_values = article_soup.select("div.article-metaline > span.article-meta-value")
    if len(all_divs_values) == 0:
        return None

    # 作者、標題、時間
    to_key = {"作者": "author", "標題": "title", "時間": "created_at"}
    for div_tag, value in zip(all_divs_tags, all_divs_values):
        tag_name = div_tag.text.strip()
        if tag_name not in to_key:
            continue

        tag_value = value.text.split()
        if tag_name == "作者":
            tag_value = tag_value[0]

        elif tag_name == "標題":
            tag_value = "".join(tag_value)

        elif tag_name == "時間":
            tag_value = " ".join(tag_value)
            tag_value = datetime.strptime(tag_value, "%a %b %d %H:%M:%S %Y")
        raw_post[to_key[tag_name]] = tag_value

    # 內文
    second_half_post = article_soup.text.split(all_divs_values[-1].text)[-1]
    raw_post["content"] = second_half_post.split("※ 發信站:")[0].strip()

    # 留言
    raw_post["comments"] = []
    comments = article_soup.select("div.push")
    if len(comments) != 0:
        for comment in comments:
            all_span_tags = comment.select("span")
            if len(all_span_tags) < 4:
                continue
            raw_post["comments"].append({
                "user": all_span_tags[1].text.strip(),
                "content": all_span_tags[2].text.strip(),
                "created_at": all_span_tags[3].text.strip()
            })

    try:
        validated_post = PostInput(**raw_post)
        create_post_with_comments(db, dict(validated_post))
        return validated_post
    except ValidationError as e:
        print(f"跳過無效資料：{raw_post}，錯誤：{e}")
        return None


def get_current_page(current_url):
    current_soup = get_soup(current_url)
    all_a_tags = current_soup.select("div.r-ent > .title > a")
    stop_crawling = False

    if not all_a_tags:
        return None

    for tag in all_a_tags:
        article = get_one_article(tag, board_id)
        if article:
            print(article)
            if article.created_at and article.created_at < cutoff_date:
                stop_crawling = True
                break  # 跳出 for tag loop
    if stop_crawling:
        return None

    # 嘗試抓上一頁連結
    prev_link = current_soup.select_one("div.btn-group-paging a:contains('上頁')")
    if prev_link and 'href' in prev_link.attrs:
        return prev_link['href'].split('/')[-1]  # 取得 page
    else:
        return None


Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_boards(db)

# 目標看版：['Stock','Baseball','NBA','HatePolitics','Lifeismoney']
all_boards = {'Stock': 1, 'Baseball': 2, 'NBA': 3, 'HatePolitics': 4, 'Lifeismoney': 5}
# 時間：一年
cutoff_date = datetime.now() - timedelta(days=365)
# url
url = "https://www.ptt.cc/bbs/{board}/{page}"

for board in all_boards.keys():
    # 某 <board> url(最新) https://www.ptt.cc/bbs/<board>/index.html
    board_id = all_boards[board]
    page = "index.html"
    try:
        first_page = url.format(board=board, page=page)
        next_page = get_current_page(first_page)
        while next_page:
            get_current_page(url.format(board=board, page=next_page))

    finally:
        db.close()