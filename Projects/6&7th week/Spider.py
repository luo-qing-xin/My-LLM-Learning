# 这是用来爬虫豆瓣2025年度图书榜单的代码，
# 包含了获取榜单书籍、获取书籍详情、保存 JSONL 和主程序四个部分。
# 请确保在运行前安装了 requests 和 beautifulsoup4 库。

import requests
import json
import time
from bs4 import BeautifulSoup

# -----------------------
# 基础请求头
# -----------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://book.douban.com/annual/2025/",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

URL = "https://book.douban.com/j/neu/page/34/"

# -----------------------
# 1. 获取榜单书籍
# -----------------------
def fetch_books():
    res = requests.get(URL, headers=HEADERS)
    data = res.json()
    books_all = []

    for widget in data.get("widgets", []):
        source_data = widget.get("source_data")
        if not source_data:
            continue

        # ---------- 情况1：dict ----------
        if isinstance(source_data, dict):
            # 榜单名称
            collection = source_data.get("subject_collection", {})
            category = collection.get("title")

            # ⭐ 修复点：items 从 source_data 取
            items = source_data.get("subject_collection_items", [])

            for idx, book in enumerate(items):
                books_all.append({
                    "title": book.get("title"),
                    "url": book.get("url"),
                    "rating": book.get("rating", {}).get("value"),
                    "rating_count": book.get("rating", {}).get("rating_count"),
                    "category": category,
                    "rank": idx + 1
                })

        # ---------- 情况2：list ----------
        elif isinstance(source_data, list):
            for entry in source_data:
                collection = entry.get("subject_collection", {})
                category = collection.get("title")

                # ⭐ 同样修复
                items = entry.get("subject_collection_items", [])

                for idx, book in enumerate(items):
                    books_all.append({
                        "title": book.get("title"),
                        "url": book.get("url"),
                        "rating": book.get("rating", {}).get("value"),
                        "rating_count": book.get("rating", {}).get("rating_count"),
                        "category": category,
                        "rank": idx + 1
                    })

    return books_all

# -----------------------
# 2. 获取书籍详情
# -----------------------
def fetch_detail(book_url):
    try:
        res = requests.get(book_url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return {}
    except:
        return {}

    soup = BeautifulSoup(res.text, "lxml")
    info = {}

    # 简介
    intro = soup.select("#link-report span")
    if intro:
        info["intro"] = intro[0].get_text(strip=True)

    # 标签
    tags = soup.select("#db-tags-section a")
    info["tags"] = [tag.get_text(strip=True) for tag in tags]

    # 基本信息
    info_block = soup.select_one("#info")
    if info_block:
        lines = info_block.get_text("\n", strip=True).split("\n")
        for line in lines:
            if "作者" in line:
                info["author"] = line.replace("作者:", "").strip()
            elif "出版社" in line:
                info["publisher"] = line.replace("出版社:", "").strip()
            elif "出版年" in line:
                info["pub_time"] = line.replace("出版年:", "").strip()
            elif "ISBN" in line:
                info["isbn"] = line.replace("ISBN:", "").strip()
    return info

# -----------------------
# 3. 保存 JSONL
# -----------------------
def save_jsonl(book, filename="books.jsonl"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(book, ensure_ascii=False) + "\n")

# -----------------------
# 4. 主程序
# -----------------------
def main():
    print("抓取榜单书籍...")
    books = fetch_books()
    print(f"共抓取 {len(books)} 本书（未去重）")

    for book in books:
        print(f"抓取: {book['category']} #{book['rank']} - {book['title']}")
        detail = fetch_detail(book["url"])
        book.update(detail)
        save_jsonl(book)
        time.sleep(2)  # 防封

    print("已保存到 books.jsonl")

if __name__ == "__main__":
    main()