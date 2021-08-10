from flask_restful import reqparse
from models import Task
from main import api


task_put_args = reqparse.RequestParser()
task_put_args.add_argument(
    "title", type=str, help="title of the task is required", required=True
)
task_put_args.add_argument("status", type=int, help="status of the Task", required=True)

task_update_args = reqparse.RequestParser()
task_update_args.add_argument(
    "title", type=str, help="title of the task to be updated is required"
)
task_update_args.add_argument(
    "status", type=int, help="status of the Task to be updated"
)


api.add_resource(Task, "/task/<int:task_id>")
