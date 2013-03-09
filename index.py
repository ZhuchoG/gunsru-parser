# -*- coding: utf-8 -*-

from parser import *

from flask import Flask

app = Flask(__name__)
app.debug = True

# @app.route('/')
# def hello():
# 	return redirect('/static/index.html')

@app.route('/<string:section>/<string:theme>', methods=['POST', 'GET'])
def show_theme(section, theme):
	return parse_theme(section, theme)

@app.route('/<string:section>/<string:theme>:<string:from_post>', methods=['POST', 'GET'])
def show_theme_from_post(section, theme, from_post):
	return parse_theme(section, theme, from_post)

@app.route('/<string:section>', methods=['POST', 'GET'])
def show_section(section):
	
	return parse_section(section)

if __name__ == '__main__':
	app.run()