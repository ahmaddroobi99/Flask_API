from flask import Flask, request
from flask_restful import Api, Resource,reqparse,abort


app = Flask(__name__)
api = Api(app)

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

video_put_arg =reqparse.RequestParser()
video_put_arg.add_argument("name",type=str,help="Nmae of the video",required=True)
video_put_arg.add_argument("views",type=int,help="views of the video",required=True)
video_put_arg.add_argument("likes",type=int,help="likes of the video",required=True)



videos ={}
def abort_if_video_doesnt_exist (video_id):
    if video_id not in videos :
        abort("video id is not valid..")



@app.route("/")
class Video (Resource):

    def get(self,video_id):
        return videos[video_id]

    def put (self,video_id):
        args =video_put_arg.parse_args()
        videos[video_id]=args
        return {video_id:args}




api.add_resource(Video,"/video/<int:video_id>")




if __name__ == "__main__":
    app.run(debug=True)
