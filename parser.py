# -*- coding: utf-8 -*-
import urllib2
import json

from bs4 import BeautifulSoup
from datetime import *

from flask import jsonify

BASEURL = "http://forum.guns.ru/forum"

def parse_theme(theme_section, theme_number, continue_from = "0"):

	url = BASEURL + "_light_message/" + theme_section + "/" + theme_number +"-"+ continue_from +".html"

	getSite = urllib2.urlopen(url)

	soup = BeautifulSoup(getSite, from_encoding = "windows-1251")

	soup.head.decompose()

	for center_tag in soup("center"):
		center_tag.decompose()

	for br_tag in soup("br"):
		if (br_tag):
			br_tag.decompose()

	for font_tag in soup("font"):
		font_tag.decompose()

	# images = []
	# i = 0
	# for img_tag in soup("img"):
	# 	images.append(img_tag['src'])
	# 	img = soup.new_string("["+unicode(i)+"]")
	# 	img_tag.replace_with(img)
	# 	i += 1

	for quote_tag in soup("blockquote"):
		for hr_tag in quote_tag("hr"):
			hr_tag.decompose()
		# q = soup.new_string("|"+quote_tag.get_text()+"|")
		# quote_tag.replace_with(q)

	soup = BeautifulSoup(soup.prettify())

	soup.body.unwrap()
	soup.html.unwrap()

	txt = unicode(soup).replace("<hr/>", '\n')

	txt_arr = txt.split('\n\n')

	txt_arr = filter(None, txt_arr)

	posts = []

	for post in txt_arr:
		s = BeautifulSoup(post)
		s.body.unwrap()
		s.html.unwrap()
		
		for p_tag in s("p"):
			p_tag.unwrap()

		if (s.small):

			user = s.b.get_text().strip()
			date = s.small.get_text().strip().split()[0]
			time = s.small.get_text().strip().split()[1]

			s.b.decompose()
			s.small.decompose()

			text = unicode(s).strip()

			posts.append({"user":user, "date":date, "time":time, "text":text})

	return jsonify({"posts":posts})

def parse_section(section_number):

	url = BASEURL + "topics/" + section_number + ".html"

	getSite = urllib2.urlopen(url)
	soup = BeautifulSoup(getSite, from_encoding = "windows-1251")
	soup = BeautifulSoup(soup.prettify())
	
	title = soup.title.get_text().split(":")[0].strip()

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
			theme_id = theme_url.rsplit('/',1)[1].split('.',1)[0]

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
				reply_count = table_row.find_all(width = "15%")[0].get_text().strip().split()[0]
				
				themes.append({"id":theme_id, "url":theme_url, \
						"creator":creator, "name":theme_name, \
						"reply_count":reply_count, \
						"begins_year":begins_year, "begins_month":begins_month, "begins_day":begins_day})

	return jsonify({"title":title, "themes":themes})

def parse_index():
	url = BASEURL + "index"

	getSite = urllib2.urlopen(url)
	soup = BeautifulSoup(getSite, from_encoding = "windows-1251")
	soup = BeautifulSoup(soup.prettify())

	soup.head.decompose()

	for script_tag in soup("script"):
		script_tag.decompose()

	for img in soup("img"):
		img.decompose()

	for table in soup("table"):
		table.unwrap()

	return str(soup)
