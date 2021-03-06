# -*- coding: utf-8 -*-

import imp

parser = imp.load_source('parser', './parser.py')

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

@app.route('/user/<string:user>')
def show_user(user):
	return get_user(user)

@app.route('/sections', methods=['POST', 'GET'])
def sections():
	return get_sections_list()

@app.route('/<string:section>', methods=['POST', 'GET'])
def show_section(section):
	return get_section(section)

@app.route('/<string:section>/<string:theme>', methods=['POST', 'GET'])
def show_theme(section, theme):
	return get_theme(section, theme)

@app.route('/<string:section>/<string:theme>-<int:count>', methods=['POST', 'GET'])
def show_theme_count(section, theme, count):
	return get_theme(section, theme, count)

@app.route('/<string:section>/<string:theme>:<float:continue_from>-<int:count>', methods=['POST', 'GET'])
def show_theme_from_time(section, theme, count, continue_from):
	return get_theme(section, theme, count, continue_from)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
