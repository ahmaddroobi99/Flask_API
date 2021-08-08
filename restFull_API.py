from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(title = {self.title}, status = {self.status})"


task_put_args = reqparse.RequestParser()
task_put_args.add_argument("title", type=str, help="title of the task is required", required=True)
task_put_args.add_argument("status", type=int, help="status of the Task", required=True)

task_update_args = reqparse.RequestParser()
task_update_args.add_argument("title", type=str, help="title of the task to be updated is required")
task_update_args.add_argument("status", type=int, help="status of the Task to be updated")

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'status': fields.Integer, #vhere i put it as integer to be like specific values in the database
                              #like 0 for not completed,1 competed ,2 delayed ...etc

}


class Task(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id):
        result = TaskModel.query.filter_by(id=task_id).first()  #filtering like in js in web
        if not result:
            abort(404, message="Could not find task with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, task_id):
        args = task_put_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if result:
            abort(409, message="task id taken...")

        task = TaskModel(id=task_id, title=args['title'], status=args['status'])
        db.session.add(task)
        db.session.commit()
        return task, 201

    @marshal_with(resource_fields)
    def patch(self, task_id):
        args = task_update_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="Task doesn't exist, cannot update")

        if args['title']:
            result.name = args['title']
        if args['status']:
            result.views = args['status']

        db.session.commit()

        return result

    # def delete(self, task_id):
    #     abort_if_task_id_doesnt_exist(task_id)
    #     del tasks[video_id]
    #     return '', 204


api.add_resource(Task, "/task/<int:task_id>")

if __name__ == "__main__":
    app.run(debug=True)
