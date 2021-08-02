from flask import Flask
from flask_restful import Api,Resource


app=Flask(__name__)
api =Api(app)
@app.route('/')
class Helloword(Resource):
    def get(self):
        return {"data":"hellow word"}
    
    
api.add_resource(Helloword,"/helloword")





if __name__ =="__main__":
    app.run (debug=True)

