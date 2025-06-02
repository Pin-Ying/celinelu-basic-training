from unittest.mock import MagicMock
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from tasks.ptt_crawl import PttCrawler

# 模擬文章 HTML
ARTICLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Test Title</title>
</head>
<body>
    <div id="main-container">
        <div id="main-content" class="bbs-screen bbs-content">
            <div class="article-metaline"><span class="article-meta-tag">作者</span><span class="article-meta-value">Tester (Jo)</span></div>
            <div class="article-metaline"><span class="article-meta-tag">標題</span><span class="article-meta-value">Test Title</span></div>
            <div class="article-metaline"><span class="article-meta-tag">時間</span><span class="article-meta-value">Fri May 23 12:00:00 2025</span></div>
            測試內文
            <div class="push"><span class="hl push-tag">推 </span><span class="f3 hl push-userid">LastAttack</span><span class="f3 push-content">: 測試留言</span><span class="push-ipdatetime"> 05/20 14:38</span></div>
            <div class="push"><span class="hl push-tag">推 </span><span class="f3 hl push-userid">LastAttack</span><span class="f3 push-content">: 測試留言</span><span class="push-ipdatetime"> 05/20 15:00</span></div>
        </div>
    </div>
</body>
</html>
"""

# 模擬 index.html 頁面列表
INDEX_HTML_1 = """
<div class="r-list-container action-bar-margin bbs-screen">
    <div class="r-ent">
        <div class="nrec"><span class="hl f3">26</span></div>
        <div class="title">
            <a href="/bbs/Lifeismoney/M.1747883553.A.825.html">[情報] Test post 1</a>
        </div>
        <div class="meta">
            <div class="author">testuser1</div>
            <div class="article-menu">
                <div class="trigger">…</div>
                <div class="dropdown">
                    <div class="item"><a href="#">搜尋同標題文章</a></div>
                    <div class="item"><a href="#">搜尋看板內 testuser1 的文章</a></div>
                </div>
            </div>
            <div class="date"> 5/22</div>
            <div class="mark"></div>
        </div>
    </div>
</div>
<div class="btn-group btn-group-paging">
    <a class="btn wide" href="/bbs/Lifeismoney/index4002.html">&lsaquo; 上頁</a>
</div>
"""

INDEX_HTML_2 = """
<div class="r-list-container action-bar-margin bbs-screen">
    <div class="r-ent">
        <div class="nrec"><span class="hl f3">26</span></div>
        <div class="title">
            <a href="/bbs/Lifeismoney/M.1747722995.A.90E.html">[情報] Test post 2</a>
        </div>
        <div class="meta">
            <div class="author">testuser2</div>
            <div class="article-menu">
                <div class="trigger">…</div>
                <div class="dropdown">
                    <div class="item"><a href="#">搜尋同標題文章</a></div>
                    <div class="item"><a href="#">搜尋看板內 testuser2 的文章</a></div>
                </div>
            </div>
            <div class="date"> 5/22</div>
            <div class="mark"></div>
        </div>
    </div>
</div>
"""


def test_parse_article_from_inline_html():
    crawler = PttCrawler(db=None, board="test", board_id=1)
    crawler.get_soup = MagicMock(return_value=BeautifulSoup(ARTICLE_HTML, "html.parser"))

    a_tag = MagicMock()
    a_tag.get.return_value = "/bbs/test/1234.html"

    post = crawler.parse_article(a_tag)

    assert post is not None
    assert post.author == "Tester"
    assert post.title == "Test Title"
    assert isinstance(post.content, str)
    assert len(post.comments) == 2


def test_crawl_with_inline_html():
    crawler = PttCrawler(None, 'Lifeismoney', 5, datetime.now() - timedelta(days=10))

    def mock_get_soup(url):
        if url.endswith("index.html"):
            return BeautifulSoup(INDEX_HTML_1, "html.parser")
        elif url.endswith("index4002.html"):
            return BeautifulSoup(INDEX_HTML_2, "html.parser")
        elif url.endswith("M.1747883553.A.825.html") or url.endswith("M.1747722995.A.90E.html"):
            return BeautifulSoup(ARTICLE_HTML, "html.parser")
        return None

    crawler.get_soup = mock_get_soup

    posts = crawler.crawl()

    assert len(posts) == 2
    for post in posts:
        assert post.author == "Tester"
        assert post.title == "Test Title"
        assert post.created_at == datetime.strptime("Fri May 23 12:00:00 2025", "%a %b %d %H:%M:%S %Y")
