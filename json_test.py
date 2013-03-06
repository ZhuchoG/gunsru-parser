# -*- coding: utf-8 -*-
import urllib2
import json
from enc import *

from bs4 import BeautifulSoup

# from flask import Flask, redirect, jsonify
# from redis import Redis

# app = Flask(__name__)
# app.debug = True

# page = urllib.urlopen("test1.html")

# doc = lxml.html.document_fromstring(page.read())

# txt1 = doc.xpath('/html/body/center/table[5]/tbody/tr[3]/text()')

pageName = "http://forum.guns.ru/forum_light_message/92/507831-6832.html"

getSite = urllib2.urlopen(pageName)

soup = BeautifulSoup(getSite, from_encoding = "windows-1251")

soup.head.decompose()

for center_tag in soup("center"):
	center_tag.decompose()

for br_tag in soup("br"):
	br_tag.decompose()

for font_tag in soup("font"):
	font_tag.decompose()
	
for quote_tag in soup("blockquote"):
	for hr_tag in quote_tag("hr"):
		hr_tag.decompose()

soup = BeautifulSoup(soup.prettify())

soup.body.unwrap()
soup.html.unwrap()

txt = unicode(soup).replace("<hr/>", '\n')

txt_arr = txt.split('\n\n')

txt_arr = filter(None, txt_arr)

posts = []

for post in txt_arr:
	s = BeautifulSoup(post)

	user = s.b.get_text().strip()
	date = s.small.get_text().strip()

	s.b.decompose()
	s.small.decompose()

	text = s.get_text().strip()

	posts.append({'user':user, 'date':date, 'text':text})


#arr = [text for text in txt_arr if len(text) > 10]

print json.dumps(posts, sort_keys=True, indent=2)

#soup.encode('utf8')

# tag = soup.new_tag("b")
	# tag.string = font_tag.get_text().strip()
	# font_tag.replace_with(tag)

#txt_arr[0].encode('utf8')

#txt.encode('utf8')

# @app.route('/')
# def hello():
# 	return jsonify({'resulting': txt, 'foto': 'test'})


# if __name__ == '__main__':
# 	app.run()

