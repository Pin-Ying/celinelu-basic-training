from unittest.mock import MagicMock
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from tasks.ptt_crawl import PttCrawler


def test_parse_article_from_local_html():
    with open("test_ptt_post.html", encoding="utf-8") as f:
        html_content = f.read()

    crawler = PttCrawler(db=None, board="test", board_id=1)

    # MagicMock，假扮get_soup，直接回傳預設的 html 假資料
    crawler.get_soup = MagicMock(return_value=BeautifulSoup(html_content, "html.parser"))

    # 模擬 a_tag
    a_tag = MagicMock()
    a_tag.get = MagicMock(return_value="/bbs/test/1234.html")

    post = crawler.parse_article(a_tag)

    assert post is not None
    assert hasattr(post, "author")
    assert hasattr(post, "title")
    assert hasattr(post, "content")
    assert hasattr(post, "comments")


def test_crawl(monkeypatch):
    crawler = PttCrawler(None, 'Lifeismoney', 5, datetime.now() - timedelta(days=10))
    with open("test_ptt_page1.html", encoding="utf-8") as f:
        page_html_1 = f.read()

    with open("test_ptt_page2.html", encoding="utf-8") as f:
        page_html_2 = f.read()

    with open("test_ptt_post.html", encoding="utf-8") as f:
        article_html = f.read()

    # 假扮get_soup，根據抓到的 URL ，回傳不同的 html 假資料
    def mock_get_soup(url):
        if url.endswith("index.html"):
            return BeautifulSoup(page_html_1, "html.parser")
        elif url.endswith("index4002.html"):
            return BeautifulSoup(page_html_2, "html.parser")
        elif url.endswith("M.1747883553.A.825.html") or url.endswith("M.1747722995.A.90E.html"):
            return BeautifulSoup(article_html, "html.parser")
        return None

    crawler.get_soup = mock_get_soup

    posts = crawler.crawl()

    assert len(posts) == 2
    for post in posts:
        assert post.author == "Tester"
        assert post.title == "Test Title"
        assert post.created_at == datetime.strptime("Fri May 23 12:00:00 2025", "%a %b %d %H:%M:%S %Y")
