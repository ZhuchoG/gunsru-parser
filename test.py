# -*- coding: utf-8 -*-

import imp

parser = imp.load_source('parser', './parser.py')

from parser import *

from flask import Flask
from flask import jsonify

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	sections = []
	sections.append({"id":"1", "name":"testsubindex1", "url":"tttt"})
	sections.append({"id":"2", "name":"testsubindex2", "url":"tttt"})
	sections.append({"id":"3", "name":"testsubindex3", "url":"tttt"})
	sections.append({"id":"4", "name":"testsubindex4", "url":"tttt"})
	return jsonify({"sections":sections})

@app.route('/-<string:subindex>')
def show_subindex(subindex):
	sections = []
	if (subindex == "1"):
		sections.append({"id":"1", "name":"testsection1", "url":"tttt"})
		sections.append({"id":"2", "name":"testsection2", "url":"tttt"})
		sections.append({"id":"3", "name":"testsection3", "url":"tttt"})
		sections.append({"id":"4", "name":"testsection4", "url":"tttt"})
	if (subindex == "2"):
		sections.append({"id":"5", "name":"testsection5", "url":"tttt"})
		sections.append({"id":"6", "name":"testsection6", "url":"tttt"})
		sections.append({"id":"7", "name":"testsection7", "url":"tttt"})
		sections.append({"id":"8", "name":"testsection8", "url":"tttt"})
	if (subindex == "3"):
		sections.append({"id":"9", "name":"testsection9", "url":"tttt"})
		sections.append({"id":"10", "name":"testsection10", "url":"tttt"})
		sections.append({"id":"11", "name":"testsection11", "url":"tttt"})
		sections.append({"id":"12", "name":"testsection12", "url":"tttt"})
	if (subindex == "4"):
		sections.append({"id":"13", "name":"testsection13", "url":"tttt"})
		sections.append({"id":"14", "name":"testsection14", "url":"tttt"})
		sections.append({"id":"15", "name":"testsection15", "url":"tttt"})
		sections.append({"id":"16", "name":"testsection16", "url":"tttt"})
	return jsonify({"sections":sections})

@app.route('/<string:section>', methods=['POST', 'GET'])
def show_section(section):
	themes = []

	themes.append({"id":str(int(section)+100), "url":"theme_url", \
				"creator":"creator", "name":"theme_name"+str(int(section)+100), \
				"reply_count":"20", \
				"timestamp":12345356.0, \
				"begins_year":"2013", "begins_month":"5", "begins_day":"14", \
				"last_post_month":"6", "last_post_day":"20", "last_post_time": "22:22"})
	themes.append({"id":str(int(section)+150), "url":"theme_url", \
				"creator":"creator", "name":"theme_name"+str(int(section)+150), \
				"reply_count":"20", \
				"timestamp":12345356.0, \
				"begins_year":"2013", "begins_month":"5", "begins_day":"14", \
				"last_post_month":"6", "last_post_day":"20", "last_post_time": "22:22"})
	themes.append({"id":str(int(section)+200), "url":"theme_url", \
				"creator":"creator", "name":"theme_name"+str(int(section)+200), \
				"reply_count":"20", \
				"timestamp":12345356.0, \
				"begins_year":"2013", "begins_month":"5", "begins_day":"14", \
				"last_post_month":"6", "last_post_day":"20", "last_post_time": "22:22"})

	return jsonify({"themes":themes})

@app.route('/<string:section>/<string:theme>', methods=['POST', 'GET'])
def show_theme(section, theme):
	posts = []

	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phaselo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"1"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"2"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"3"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"4"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"5"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"6"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"7"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"8"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"9"})
	posts.append({"user":"user", "date":"22-22-2222", "time":"22:22", "timestamp":12345356.0, "html_text":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc venenatis ligula magna, et interdum augue. Vivamus justo urna, imperdiet vel imperdiet sed, ornare non ipsum. Curabitur pretium erat id odio convallis at pretium lectus volutpat. Integer dictum, mauris quis auctor porta, sem leo gravida ligula, eget semper lectus leo in est. Phasellus commodo, mi vel semper lobortis, arcu libero porttitor est, eget aliquam lorem augue ut elit. Aliquam tristique justo sit amet neque commodo varius. Curabitur et felis quis odio venenatis tempor quis ac erat. Fusce congue, lectus id posuere elementum, libero quam dapibus erat, vitae varius erat augue nec ipsum."+section+theme+"10"})

	return jsonify({"posts":posts})

@app.route('/<string:section>/<string:theme>:<string:from_post>', methods=['POST', 'GET'])
def show_theme_from_post(section, theme, from_post):
	return get_theme(section, theme, from_post)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
