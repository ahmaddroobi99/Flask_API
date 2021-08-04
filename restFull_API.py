from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort ,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLAlCHEMY_DATABASE_URI']='sqlite:///database.db'
db =SQLAlchemy(app)

class VideoModel (db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(100),nullable=False)
    views =db.Column(db.Integer,nullable=False)
    likes =db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f'Video(name={self.name},views={self.views},likes={self.likes})'





# names={"tala":{"age":19,"gender":"male"},
#        "ahmad":{"age":99,"gender":"male"},}
#
# class Helloword(Resource):
#     # def get(self,name,test):
#     #     return {"name": name,"test":test}
#     #
#     # def post (self):
#     #     return {"data":"Posted "}
#
#     def get (self,name):
#         return names[name]

video_put_arg = reqparse.RequestParser()
video_put_arg.add_argument("name", type=str, help="Nmae of the video", required=True)
video_put_arg.add_argument("views", type=int, help="views of the video", required=True)
video_put_arg.add_argument("likes", type=int, help="likes of the video", required=True)


# videos = {}
#
#
# def abort_if_video_doesnt_exist(video_id):
#     if video_id not in videos:
#         abort(404, message="video id is not valid..")
#
#
# def abort_if_video_exist(video_id):
#     if video_id in videos:
#         abort(409, message="Video exist with that ID...")

resourse_field ={
   'id': fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer

}

@app.route("/")
class Video(Resource):
    @marshal_with(resourse_field)
    def get(self, video_id):
        # abort_if_video_doesnt_exist(video_id)
        result = VideoModel.query.filter_by(id=video_id).first()
        return result

    @marshal_with(resourse_field)
    def put(self, video_id):
        # abort_if_video_exist(video_id)
        args = video_put_arg.parse_args()
        video = VideoModel(id=video_id,name= args['name'],views =args['views'],likes =args['likes'])
        db.session.add(video)
        db.session.commit()
        return video,201

    def delete(self, video_id):
        # abort_if_video_doesnt_exist(video_id)
        del videos[video_id]
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)
