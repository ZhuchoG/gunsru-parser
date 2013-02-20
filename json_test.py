from flask import Flask, redirect, jsonify
from redis import Redis

app = Flask(__name__)
app.debug = True

db = Redis()

@app.route('/')
def hello():
	return jsonify({'result': 'test', 'foto': 'test'})

@app.route('/vote/<int:voteid>', methods=['POST'])
def vote(voteid):
	return jsonify({'result': 'test', 'foto': 'test'})

if __name__ == '__main__':
	app.run()