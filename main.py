import flask
from flask import request
from flask_restful import Api,Resource
from resources.user import Users, User

app = flask.Flask(__name__)
app.config["DEBUG"]=True
api=Api(app)
api.add_resource(Users,"/users")
api.add_resource(User,"/user/<id>")

@app.errorhandler(Exception)
def handle(error):
	status_code = 500
	if type(error).__name__ =='NotFound':
		code = 404
	return {
		'msg':type(error).__name__
	}, code

@app.before_request
def auth():
	token = request.headers.get('auth')
	if token == '567':
		pass
	else:
		return {
			'msg':'invalid token',
		}, 401

@app.route('/',methods=['GET'])
def home():
	return "Hello"

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=3333)