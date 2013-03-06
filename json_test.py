# -*- coding: utf-8 -*-
import urllib2
import json

from bs4 import BeautifulSoup
from datetime import *

# from flask import Flask, redirect, jsonify
# from redis import Redis

# app = Flask(__name__)
# app.debug = True

# page = urllib.urlopen("test1.html")

# doc = lxml.html.document_fromstring(page.read())

# txt1 = doc.xpath('/html/body/center/table[5]/tbody/tr[3]/text()')

#"http://forum.guns.ru/forum_light_message/92/507831.html"

def parse_theme(url):
	getSite = urllib2.urlopen(url)

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

		if (s.small):

			user = s.b.get_text().strip()
			date = s.small.get_text().strip()

			s.b.decompose()
			s.small.decompose()

			text = s.get_text().strip()

			posts.append({'user':user, 'date':date, 'text':text})

	return json.dumps(posts, sort_keys=True, indent=2)

def parse_section(url):
	getSite = urllib2.urlopen(url)
	soup = BeautifulSoup(getSite, from_encoding = "windows-1251")
	soup = BeautifulSoup(soup.prettify())
	
	soup.head.decompose()

	for script_tag in soup("script"):
		script_tag.decompose()

	# for font_tag in soup("font"):
	# 	font_tag.unwrap()

	for img in soup("img"):
		img.decompose()

	for table in soup("table"):
		table.unwrap()

	themes = []
	for table_row in soup("tr"):
		if (table_row.a):
			theme_url = table_row.a['href']
			if (theme_url.find(".html") != -1 and theme_url.find("http://") != -1):

				time_stamp = table_row.find_all(width = "21%")[0].get_text().strip().split('->')

				begins_year = ""
				begins_month = ""
				begins_day = ""

				if (len(time_stamp) == 2):
					last_post_begin = time_stamp[0].split('-')

					if (len(last_post_begin) == 3):
						begins_day = last_post_begin[0]
						begins_month = last_post_begin[1]
						begins_year = last_post_begin[2].strip()
					if (len(last_post_begin) == 2):
						begins_day = last_post_begin[0]
						begins_month = last_post_begin[1]
						begins_year = str(date.today().year)

					if (table_row.find_all(size = "1")):table_row.find_all(size = "1")[0].decompose()


				creator = table_row.find_all(width = "12%")[0].get_text().strip()
				theme_name = table_row.find_all(width = "46%")[0].get_text().strip()
				
				

				themes.append({"url":theme_url, \
						"creator":creator, "name":theme_name, \
						"begins_year":begins_year, "begins_month":begins_month, "begins_day":begins_day})

	return json.dumps(themes, sort_keys=True, indent=2)


pageName = "http://forum.guns.ru/forumtopics/92.html"

print parse_section(pageName)
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

