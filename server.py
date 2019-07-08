from bottle import Bottle, run
from bottle import HTTPResponse, request
from helpers import *
import json

app = Bottle()

@app.route('/')
def index():
	return "MASAI SCHOOL"


@app.route('/auth/register', method='POST')
def auth_register():
	name = request.json.get('name')
	email = request.json.get('email')
	username = request.json.get('username')
	password = request.json.get('password')
	mobile = request.json.get('mobile')
	description = request.json.get('description')

	registration = user_registration(name, email, username, password, mobile, description)

	return json.dumps(registration)


@app.route('/auth/login', method='POST')
def auth_login():
	username = request.json.get('username')
	password = request.json.get('password')

	login = user_login(username, password)

	if (login['error']):
		return HTTPResponse(status=401, body=json.dumps(login))
	else:
		return json.dumps(login)


@app.route('/user/<username>')
def user(username):
	authorization = request.get_header('Authorization')
	auth = authorization.split(' ')
	user = get_user(username)

	if (len(auth) == 2 and auth[0] == 'Bearer'):
		if ('token' in user and auth[1] == user['token']):
			del user['password']
			return json.dumps(user)
		else:
			return HTTPResponse(status=401, body=json.dumps({'message': "Invalid token for user"}))
	else:
		return HTTPResponse(status=401, body=json.dumps({'message': "Invalid authentication request"}))


run(app, host='localhost', port=8080, reloader=True, debug=True)