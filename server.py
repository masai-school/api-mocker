from bottle import Bottle, run
from bottle import HTTPResponse, request, response
from helpers import *
import json

app = Bottle()

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'


@app.route('/', method=['OPTIONS', 'GET'])
def index():
	if request.method == 'OPTIONS':
		return {}
	else:
		return "MASAI SCHOOL"


@app.route('/codenames/<os>', method=['OPTIONS', 'GET'])
def codenames(os):
	if request.method == 'OPTIONS':
		return {}
	else:
		if os == 'android':
			android = [{"version": 9, "name": "Pie"}, {"version": 8, "name": "Oreo"}, {"version": 7, "name": "Nougat"}]
			return json.dumps({"os": "android", "codenames": android})
		elif os == 'ubuntu':
			ubuntu = [{"version": 19.04, "name": "Disco Dingo"}, {"version": 18.04, "name": "Bionic Beaver"}, {"version": 17.04, "name": "Zesty Zapus"}]
			return json.dumps({"os": "ubuntu", "codenames": ubuntu})
		elif os == 'windows':
			windows = [{"version": 10, "name": "Redstone"}, {"version": 8, "name": "Jupiter"}, {"version": 7, "name": "Blackcomb"}]
			return json.dumps({"os": "windows", "codenames": windows})
		elif os == 'macos':
			macos = [{'version': 10.14, "name": "Mojave"}, {"version": 10.13, "name": "High Sierra"}, {"version": 10.11, "name": "El Capitan"}]
			return json.dumps({"os": "macos", "codenames": macos})
		else:
			return json.dumps({"os": os, "codenames": []})


@app.route('/auth/register', method=['OPTIONS', 'POST'])
def auth_register():
	if request.method == 'OPTIONS':
		return {}
	else:
		name = request.json.get('name')
		email = request.json.get('email')
		username = request.json.get('username')
		password = request.json.get('password')
		mobile = request.json.get('mobile')
		description = request.json.get('description')

		registration = user_registration(name, email, username, password, mobile, description)

		return json.dumps(registration)


@app.route('/auth/login', method=['OPTIONS', 'POST'])
def auth_login():
	if request.method == 'OPTIONS':
		return {}
	else:
		username = request.json.get('username')
		password = request.json.get('password')

		login = user_login(username, password)

		if (login['error']):
			return HTTPResponse(status=401, body=json.dumps(login))
		else:
			return json.dumps(login)


@app.route('/user/<username>', method=['OPTIONS', 'GET'])
def user(username):
	if request.method == 'OPTIONS':
		return {}
	else:
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