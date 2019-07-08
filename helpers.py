import csv
import hashlib

def user_registration(name, email, username, password, mobile, description):
	users = get_users()

	for user in users:
		if(user['email'] == email or user['username'] == username or user['mobile'] == mobile):
			return {'error': True, 'message': 'Registration failed, user already exists'}
			
	save_user([get_hash(username), name, email, get_hash(password), username, mobile, description])
	return {'error': False, 'message': 'Registration Success'}

def user_login(username, password):
	users = get_users()
	password_hash = get_hash(password)

	for user in users:
		if (user['username'] == username):
			if (user['password'] == password_hash):
				return {'error': False, 'token': user['token']} 

	return {'error': True, 'message': 'Invalid login creadentials'}


def get_users():
	users = []
	
	with open('data/users.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		users = list(reader)

	return users


def get_user(username):
	users = get_users()

	for user in users:
		if (user['username'] == username):
			return user

	return {}


def save_user(user):
	user_string = ",".join(user)
	users_file = open("data/users.csv","a")
	users_file.write("\n" + user_string)
	users_file.close()

	return


def get_hash(input):
	input = input.encode('utf-8')
	return hashlib.md5(input).hexdigest()