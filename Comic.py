from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from webdriver_manager.chrome import ChromeDriverManager
from datetime import date
import mysql.connector
import Email

# Establish connection with mySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1@nc310t",
    database="notification"
)

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument("--disable-gpu")

my_cursor = mydb.cursor()


def manga_plus():
    # get list of comic titles
    my_cursor.execute("SELECT DISTINCT cname FROM emails")
    comic_list = my_cursor.fetchall()

    url = 'https://mangaplus.shueisha.co.jp/manga_list/updated'
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.get(url)
    print("refreshing webpage...")

    try:
        # Get titles of comics with new chapters from the website
        new_titles = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "LastUpdatedTitle-module_allTitle_20kmL"))
        )
        for titles in new_titles[0:5]:
            # title = WebDriverWait(titles, 2).until(
            #    ec.presence_of_element_located((By.CLASS_NAME, "LastUpdatedTitle-module_title_3HJEY")))
            title = titles.find_element(By.CLASS_NAME, "LastUpdatedTitle-module_title_3HJEY")
            # print(title.text)
            for comic in comic_list:
                if title.text == comic[0]:
                    print("found title match! " + comic[0])
                    # getting image and link of the comic
                    link = titles.get_attribute("href")
                    img = WebDriverWait(titles, 5).until(
                        ec.visibility_of_element_located((By.CSS_SELECTOR, "img[src]")))
                    # img = titles.find_element(By.CLASS_NAME, "LastUpdatedTitle-module_image_33lsO")
                    src = img.get_attribute("src")
                    print(src)
                    last_read(link, comic[0], src)
    finally:
        driver.quit()


def last_read(link, comic, src):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.get(link)
    today = date.today()
    d = today.strftime("%Y-%m-%d")

    my_cursor.execute("SELECT last_ch FROM comics where cname = '" + comic + "'")
    last_ch = my_cursor.fetchall()

    print("loading the comic page...")
    try:
        # get list of new chapters in comic
        new_chapters = WebDriverWait(driver, 5).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "ChapterListItem-module_title_3Id89"))
        )
        recent_chapter = new_chapters[-1]

        # check if the notification for the new chapter has already been sent
        if recent_chapter.text != last_ch[0]:
            print("sending mail...")
            my_cursor.execute("SELECT email_id FROM emails WHERE cname = '" + comic + "'")
            emails = my_cursor.fetchall()

            my_cursor.execute("UPDATE comics SET last_ch = '" + recent_chapter.text +
                              "', last_read = '" + d + "' WHERE cname = '" + comic + "'")
            mydb.commit()

            print(recent_chapter.text)
            Email.comic_mail(comic, recent_chapter.text, link, emails, src)
        else:
            print("already read " + last_ch[0])
    finally:
        driver.quit()


manga_plus()
