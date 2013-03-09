# -*- coding: utf-8 -*-

from parser import *

from flask import Flask, redirect, jsonify
from redis import Redis

app = Flask(__name__)
app.debug = True

db = Redis()

# @app.route('/')
# def hello():
# 	return redirect('/static/index.html')

@app.route('/<string:section>/<string:theme>', methods=['POST', 'GET'])
def show_theme(section, theme):
	# if not (0 <= voteid <= 2):
	# 	return jsonify({'error': 'strange vote!'})
	# res = db.incr('foto:vote:' + str(voteid))
	return parse_theme(section, theme)

@app.route('/<string:section>', methods=['POST', 'GET'])
def show_section(section):
	
	return parse_section(section)

if __name__ == '__main__':
	app.run()