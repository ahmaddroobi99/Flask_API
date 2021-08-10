from flask_restful import Resource, abort, fields, marshal_with
from flask import jsonify, request, make_response
from initialize import task_put_args, task_update_args
from main import db, app
import jwt
import datetime
from functools import wraps


class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Task(title = {self.title}, status = {self.status})"


resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "status": fields.Integer,  # here i put it as integer to be like specific values in the database
    # like 0 for not completed,1 competed ,2 delayed ...etc
}


class Task(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id):
        result = TaskModel.query.filter_by(
            id=task_id
        ).first()  # filtering like in js in web
        if not result:
            abort(404, message="Could not find task with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, task_id):
        args = task_put_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if result:
            abort(409, message="task id taken...")

        task = TaskModel(id=task_id, title=args["title"], status=args["status"])
        db.session.add(task)
        db.session.commit()
        return task, 201

    @marshal_with(resource_fields)
    def patch(self, task_id):
        args = task_update_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="Task doesn't exist, cannot update")

        if args["title"]:
            result.title = args["title"]
        if args["status"]:
            result.status = args["status"]

        db.session.commit()

        return result

    # def delete(self, task_id):
    #     abort_if_task_id_doesnt_exist(task_id)
    #     del tasks[task_id]
    #     return '', 204

    # now we add Authentications login and stuff lik that to our RESt_API

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.args.get(
                "token"
            )  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

            if not token:
                return jsonify({"message": "Token is missing!"}), 403

            try:
                data = jwt.decode(token, app.config["SECRET_KEY"])
            except:
                return jsonify({"message": "Token is invalid!"}), 403

            return f(*args, **kwargs)

        return decorated

    @app.route("/unprotected")
    def unprotected(self):
        return jsonify({"message": "Anyone can view this!"})

    @app.route("/protected")
    @token_required
    def protected(self):
        return jsonify(
            {"message": "This is only available for people with valid tokens."}
        )

    @app.route("/login")
    def login(self):
        auth = request.authorization

        if auth and auth.password == "secret":
            token = jwt.encode(
                {
                    "user": auth.username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=15),
                },
                app.config["SECRET_KEY"],
            )

            return jsonify({"token": token.decode("UTF-8")})

        return make_response(
            "Could not verify!",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )
