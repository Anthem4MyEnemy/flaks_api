from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


data = [{
      "reference_number": "96321478",
      "location": "21485214521",
      "destination": "45214521",
      "timeslot": "08:55",
      "id": 52
    },
    {
      "reference_number": "789",
      "location": "jjj",
      "destination": "jjj",
      "date": "2018-10-30",
      "timeslot": "12:01",
      "user_id": "99635",
      "id": 53
    }
]


app = Flask(__name__)
api = Api(app)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class PackageModel(db.Model):
	id =db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, nullable = False)
	reference_number = db.Column(db.String(50), nullable = False)
	location = db.Column(db.String(50), nullable = False)
	destination = db.Column(db.String(50), nullable = False)
	date = db.Column(db.String(30), nullable = False)
	timeslot = db.Column(db.String(20), nullable = False)
	

	def __repr__():
		return f"location = {location}, destination = {destination}, date = {date}, timeslot = {timeslot}"


db.create_all()
#Validate the data that is sent to us
#:reference_number, :location, :destination, :date, :timeslot, :user_id
package_put_args = reqparse.RequestParser()
package_put_args.add_argument("user_id",type=str, help="Unique User ID",required =True)
package_put_args.add_argument("reference_number",type=str, help="Destination to travel from",required =True)
package_put_args.add_argument("destination",type=str, help="Destination to travel from",required =True)
package_put_args.add_argument("location",type=str, help="Location is required",required =True)
package_put_args.add_argument("date",type=str, help="Date in Date format is required",required =True)
package_put_args.add_argument("timeslot",type=str, help="Time in 24h time format is required",required =True)

'''
packages ={}

#If looking for data of an user_id that does not exist it doesn't crash
def abort_if_id_not_exits(user_id):
	if (user_id not in packages):
		abort(404, message = "Could not find user")

#See if user exists and abourt to not overwrite user
def abort_if_video_exist(user_id):
	if(user_id in packages):
		abort(409, message= "User already exists")
'''
resource_fields = {
	'id': fields.Integer,
	'user_id':fields.Integer,
	'reference_number': fields.String,
	'location':fields.String,
	'destination':fields.String,
	'date':fields.String,
	'timeslot':fields.String
}

update_args = reqparse.RequestParser()
update_args.add_argument("user_id",type=int, help="Destination to travel from")
update_args.add_argument("destination",type=str, help="Destination to travel from")
update_args.add_argument("location",type=str, help="Location")
update_args.add_argument("date",type=str, help="Date in Date format")
update_args.add_argument("timeslot",type=str, help="Time in 24h time format")
update_args.add_argument("reference_number",type=str, help="Unique reference number")

class Package(Resource):
	@marshal_with(resource_fields)
	def get(self,user_id):
		result = PackageModel.query.all()
		if not result:
			abort(404, message = "ID does not exist")
		return result

	#edit package in databas with user_is
	@marshal_with(resource_fields)
	def patch(self,user_id):
		args = update_args.parse_args()
		result = PackageModel.query.filter_by(id= user_id).first()
		if not result:
			abort(404, message = "Package does not exist, cannot update")
		
		if args['location']:
			result.location = args['location']
		if args['destination']:
			result.destination = args['destination']
		if args['date'] :
			result.date = args['date']
		if args['timeslot'] :
			result.timeslot = args['timeslot']
		if args['reference_number'] :
			result.reference_number = args['reference_number']
		if args['user_id']:
			result.user_id = args['user_id']

		db.session.commit()

		return result 

	#Add new package to database
	@marshal_with(resource_fields)
	def put(self,user_id):
		args = package_put_args.parse_args()
		#See if ID already exits
		result = PackageModel.query.filter_by(id= user_id).first()
		if result:
			abort(409, message = "ID already exist")
		package = PackageModel(id = user_id, user_id=args['user_id'], reference_number=args['reference_number'] ,location=args['location'],destination = args['destination'], date = args['date'], timeslot = args['timeslot'])
		db.session.add(package)
		db.session.commit()
		#201 code for created
		return package,201

	#delete package from database with user_id
	def delete(self,user_id):
		PackageModel.query.filter_by(id=user_id).delete()
		db.session.commit()
		#204 deleted succesfully
		return '',204


api.add_resource(Package,"/package/<int:user_id>")

#For logging in
@app.route('/login',methods = ['POST'])
def get_login_data():
	email = request.form.get('email')
	password = request.form.get('password')
	return {'email':'123@1'},200


if __name__ == "__main__":
	app.run(debug=True)