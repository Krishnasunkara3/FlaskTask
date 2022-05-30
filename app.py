from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Starting the flask
app = Flask(__name__)
api = Api(app)


# Connecting with postgresql server

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/Flask"
db = SQLAlchemy(app)

# Creating student model
class StudentModel(db.Model):
    __tablename__ = "students"
    StudentId = db.Column(db.Integer, primary_key=True)
    StudentName = db.Column(db.String(100), nullable=False)
    StudentClass = db.Column(db.String(50), nullable=False)
    StudentAge = db.Column(db.Integer, nullable=False)
    StudentAddress = db.Column(db.String(100))
    def __init__(self, StudentId, StudentName, StudentClass, StudentAge, StudentAddress):
        self.StudentId = StudentId
        self.StudentName = StudentName
        self.StudentClass = StudentClass
        self.StudentAge = StudentAge
        self.StudentAddress = StudentAddress


student_args = reqparse.RequestParser()
student_args.add_argument("StudentId", type=int, help="Student id is required", required=True)
student_args.add_argument("StudentName", type=str, help="Student name is required", required=True)
student_args.add_argument("StudentClass", type=str, help="Student name is required", required=True)
student_args.add_argument("StudentAge", type=int, help="Student id is required", required=True)
student_args.add_argument("StudentAddress", type=str, required=False)

student_put_args = reqparse.RequestParser()
student_put_args.add_argument("StudentId", type=int, help="Student id is required")
student_put_args.add_argument("StudentName", type=str, help="Student name is required")
student_put_args.add_argument("StudentClass", type=str, help="Student name is required")
student_put_args.add_argument("StudentAge", type=int, help="Student id is required")
student_put_args.add_argument("StudentAddress", type=str)

resource_fields = {
                        'StudentId': fields.Integer,
                        'StudentName': fields.String,
                        'StudentClass': fields.String,
                        'StudentAge': fields.Integer,
                        'StudentAddress': fields.String
                 }


class Student(Resource):
    @marshal_with(resource_fields)
    def get(self, StudentId):
        result = StudentModel.query.filter_by(StudentId=StudentId).first()
        if not result:
            abort(404, message="student id not available")
        return result

    @marshal_with(resource_fields)
    def post(self, StudentId):
        args = student_args.parse_args()
        result = StudentModel.query.filter_by(StudentId=StudentId).first()
        if result:
            abort(404, message="student id  is already available")

        student_details = StudentModel(StudentId=StudentId, StudentName=args["StudentName"],
                                       StudentClass=args["StudentClass"], StudentAge=args["StudentAge"],
                                       StudentAddress=args["StudentAddress"])
        db.session.add(student_details)
        db.session.commit()
        return student_details, 201

    @marshal_with(resource_fields)
    def put(self, StudentId):
        args = student_put_args.parse_args()
        result = StudentModel.query.filter_by(StudentId=StudentId).first()

        if not result:
            abort(404, message="student id not available")

        if args["StudentName"]:
            result.StudentName = args["StudentName"]

        if args["StudentClass"]:
            result.StudentClass = args["StudentClass"]

        if args["StudentAge"]:
            result.StudentAge = args["StudentAge"]

        if args["StudentAddress"]:
            result.StudentAddress = args["StudentAddress"]

        db.session.commit()

        return result

    def delete(self, StudentId):
        result = StudentModel.query.filter_by(StudentId=StudentId).first()
        if not result:
            abort(404, message="student id not available")

        db.session.delete(result)
        db.session.commit()

        return {StudentId: 'student id is deleted'}, 204


class SearchByName(Resource):
    @marshal_with(resource_fields)
    def get(self, StudentName):
        result = StudentModel.query.filter_by(StudentName=StudentName).all()
        if not result:
            abort(404, message="student name not available")
        return result


api.add_resource(Student, '/student/<string:StudentId>')
api.add_resource(SearchByName, '/student1/<string:StudentName>')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6001, debug=True)
