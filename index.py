# -*- coding: utf-8 -*-

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

@app.route('/<string:section>', methods=['POST', 'GET'])
def show_section(section):
	return get_section(section)

@app.route('/<string:section>/<string:theme>', methods=['POST', 'GET'])
def show_theme(section, theme):
	return get_theme(section, theme)

@app.route('/<string:section>/<string:theme>:<string:from_post>', methods=['POST', 'GET'])
def show_theme_from_post(section, theme, from_post):
	return parse_theme(section, theme, from_post)

if __name__ == '__main__':
	app.run()