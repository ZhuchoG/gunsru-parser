from flask import Flask, redirect, jsonify
from redis import Redis

app = Flask(__name__)
app.debug = True

db = Redis()

@app.route('/')
def hello():
	return redirect('/static/index.html')

@app.route('/vote/<int:voteid>', methods=['POST'])
def vote(voteid):
	if not (0 <= voteid <= 2):
		return jsonify({'error': 'strange vote!'})
	res = db.incr('foto:vote:' + str(voteid))
	return jsonify({'result': res, 'foto': voteid})

if __name__ == '__main__':
	app.run()