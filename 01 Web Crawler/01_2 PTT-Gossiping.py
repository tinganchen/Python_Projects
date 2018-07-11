"""
Outline

# 1. Request
# 2. Dissect the HTML webpage
# 3. Input- dissected webpage, date when articles are going to be scraped
#    Output- current page articles, url of the previous page
# 4. Scrape all articles published today from current and prvious pages
# 5. Select and print the Hot articles whose times of push are over
#    a specific threshold

"""
import requests
from bs4 import BeautifulSoup
import time

ptt_url = "https://www.ptt.cc"
topic = "Gossiping"
ptt_gossip_url = ptt_url + "/bbs/" + topic + "/index.html"

# 1. Request
def request(url):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
              "AppleWebKit/537.36 (KHTML, like Gecko)"
              "Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url, headers = header, cookies = {"over18":"1"})

# 2. Dissect the HTML webpage
def diss_html(req):
    if req.status_code == requests.codes.ok:
        req.encoding = "utf8"
        soup = BeautifulSoup(req.text, "lxml")
    else:
        print("HTTP request fails...")
        soup = None
    return soup

# 3. Input- dissected webpage, date when articles are going to be scraped
#    Output- current page articles, url of the previous page
def get_articles_info(soup, date):
    articles = []
    tag_article = soup.find_all("div", class_ = "r-ent")
    for tag in tag_article:
        # Discriminate if the date is same as "date" (means today here) input 
        article_date = tag.find("div", class_ = "date").text.strip(" ")
        if  article_date == date:
            # Title, link
            tag_title = tag.find("a")
            if tag_title:
                title = tag_title.text
                link = ptt_url + tag_title["href"]
                author = tag.find("div", class_ = "author").text
                # Push Count
                push_count = tag.find("div", class_ = "nrec").text
                if push_count:
                    try:
                        push_count = int(push_count)
                    except ValueError:
                        if push_count == "爆":
                            push_count = 99
                        else:
                            push_count = -1
                else: 
                    push_count = 0 #
                    
                articles.append({
                        "Title" : title,
                        "Link" : link,
                        "Author" : author,
                        "Push_Count" : push_count})
                
    # Previous pages may contain articles pulished on the "date" (today)
    tag_paging = soup.find("div", class_ = "btn-group btn-group-paging")
    prev_url = ptt_url + tag_paging.find_all("a")[1]["href"]
    
    return articles, prev_url       

# 4. Scrape all articles published today from current and prvious pages
def web_scraping_bot(url):
    articles = []
    soup = diss_html(request(url))
    today = time.strftime("%m/%d").lstrip("0")
    today_article, prev_url = get_articles_info(soup, today)
    while today_article:
        articles += today_article
        soup = diss_html(request(prev_url))
        today_article, prev_url = get_articles_info(soup, today)
    return articles         

# 5. Select and print the Hot articles whose times of push are over
#    a specific threshold
def hot_articles(url, threshold):
    ptt_today_articles = web_scraping_bot(url)
    print("Number of articles published on PTT-{0} today: {1}".format(
            topic, len(ptt_today_articles)))   
    print("Hot Articles! Pushed over {0} times!\n".format(threshold),
          "------------------------------")
    for article in ptt_today_articles:
        if article["Push_Count"] > threshold:
            for info in dict.values(article):
                print(info)

ptt = ptt_gossip_url
threshold = 50
Hot_articles_today = hot_articles(ptt, threshold)
# Hot_articles_today