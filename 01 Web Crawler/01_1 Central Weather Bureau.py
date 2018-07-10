"""
Outline

# 1. Define a function to Get requests and Dissect the html webpages
# 2. Websites to be scraped
# 3. Define a function to Scrape all wanted info. (city) in array type
# 4. Define attributes' name
# 5. Write all info. from 3. into a CSV. file (Country)
  
"""

import requests
from bs4 import BeautifulSoup
import csv
# import time
import re

# 1. Define a function to Get requests and Dissect the html webpages
def request_dissect(url):
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        req.encoding = "utf8"
        soup = BeautifulSoup(req.text, "lxml")
        return soup
    else: 
        print("HTTP request fails....")
        
# 2. Websites to be scraped
url1 = "https://www.cwb.gov.tw/V7/forecast/taiwan/Keelung_City.htm"
soup1 = request_dissect(url1)
tag_all_city = soup1.find(id = "ContentTitle").find_all("option")
url_index = [city["value"] for city in tag_all_city]
urls = []
for index in url_index:
    url = "https://www.cwb.gov.tw/V7/forecast/taiwan/{0}".format(index)
    urls.append(url)
# print(urls)

# 3. Define a function to Scrape all wanted info. (city) in array type
def web_scraping_bot(url):
    soup = request_dissect(url)
    city = soup.find("table").th.string
    tag_t_row = soup.find("table").tbody.find_all("tr")

    table_array = []       
    for row in tag_t_row:
        rowList = []
        rowList.append(city)
        rowList.append(re.match("\w+ ", row.th.text).group(0).replace(" ", ""))
        for cell in row.find_all("td"):
            cell_text = cell.text.replace("\n", "").replace("\r", "").replace(" ", "")
            if len(cell_text) == 0:
                rowList.append(cell.img["title"])
            else:
                rowList.append(cell_text)
        table_array.append(rowList)
    return table_array

# 4. Define attributes' name
attr_name = ["City", "Time", "Tempature", "Weather", "Comfort_Index", "Prob_Precipitation"]
    
# 5. Write all info. from 3. into a CSV. file (Country)
with open("01_1 Weather_Taiwan.csv", "a", newline = '') as file:
    write_in = csv.writer(file)
    write_in.writerow(attr_name)     
    for city_url in urls:
        for time_section in web_scraping_bot(city_url):
            write_in.writerow(time_section)
        """
        print("Waite five seconds...")
        time.sleep(5)
        """

