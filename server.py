#!/usr/bin/python3
from flask import Flask, request, jsonify,render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///CustomersDB.db')
app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
  return render_template('index.html')

class Customers(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from customers") # This line performs query and returns json result
        return {'Customers': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
   
    
class Customer_Data(Resource):
    def get(self, customer_id):
        conn = db_connect.connect()
        query = conn.execute("select * from Customers where id=%d "  %int(customer_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Customers, '/customers') # Route_1
api.add_resource(Customer_Data, '/customers/<customer_id>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')
