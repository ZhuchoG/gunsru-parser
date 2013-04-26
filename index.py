# -*- coding: utf-8 -*-

import imp

parser = imp.load_source('parser', '/var/www/gunsru-api/parser.py')

from parser import *

from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/-<string:subindex>')
def show_subindex(subindex):
	return get_subindex(subindex)

@app.route('/')
def index():
	return get_index()

@app.route('/daily')
def show_daily():
	return get_daily()

@app.route('/<string:section>', methods=['POST', 'GET'])
def show_section(section):
	return get_section(section)

@app.route('/<string:section>/<string:theme>', methods=['POST', 'GET'])
def show_theme(section, theme):
	return get_theme(section, theme)

@app.route('/<string:section>/<string:theme>:<float:from_time>', methods=['POST', 'GET'])
def show_theme_from_time(section, theme, from_time):
	return get_theme(section, theme, from_time)

@app.route('/<string:section>/<string:theme>:<float:from_time>:<float:to_time>', methods=['POST', 'GET'])
def show_theme_from_time_to_time(section, theme, from_time, to_time):
	return get_theme(section, theme, from_time, to_time)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
