# -*- coding: UTF-8 -*-

import urllib2
from bs4 import BeautifulSoup

# from flask import Flask, redirect, jsonify
# from redis import Redis

# app = Flask(__name__)
# app.debug = True

# page = urllib.urlopen("test1.html")

# doc = lxml.html.document_fromstring(page.read())

# txt1 = doc.xpath('/html/body/center/table[5]/tbody/tr[3]/text()')

soup = BeautifulSoup(urllib2.urlopen("http://forum.guns.ru/forummessage/92/507831.html"))

#txt1 = doc.xpath('/html/body/span[@class="simple_text"]/text()')
#txt2 = doc.xpath('/html/body/span[@class="cyrillic_text"]/following-sibling::text()[1]')

txt = soup.find_all("td")

# print txt

for link in soup.find_all('td'):
    print(link.get_text())

# @app.route('/')
# def hello():
# 	return jsonify({'resulting': txt, 'foto': 'test'})


# if __name__ == '__main__':
# 	app.run()