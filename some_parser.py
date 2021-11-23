import re
import pymysql
import requests as req
from selenium import webdriver
from bs4 import BeautifulSoup

def GetTrailerLink(trailer):
    #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    # пример маршрута C:/Users/USERNAME/OneDrive/Рабочий стол/Parser
    chromedriver = "ВСТАВЬТЕ_СЮДА/chromedriver"
    #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    browser.get(trailer)
    requiredHtml = browser.page_source
    soup = BeautifulSoup(requiredHtml, 'html5lib')
    YouLink = soup.find("iframe", {"frameborder": "0"}).get("src")
    YouLink = re.split(r'/', YouLink)
    YouLink = re.split(r'\?', YouLink[4])
    YouLink = YouLink[0]
    YouLink = "https://www.youtube.com/watch?v=" + YouLink
    return YouLink

resp = req.get("SOME_SITE_FOR_PARSE")

soup = BeautifulSoup(resp.text, 'lxml')
links = soup.find_all("loc")

for i in links:
    resp = req.get(i.text)
    soup = BeautifulSoup(resp.text, 'lxml')

    title = soup.find("div", class_="movie-title").find("h1")
    title = title.text

    if "Фильм" in title:
        title = re.split(r'[\(\d\)]', title)
        title = title[0]
        title = title.split("Фильм ")[1]

        discription = soup.find("div", class_="movie-desc full-text clearfix")
        discription = discription.text.split("Описание: ")[1].split("\n")[0]

        year = soup.find("div", class_="ml-desc")
        year = year.text

        genres = soup.find("div", class_="ml-desc1").find_all("a")
        final = ""
        for a in genres:
            final = final + "," + a.text
            final = final.lstrip(",")

        poster = soup.find("div", class_="movie-poster").find("img")
        poster = "http://tvtuk.online" + poster.get("src")

        trailer = soup.find("iframe", {"width": "610"})
        trailer = trailer.get("src")
        trailer = GetTrailerLink(trailer)

        video = soup.find("iframe", {"width": "560"})
        if video == None:
            continue
        else:
            video = "http:" + video.get("src")
            if "videocdn" in video:
                video = soup.find("iframe", {"width": "560"})
                video = "http:" + video.get("src")
                #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                # пример маршрута C:/Users/Kumamon/OneDrive/Рабочий стол/Parser
                chromedriver = "ВСТАВЬТЕ_СЮДА/chromedriver"
                #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--log-level=3')
                browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
                browser.get(video)
                requiredHtml = browser.page_source
                soup = BeautifulSoup(requiredHtml, 'html5lib')
                VidLink = soup.find("video").get("src")
                VidLink = "http:" + VidLink
                VidLink = VidLink[0:-7]
                cat = "Фильмы"
                #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                #ЗДЕСЬ УКАЖИТЕ ДАННЫЕ ДЛЯ ПОДКЛЮЧЕНИЯ К БД
                con = pymysql.connect('IP or DOMAIN', 'USER',
                                      'PASS', 'DB')
                #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                mycursor = con.cursor()
                video240 = VidLink + "240.mp4"

                sql = "INSERT INTO mainMovies (title, description, genre, year, urlvideo, urlimage, trailer, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (title, discription, final, year, video240, poster, trailer, cat)
                mycursor.execute(sql, val)

                video360 = VidLink + "360.mp4"
                sql = "INSERT INTO mainMovies (title, description, genre, year, urlvideo, urlimage, trailer, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (title, discription, final, year, video360, poster, trailer, cat)
                mycursor.execute(sql, val)

                video480 = VidLink + "480.mp4"
                sql = "INSERT INTO mainMovies (title, description, genre, year, urlvideo, urlimage, trailer, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (title, discription, final, year, video480, poster, trailer, cat)
                mycursor.execute(sql, val)

                video720 = VidLink + "720.mp4"
                sql = "INSERT INTO mainMovies (title, description, genre, year, urlvideo, urlimage, trailer, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (title, discription, final, year, video720, poster, trailer, cat)
                mycursor.execute(sql, val)

                video1080 = VidLink + "1080.mp4"
                sql = "INSERT INTO mainMovies (title, description, genre, year, urlvideo, urlimage, trailer, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (title, discription, final, year, video1080, poster, trailer, cat)
                mycursor.execute(sql, val)
                con.commit()

                print("One Added")
            else:
                continue

    else:
        print("None")

