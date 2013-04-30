# -*- coding: utf-8 -*-
import urllib2
import json
import ast
import thread

from datetime import date,datetime
import time

from operator import itemgetter
from bs4 import BeautifulSoup
from flask import jsonify
from redis import Redis

BASEURL = "http://forum.guns.ru/forum"

db = Redis()

proxy_support = urllib2.ProxyHandler({"http":"http://192.168.0.169:3128"})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

#-------------------------------Parsing functions------------------------------------# 

def parse_theme(theme_section, theme_number):

	base_id = theme_section + ":" + theme_number

	url = BASEURL + "_light_message/" + theme_section + "/" + theme_number +"-"+ str(db.zcard(base_id)) +".html"

	print url

	getSite = urllib2.urlopen(url, timeout=300)

	site = getSite.read().replace("[/QUOTE]", "</blockquote>").replace("[/B]", "</b>").replace("[", "<").replace("]", ">").replace("pes_i_kot", "</blockquote>")

	soup = BeautifulSoup(site, from_encoding = "windows-1251")

	soup.head.decompose()

	for center_tag in soup("center"):
		center_tag.decompose()

	for br_tag in soup("br"):
		if (br_tag):
			br_tag.decompose()

	for font_tag in soup("font"):
		try:
			font_tag.decompose()
		except:
			pass

	# for fail_tag in soup.find_all(text="[/QUOTE]")
	# 	fail_tag

	# images = []
	# i = 0

	for quote_tag in soup("blockquote"):
		for hr_tag in quote_tag("hr"):
			hr_tag.decompose()
		#quote_tag.string = str(quote_tag).replace("[/QUOTE]", "</blockquote>")
		#quote_tag.string = str(quote_tag).replace("[/B]", "</b>")
		# q = soup.new_string("|"+quote_tag.get_text()+"|")
		# quote_tag.replace_with(q)

	#print soup.prettify().encode("utf-8", errors="ignore")

	soup = BeautifulSoup(soup.prettify())

	soup.body.unwrap()
	soup.html.unwrap()

	txt = unicode(soup).replace("<hr/>", '\n')

	txt_arr = txt.split('\n\n')

	txt_arr = filter(None, txt_arr)

	if (db.zcard(base_id) < len(txt_arr)):

		for post in txt_arr:
			s = BeautifulSoup(post)

			if (s.body):

				s.body.unwrap()
				s.html.unwrap()
				
				# for img_tag in soup("img"):
				# 	#images.append(img_tag['src'])
				# 	img = soup.new_tag('img')
				# 	img['src'] = img_tag['src'] #.replace("talks", "forum")
				# 	img_tag.replace_with(img)

				for p_tag in s("p"):
					p_tag.unwrap()

				if (s.small):

					user = s.b.get_text().strip()
					post_date = s.small.get_text().strip().split()[0]
					post_time = s.small.get_text().strip().split()[1]

					post_datetime = datetime.strptime(s.small.get_text().strip(),'%d-%m-%Y %H:%M')

					timestamp = time.mktime(post_datetime.timetuple())

					s.b.decompose()
					s.small.decompose()

					html_text = unicode(s).strip().replace("talks", "forum")

					signature = ""

					try: 
						text = html_text.split("------------------")
						html_text = text[0].strip()
						signature = text[1].strip()
					except:
						pass

					post_dict = {"user":user, "timestamp":timestamp, "html_text":html_text, "signature":signature}

					db.zadd(base_id, post_dict, timestamp)

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
			section_id = theme_url.rsplit('/',1)[0].rsplit('/',1)[1]

			if (theme_url.find(".html") != -1 and theme_url.find("http://") != -1):
				try:
					reply_count = table_row.find_all(width = "15%")[0].get_text().strip().split()[0]

					try:
						int(reply_count)
					except:
						pass
					
					time_stamp = table_row.find_all(width = "21%")[0].get_text().strip()

					begins_year = ""
					begins_month = ""
					begins_day = ""

					last_year = ""
					last_month = ""
					last_day = ""
					last_time = ""

					if (time_stamp.find("->") == -1):
						begins_day = last_day = str(date.today().day)
						begins_month = last_month = str(date.today().month)
						begins_year = last_year = str(date.today().year)

						last_time = time_stamp
					else:
						time_stamp = time_stamp.split("->")

						if (len(time_stamp) == 1 ):

							begins_day = last_day = str(date.today().day)
							begins_month = last_month = str(date.today().month)
							begins_year = last_year = str(date.today().year)

							last_time = timestamp[0]

						if (len(time_stamp) == 2):
							theme_begins = time_stamp[0].split('-')

							if (len(theme_begins) == 3):
								begins_day = theme_begins[0]
								begins_month = theme_begins[1]
								begins_year = theme_begins[2].strip()
							if (len(theme_begins) == 2):
								begins_day = theme_begins[0]
								begins_month = theme_begins[1]
								begins_year = str(date.today().year)

							theme_last_post = time_stamp[1].split()

							if (len(theme_last_post) == 1):
								last_day = str(date.today().day)
								last_month = str(date.today().month)
								last_year = str(date.today().year)

								last_time = theme_last_post[0].strip()

							if (len(theme_last_post) == 2):

								theme_last_post_DMY = last_day = theme_last_post[0].strip().split('-')

								if (len(theme_last_post_DMY) == 2):
									last_year = str(date.today().year)
									last_day = theme_last_post_DMY[0]
									last_month = theme_last_post_DMY[1]

								if (len(theme_last_post_DMY) == 3):
									last_year = theme_last_post_DMY[2]
									last_day = theme_last_post_DMY[0]
									last_month = theme_last_post_DMY[1]

								last_time = theme_last_post[1]


						if (table_row.find_all(size = "1")): table_row.find_all(size = "1")[0].decompose()

					last_post_datetime_string = last_day + "-" + last_month + "-" + last_year + " " + last_time

					last_post_datetime = datetime.strptime(last_post_datetime_string,'%d-%m-%Y %H:%M')

					timestamp = time.mktime(last_post_datetime.timetuple())

					creator = table_row.find_all(width = "12%")[0].get_text().strip()
					theme_name = table_row.find_all(width = "46%")[0].get_text().strip().split('\n')[0]
					
					theme_dict = ({"id":theme_id, "section":section_id, \
							"creator":creator, "name":theme_name, \
							"timestamp":timestamp})

					db.sadd(base_id, theme_dict)

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
		if (a_tag['href'].find("index") != -1 and a_tag['href'].find(".html") != -1):

			section_url = a_tag['href']
			section_name = a_tag.get_text().strip()
			section_id = int(section_url.rsplit('/',1)[1].split('.',1)[0])

			sections_dict = ({"id":section_id, "name":section_name, "url":section_url})

			db.sadd("index", sections_dict)

def parse_subindex(subindex_id):

	base_id = "index:" + str(subindex_id)

	url = BASEURL + "index/" + str(subindex_id) + ".html"

	getSite = urllib2.urlopen(url)
	soup = BeautifulSoup(getSite, from_encoding = "windows-1251")
	soup = BeautifulSoup(soup.prettify())

	soup.head.decompose()

	for font_tag in soup("font"):
		font_tag.decompose()

	sections = []
	for a_tag in soup("a"):
		if (a_tag['href'].find("topics") != -1):

			section_url = a_tag['href']
			section_name = a_tag.get_text().strip()
			section_id = section_url.rsplit('/',1)[1].split('.',1)[0]

			sections_dict = ({"id":section_id, "name":section_name, "url":section_url})

			db.sadd(base_id, sections_dict)

def parse_daily():

	url = BASEURL + "daily.html"

	getSite = urllib2.urlopen(url)
	soup = BeautifulSoup(getSite, from_encoding = "koi8-r")
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

	for table_row in soup("tr"):
		if (table_row.a):
			theme_url = table_row.a['href'].replace("-0","")
			if (theme_url.find(".html") != -1 and theme_url.find("http://") != -1):

				
				theme_id = theme_url.rsplit('/',1)[1].split('.',1)[0]
				section_id = theme_url.rsplit('/',1)[0].rsplit('/',1)[1]
				
				theme_name = table_row.a.get_text().strip()

				section_name = table_row.find_all(size="2")[1].get_text().strip()

				last_year = str(date.today().year)
				last_month = str(date.today().month)
				last_day = str(date.today().day)
				last_time = table_row.find(size="Unknown Tag: DateSize").get_text().strip()

				last_post_datetime_string = last_day + "-" + last_month + "-" + last_year + " " + last_time

				last_post_datetime = datetime.strptime(last_post_datetime_string,'%d-%m-%Y %H:%M %p')

				timestamp = time.mktime(last_post_datetime.timetuple())

				themes_dict = ({"id":theme_id, "section":section_id, "name":theme_name, "timestamp":timestamp, "section_name":section_name})

				db.zadd("daily", themes_dict, float(time.time()+20))

#----------------------------------Get functions------------------------------------#
def get_daily():

	base_id = "daily"

	db.zremrangebyscore(base_id, 0, time.time());
	if (db.zcard(base_id)):
		thread.start_new_thread( parse_daily, () )
	else:
		parse_daily()

	
	themes_strings = db.zrange(base_id, 0, -1)

	themes = []
	for t in themes_strings:
		themes.append(ast.literal_eval(t))

	return jsonify({"themes":themes})


def get_section(section_number):

	base_id = "section:" + str(section_number)

	if (db.scard(base_id)):
		thread.start_new_thread( parse_section, (section_number, ) )
	else:
		parse_section(section_number)

	themes_strings = db.smembers(base_id)

	themes = []
	for t in themes_strings:
		themes.append(ast.literal_eval(t))

	return jsonify({"themes":themes})

def get_theme(theme_section, theme_number, count = 0, continue_from = 0, get_to = time.time()):

	base_id = theme_section + ":" + theme_number

	if (db.zcard(base_id)):
		thread.start_new_thread( parse_theme, (theme_section, theme_number, ) )
	else:
		parse_theme(theme_section, theme_number, )

	if (count > 0 and continue_from > 0):
		posts_strings = db.zrangebyscore(base_id, continue_from, get_to)
		posts_strings = posts_strings[0:count]
		print get_to
	elif (count > 0):
		posts_strings = db.zrange(base_id, 0, count - 1)
	else:
		posts_strings = db.zrangebyscore(base_id, continue_from, get_to)

	posts = []
	for p in posts_strings:
		posts.append(ast.literal_eval(p))

	return jsonify({"posts":posts})

def get_all_sections():
	base_id = "index"

	subindexes_strings = db.smembers(base_id)
	subindexes = []
	for s in subindexes_strings:
		subindexes.append(ast.literal_eval(s))

	sections = []
	for subindex in subindexes:
		basepath = base_id + ":" + str(subindex["id"])

		sections_strings = db.smembers(basepath)

		for s in sections_strings:
			sections.append(ast.literal_eval(s))

	return jsonify({"sections":sections})

def get_index():
	base_id = "index"

	if (db.scard(base_id)):
		thread.start_new_thread( parse_index, ())
	else:
		parse_index()

	sections_strings = db.smembers(base_id)

	sections = []
	for s in sections_strings:
		sections.append(ast.literal_eval(s))

	return jsonify({"sections":sections})

def get_subindex(subindex_id):
	base_id = "index:" + str(subindex_id)

	if (db.scard(base_id)):
		thread.start_new_thread( parse_subindex, (subindex_id, ))
	else:
		parse_subindex(subindex_id)

	sections_strings = db.smembers(base_id)

	sections = []
	for s in sections_strings:
		sections.append(ast.literal_eval(s))

	return jsonify({"sections":sections})
	
