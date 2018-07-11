"""
Outline

"""

import requests
from bs4 import BeautifulSoup
import re

def get_url(keyword_search, page_no):
    url_type = "http://search.books.com.tw/search/query/cat/all/key/{0}/sort/1/page/{1}/v/0/"
    url = url_type.format(keyword_search, page_no)
    return url

def request_parse(url):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
              "AppleWebKit/537.36 (KHTML, like Gecko)"
              "Chrome/63.0.3239.132 Safari/537.36"}
    res = requests.get(url, headers = header)
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def get_isbn(book_url):
    soup = request_parse(book_url)
    isbn = soup.find("div", class_ = "mod_b type02_m058 clearfix").li.text[5:]
    return isbn

def books_web_scrape(url):
    books = []
    soup = request_parse(url)
    tag_books = soup.find_all(class_ = "item")
    
    for tag_book in tag_books:
        book = []
        tag_h3 = tag_book.find("h3")
        name = tag_h3.text.replace("\n", "").replace("\t", "")
        book.append(name)
        
        book_url = "http://www.books.com.tw/products/" + tag_book.input["value"]     
        isbn = get_isbn(book_url)
        book.append(isbn)
        
        tag_price = tag_book.find(class_ = "price")
        tag_price_b = tag_price.find_all("b")
        # Avoid the situation that a book is without discount, i.e. only one <b> 
        price = tag_price_b[len(tag_price_b)-1].text  
        book.append(price)
        books.append(book)
    return books

word_search = "python"
page1_soup = request_parse(get_url(word_search, 1))
tag_about = page1_soup.find(class_ = "about")
page_count = re.search(" \d+", str(tag_about)).group(0).strip()
all_pages_books = []
# for page_no in range(1, int(page_count) + 1):
# Take int(page_count)=2 for substitution to avoid much runtime due to many pages
for page_no in range(1, 2 + 1):
    url = get_url(word_search, page_no)
    curr_page_books = books_web_scrape(url)
    all_pages_books += curr_page_books
all_pages_books
