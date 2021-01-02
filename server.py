from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
import jwt
from termcolor import colored

app = Flask(__name__)
api = Api(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flight_database.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config ['SECRET_KEY'] = 'neverFound'

db = SQLAlchemy(app)

# init databases
class FlightDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_city = db.Column(db.String(32), nullable=False) 
    to_city = db.Column(db.String(32), nullable=False)
    departure_time = db.Column(db.String(32), nullable=False)
    arrival_time = db.Column(db.String(32), nullable=False)
    airplane_info = db.Column(db.String(64), nullable=False)
    passengers_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return {'flight_id': self.id, 'from': self.from_city, 'to': self.to_city}

class Admin(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"Username: {username}, Password: {password}"

# parse request
post_args = reqparse.RequestParser()

post_args.add_argument('from_city', type=str, help='Please, enter model name of car', nullable=False)
post_args.add_argument('to_city', type=str, help='Please, enter company name of manufacturer', nullable=False)
post_args.add_argument('departure_time', type=str, help='Please, enter vehicle type of car', nullable=False)
post_args.add_argument('arrival_time', type=str, help='Please, enter transmission type of car', nullable=False)
post_args.add_argument('airplane_info', type=str, help='Please, enter introduction date of car', nullable=False)
post_args.add_argument('passengers_count', type=int, help='Please, enter introduction date of car', nullable=False)
post_args.add_argument('token', type=str, help="Authorization token", nullable=False)

update_args = reqparse.RequestParser()
update_args.add_argument('flight_id', type=int, help='Please, enter flight id', nullable=False)
update_args.add_argument('from_city', type=str, help='Please, enter model name of car')
update_args.add_argument('to_city', type=str, help='Please, enter company name of manufacturer')
update_args.add_argument('departure_time', type=str, help='Please, enter vehicle type of car')
update_args.add_argument('arrival_time', type=str, help='Please, enter transmission type of car')
update_args.add_argument('airplane_info', type=str, help='Please, enter introduction date of car')
update_args.add_argument('passengers_count', type=int, help='Please, enter introduction date of car')
update_args.add_argument('token', type=str, help="Authorization token", nullable=False)

delete_args = reqparse.RequestParser()
delete_args.add_argument('flight_id', type=int, help='Please, enter flight id', nullable=False)
delete_args.add_argument('token', type=str, help="Authorization token", nullable=False)


admin_args = reqparse.RequestParser()
admin_args.add_argument('username', type=str, nullable=False)
admin_args.add_argument('password', type=str, nullable=False)

logout_args = reqparse.RequestParser()
logout_args.add_argument('token', type=str, nullable=False)

#resource fields
resource_fields = {
    'from_city': fields.String,
    'to_city': fields.String,
    'departure_time': fields.String,
    'arrival_time': fields.String,
    'passengers_count': fields.Integer
}
tokens = {}

class ManipulateFlights(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = post_args.parse_args()
        print(args.token)
        if args.token not in tokens.values():
            abort(401, message="Not authorized for this operation")
        
        flight = FlightDB(from_city=args['from_city'], to_city=args['to_city'], departure_time=args['departure_time'], 
                    arrival_time=args['arrival_time'], airplane_info=args['airplane_info'], passengers_count=args['passengers_count'])
        db.session.add(flight)
        db.session.commit()

        return flight, 201

    @marshal_with(resource_fields)
    def put(self):
        args = update_args.parse_args()
        if args.token not in tokens.values():
            abort(401, message="Not authorized for this operation")
        result = FlightDB.query.filter_by(id=args.flight_id).first()
        # print(args.token)
        if not result:
            abort(404, message="Flight doesn't exist")
        if args['from_city']:
            result.from_city = args['from_city'] 
        if args['to_city']:
            result.to_city = args['to_city']
        if args['departure_time']:
            result.departure_time = args['departure_time']
        if args['arrival_time']:
            result.arrival_time = args['arrival_time']
        if args['airplane_info']:
            result.airplane_info = args['airplane_info']
        if args['passengers_count']:
            result.passengers_count = args['passengers_count']
        
        db.session.commit()
        
        return result, 201

    @marshal_with(resource_fields)
    def delete(self):
        args = delete_args.parse_args()
        if args.token not in tokens.values():
            abort(401, message="Not authorized for this operation")
        result = FlightDB.query.filter_by(id=args.flight_id).first()
        if not result:
            abort(404, message="No flight with that id")
        db.session.delete(result)
        db.session.commit()
        return '', 204

class Get_Flight(Resource):
    @marshal_with(resource_fields)
    def get(self, from_city, to_city):
        result = FlightDB.query.filter_by(from_city=from_city, to_city=to_city).first()
        if not result:
            abort(404, message="No flight")
        return result

class AUTH(Resource):
    def post(self):
        args = admin_args.parse_args()
        admin = Admin.query.filter_by(username = args['username'], password = args['password']).first()
        if not admin:
            abort(404, message="Invalid username or password")
        token = jwt.encode({'username': admin.username, 'password': admin.password}, app.config['SECRET_KEY'])
        tokens[args.username] = token
        # print(colored(f"{type(token)} \ | /{token}", 'red'))
        return jsonify({'token': token})

class Logout(Resource):
    def post(self):
        args = logout_args.parse_args()
        if args.token not in tokens.values():
            abort(408, message="Not logged in")
        for key, value in tokens.copy().items():
            if value == args.token:
                del tokens[key]
        return {"message": "Logged out succesfully"}, 200
        

api.add_resource(ManipulateFlights, "/flights") # Admin Post
api.add_resource(Get_Flight, "/flights/<string:from_city>/<string:to_city>") # User
api.add_resource(AUTH, "/authentication_authorization") # Authentication
api.add_resource(Logout, "/end_session") # Logout

def main():
    app.run(debug=True)
    # db.create_all()

if __name__ == '__main__':
    main()