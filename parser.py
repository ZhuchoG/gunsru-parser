# -*- coding: utf-8 -*-
import urllib2
import json
import ast
import thread

from bs4 import BeautifulSoup
from datetime import *

from flask import jsonify
from redis import Redis

BASEURL = "http://forum.guns.ru/forum"

db = Redis()

#-------------------------Parsing functions------------------------------------# 

def parse_theme(theme_section, theme_number, continue_from = "0"):

	base_id = theme_section + ":" + theme_number

	url = BASEURL + "_light_message/" + theme_section + "/" + theme_number +"-"+ str(db.llen(base_id)) +".html"

	print url

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

	if (db.llen(base_id) < len(txt_arr)):

		for post in txt_arr:
			s = BeautifulSoup(post)

			if (s.body):

				s.body.unwrap()
				s.html.unwrap()
				
				for p_tag in s("p"):
					p_tag.unwrap()

				images_height = 0
				for img_tag in s("img"):
					try:
						images_height += int(img_tag['height'])
					except:
						images_height += 0

				if (s.small):

					user = s.b.get_text().strip()
					date = s.small.get_text().strip().split()[0]
					time = s.small.get_text().strip().split()[1]

					s.b.decompose()
					s.small.decompose()

					html_text = unicode(s).strip()

					text = s.get_text().strip();

					post_dict = {"user":user, "date":date, "time":time, "html_text":html_text, "text":text, "images_height":images_height};

					db.rpush(base_id, post_dict)

def parse_section(section_number):

	base_id = "section:" + str(section_number)

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
				try:
					reply_count = table_row.find_all(width = "15%")[0].get_text().strip().split()[0]

					try:
						int(reply_count)
					except:
						continue

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
					theme_name = table_row.find_all(width = "46%")[0].get_text().strip().split('\n')[0]
					
					
					theme_dict = ({"id":theme_id, "url":theme_url, \
							"creator":creator, "name":theme_name, \
							"reply_count":reply_count, \
							"begins_year":begins_year, "begins_month":begins_month, "begins_day":begins_day})

					db.rpush(base_id, theme_dict)

				except:
					pass

def parse_index():
	url = BASEURL + "index"

	getSite = urllib2.urlopen(url)
	soup = BeautifulSoup(getSite, from_encoding = "windows-1251")
	soup = BeautifulSoup(soup.prettify())

	soup.head.decompose()

	sections = []
	for a_tag in soup("a"):
		if (a_tag['href'].find("topics") != -1):

			section_url = a_tag['href']
			section_name = a_tag.get_text().strip()
			section_id = section_url.rsplit('/',1)[1].split('.',1)[0]

			sections_dict = ({"id":section_id, "name":section_name, "url":section_url})

			db.rpush("index", sections_dict)

	# for script_tag in soup("script"):
	# 	script_tag.decompose()

	# for img in soup("img"):
	# 	img.decompose()

	# for table in soup("table"):
	# 	table.unwrap()

	# return jsonify({"sections":sections})

#-----------------------Get functions--------------------------------#

def get_section(section_number):

	base_id = "section:" + str(section_number)

	if (db.llen(base_id)):
		thread.start_new_thread( parse_section, (section_number, ) )
	else:
		parse_section(section_number)

	themes_strings = db.lrange(base_id, 0, -1)

	themes = []
	for t in themes_strings:
		themes.append(ast.literal_eval(t))

	return jsonify({"themes":themes})

def get_theme(theme_section, theme_number):

	base_id = theme_section + ":" + theme_number

	if (db.llen(base_id)):
		thread.start_new_thread( parse_theme, (theme_section, theme_number, ) )
	else:
		parse_theme(theme_section, theme_number)

	posts_strings = db.lrange(base_id, 0, -1)

	posts = []
	for p in posts_strings:
		posts.append(ast.literal_eval(p))

	return jsonify({"posts":posts})

def get_index():
	base_id = "index"

	if (db.llen(base_id)):
		thread.start_new_thread( parse_index, ())
	else:
		parse_index()

	sections_strings = db.lrange(base_id, 0, -1)

	sections = []
	for s in sections_strings:
		sections.append(ast.literal_eval(s))

	return jsonify({"sections":sections})
