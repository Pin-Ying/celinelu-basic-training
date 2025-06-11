import logging
from datetime import datetime, timedelta
from typing import List

import bs4
import requests
from bs4 import BeautifulSoup

from db.crud import get_existing_user_map, get_or_create_user, get_or_create_post, get_existing_comments_keys_list, \
    create_comments_bulk
from model.ptt_content import Post, Comment
from schema.ptt_content import PostCrawl, CommentCrawl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ptt_crawler")


class PttCrawler:
    BASE_URL = "https://www.ptt.cc"
    cutoff_date = datetime.now() - timedelta(days=365)

    def __init__(self, db, board: str, board_id: int, latest_post: Post = None):
        self.db = db
        self.board = board
        self.board_id = board_id
        self.latest_post = latest_post
        if latest_post:
            self.cutoff_date = latest_post.post_created_time
        self.session = requests.Session()
        self.session.cookies.set("over18", "1")
        self.user_map = get_existing_user_map(self.db)

    def get_soup(self, url):
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            print(f"[Error] fetch {url}: {e}")
        return None

    def is_latest_post(self, post: PostCrawl) -> bool:
        if self.latest_post:
            if post.title == self.latest_post.title and post.post_created_time == self.latest_post.post_created_time:
                return True
        return False

    def parse_article(self, post_a_tag: bs4.element.Tag) -> PostCrawl | None:
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

            meta_map = dict(作者="author", 標題="title", 時間="post_created_time")
            for tag, val in zip(metas, meta_vals):
                key = meta_map.get(tag.text.strip())
                if not key:
                    continue
                val_text = val.text.strip()
                if key == "author":
                    val_text = val_text.split()[0]
                elif key == "post_created_time":
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
                        "comment_created_time": spans[3].text.strip()
                    })

            return PostCrawl(**post_data)

        except Exception as e:
            print(f"[ParseError] {url} -> {e}")
            return None

    def crawl_all_articles(self) -> List[PostCrawl]:
        crawling_article_list = "index.html"
        all_posts = []
        found_cutoff_post = False

        # 爬取文章列表 => crawling_article_list 為正在爬取的文章列表
        while crawling_article_list and not found_cutoff_post:
            logger.info(f"{self.board}, Crawling，crawling_article_list: {crawling_article_list}...")
            article_list_soup = self.get_soup(f"{self.BASE_URL}/bbs/{self.board}/{crawling_article_list}")
            if not article_list_soup:
                break

            # 取得每篇文章的 a_tag
            article_a_tags = []
            for tag in article_list_soup.select("div.r-list-container > div"):
                # r-list-sep => 截掉首頁幾篇排在後面的熱門文章(無時序且會與其他頁重複)
                if "r-list-sep" in tag.get("class", []):
                    break
                if "r-ent" in tag.get("class", []):
                    a_tag = tag.select_one(".title > a")
                    if a_tag:
                        article_a_tags.append(a_tag)
            if not article_a_tags:
                break

            # 每篇文章的爬取 => parse_article()
            # reversed(article_a_tags) => 確保文章排序新到舊(原文章列表預設新文章在下)
            for a_tag in reversed(article_a_tags):
                try:
                    post = self.parse_article(a_tag)
                    if post:
                        # 爬到前次爬取的最新文章後結束爬取
                        if self.is_latest_post(post):
                            found_cutoff_post = True
                            break
                        # 若文章舊於 cutoff_date 則結束爬取
                        if post.post_created_time and post.post_created_time < self.cutoff_date:
                            found_cutoff_post = True
                            break
                        all_posts.append(post)
                except Exception as e:
                    logger.error(f"Error!: {e}")
                    continue
            logger.info(f"{self.board}, crawling_article_list: {crawling_article_list} Finish.")

            prev_link = article_list_soup.select_one("div.btn-group-paging a:contains('上頁')")
            if not prev_link:
                break
            crawling_article_list = prev_link["href"].split("/")[-1]
        return all_posts

    # --- save data to db ---
    def save_single_post(self, post_input: PostCrawl):
        try:
            # 取得作者
            author = self.user_map.get(post_input.author) if self.user_map else None
            if author is None:
                author = get_or_create_user(self.db, post_input.author)
                self.user_map[author.name] = author
            new_post = Post(
                title=post_input.title,
                content=post_input.content,
                post_created_time=post_input.post_created_time,
                board_id=post_input.board_id,
                author_id=author.id
            )
            post = get_or_create_post(self.db, new_post)
            return post

        except Exception as e:
            self.db.rollback()
            raise e

    def save_comments_bulk(self, comments_inputs: List[CommentCrawl], post_id: int):
        try:
            new_comments = []
            # 該文章已經存在的留言
            existing_comment_keys = get_existing_comments_keys_list(self.db, post_id)
            seen_comments = set(existing_comment_keys)

            for comment in comments_inputs:
                comment_key = (comment.user, comment.content, comment.comment_created_time)
                if comment_key in seen_comments:
                    continue
                seen_comments.add(comment_key)

                comment_user = self.user_map.get(comment.user) if self.user_map else None
                if comment_user is None:
                    comment_user = get_or_create_user(self.db, comment.user)
                self.user_map[comment_user.name] = comment_user

                new_comment = Comment(
                    post_id=post_id,
                    user_id=comment_user.id,
                    content=comment.content,
                    comment_created_time=comment.comment_created_time
                )
                new_comments.append(new_comment)

            comments = create_comments_bulk(self.db, new_comments)

            return comments
        except Exception as e:
            self.db.rollback()
            raise e

    def save_posts_from_postcrawls(self, post_inputs: List[PostCrawl]):
        try:
            post_finish = []
            post_exception_msgs = []
            for post_input in post_inputs:
                try:
                    # 將文章先加入資料庫
                    post_result = self.save_single_post(post_input)

                    # 若該文章有留言，加入資料庫
                    if post_result and post_input.comments:
                        self.save_comments_bulk(post_input.comments, post_result.id)

                    post_finish.append(post_result)
                except Exception as e:
                    # 存下遇到的錯誤，繼續存取其他文章
                    self.db.rollback()
                    post_exception_msgs.append(e)
                    logger.error(f"Error!: {e}")
                    continue

            return post_finish, post_exception_msgs
        except Exception as e:
            self.db.rollback()
            raise e
