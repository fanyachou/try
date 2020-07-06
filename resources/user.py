from flask import jsonify, make_response
from flask_restful import Resource, reqparse
import pymysql

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class Users(Resource):

	def db_init(self):
		db = pymysql.connect(
			'localhost',
			'fanya',
			'qwer',
			'flask_demo'
			)
		cursor = db.cursor(pymysql.cursors.DictCursor)
		return db,cursor

	def get(self):
		db, cursor = self.db_init()
		sql = 'SELECT * FROM flask_demo.new_table where deleted = False;'
		cursor.execute(sql)
		users = cursor.fetchall()
		db.close()


		return jsonify(users)

	def post(self):
		db, cursor = self.db_init()
		arg= parser.parse_args()
		user = {
			'name':arg['name'],
			'gender':arg['gender'],
			'birth':arg['birth'] or '1900-01-01',
			'note':arg['note'],

		}
		sql = """
			INSERT INTO `flask_demo`.`new_table` (`name`, `gender`, `birth`, `note`) 
			VALUES ('{}', '{}', '{}', '{}');
		""".format(user['name'],user['gender'],user['birth'],user['note'])

		result = cursor.execute(sql)
		db.commit()
		db.close()
		response = {"msg":'success'}
		code =201
		if result==0:
			response['msg']='error'
			code =400
		return make_response(jsonify(response),code)


class User(Resource):

	def db_init(self):
		db = pymysql.connect(
			'localhost',
			'fanya',
			'qwer',
			'flask_demo'
			)
		cursor = db.cursor(pymysql.cursors.DictCursor)
		return db,cursor

	def get(self, id):
		db, cursor = self.db_init()
		sql = 'SELECT * FROM flask_demo.new_table where id ={};'.format(id)
		cursor.execute(sql)
		user = cursor.fetchone()
		db.close()


		return jsonify(user)

	def delete(self, id):
		db, cursor = self.db_init()
		# sql = 'DELETE FROM `flask_demo`.`new_table` where id ={};'.format(id)
		sql = 'UPDATE `flask_demo`.`new_table` SET deleted = True where id ={};'.format(id)

		result = cursor.execute(sql)
		db.commit()
		db.close()
		response = {'code':200, "msg":'success'}

		if result==0:
			response['msg']='error'
		return jsonify(response)


		return jsonify(user)




	def patch(self,id):
		db, cursor = self.db_init()
		arg= parser.parse_args()
		user = {
			'name':arg['name'],
			'gender':arg['gender'],
			'birth':arg['birth'] or '1900-01-01',
			'note':arg['note'],

		}
		query = []
		for key,value in user.items():
			if value != None:
				query.append(key + "=" + " '{}' ".format(value))
		query = ",".join(query)

		sql = """
		UPDATE `flask_demo`.`new_table` 
		SET {} WHERE id = {};
		""".format(query,id)
		result = cursor.execute(sql)

		db.commit()
		db.close()
		response = {'code':200, "msg":'success'}

		if result==0:
			response['msg']='error'
		return jsonify(response)
