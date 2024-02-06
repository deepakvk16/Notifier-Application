from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import time

import Email

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument("--disable-gpu")

mails = [('acc31r0ck@gmail.com',)]


def nhce_news():
    file1 = open("href.txt", "r+")
    old_event = file1.readline()

    url = 'https://newhorizoncollegeofengineering.in/events/'
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.get(url)
    print("refreshing webpage...")
    # Wait for webpage to load
    time.sleep(3)

    new_event = driver.find_element(By.XPATH, '//*[@id=' + '"tab-expired"' + ']/div[1]')
    a = new_event.find_element(By.TAG_NAME, "a")
    link = a.get_attribute("href")

    if link != old_event:
        file1 = open("href.txt", "w")
        file1.write(link)

        img = new_event.find_element(By.TAG_NAME, "img")
        title = a.get_attribute("text")
        src = img.get_attribute("src")

        timing = new_event.find_element(By.CLASS_NAME, "date")
        day = timing.get_attribute("innerHTML")
        timing = new_event.find_element(By.CLASS_NAME, "month")
        month = timing.get_attribute("innerHTML")

        Email.news_mail(title, link, src, day, month, mails)

    file1.close()


nhce_news()
