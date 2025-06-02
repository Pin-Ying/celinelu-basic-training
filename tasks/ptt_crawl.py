from typing import List

import bs4
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import logging
from schema.ptt_content import PostCrawl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ptt_crawler")


class PttCrawler:
    BASE_URL = "https://www.ptt.cc"

    def __init__(self, db, board: str, board_id: int, cutoff_date=datetime.now() - timedelta(days=365)):
        self.db = db
        self.board = board
        self.board_id = board_id
        self.cutoff_date = cutoff_date
        self.session = requests.Session()
        self.session.cookies.set("over18", "1")

    def get_soup(self, url):
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            print(f"[Error] fetch {url}: {e}")
        return None

    def parse_article(self, post_a_tag: bs4.element.Tag) -> PostCrawl:
        post_data = {"board_id": self.board_id}
        url = self.BASE_URL + post_a_tag.get("href")
        soup = self.get_soup(url)
        if not soup:
            return None

        try:
            metas = soup.select("div.article-metaline > span.article-meta-tag")
            meta_vals = soup.select("div.article-metaline > span.article-meta-value")
            if len(meta_vals) == 0:
                return None

            meta_map = dict(作者="author", 標題="title", 時間="created_at")
            for tag, val in zip(metas, meta_vals):
                key = meta_map.get(tag.text.strip())
                if not key:
                    continue
                val_text = val.text.strip()
                if key == "author":
                    val_text = val_text.split()[0]
                elif key == "created_at":
                    val_text = " ".join(val_text.split())
                    val_text = datetime.strptime(val_text, "%a %b %d %H:%M:%S %Y")
                post_data[key] = val_text

            body_text = soup.text.split(meta_vals[-1].text)[-1]
            post_data["content"] = body_text.split("※ 發信站:")[0].strip()

            post_data["comments"] = []
            for comment in soup.select("div.push"):
                spans = comment.select("span")
                if len(spans) >= 4:
                    post_data["comments"].append({
                        "user": spans[1].text.strip(),
                        "content": spans[2].text.strip(': '),
                        "created_at": spans[3].text.strip()
                    })

            return PostCrawl(**post_data)

        except Exception as e:
            print(f"[ParseError] {url} -> {e}")
            return None

    def crawl(self) -> List[PostCrawl]:
        crawling_page = "index.html"
        all_posts = []

        while crawling_page != '':
            page_posts = []
            logger.info(f"{self.board}, Crawling，crawling_page: {crawling_page}...")
            soup = self.get_soup(f"{self.BASE_URL}/bbs/{self.board}/{crawling_page}")
            if not soup:
                break

            crawling_page = ''  # 迴圈終止預設條件

            post_a_tags = []
            for tag in soup.select("div.r-list-container > div"):
                if "r-list-sep" in tag.get("class", []):
                    break
                if "r-ent" in tag.get("class", []):
                    a_tag = tag.select_one(".title > a")
                    if a_tag:
                        post_a_tags.append(a_tag)

            if not post_a_tags:
                break

            try:
                post = [self.parse_article(a_tag) for a_tag in post_a_tags]
                if post:
                    all_posts.extend(post)
                    page_posts.extend(post)
            except Exception as e:
                logger.error(f"Error!: {e}")

            logger.info(f"Finish crawling_page: {crawling_page}")

            if len(page_posts) > 0:
                page_posts.sort(key=lambda p: p.created_at)
                if page_posts[0].created_at < self.cutoff_date:
                    page_posts = [p for p in page_posts if p.created_at >= self.cutoff_date]
                    all_posts.extend(page_posts)
                    break

            prev_link = soup.select_one("div.btn-group-paging a:contains('上頁')")
            if not prev_link:
                break
            crawling_page = prev_link["href"].split("/")[-1]

        return all_posts
