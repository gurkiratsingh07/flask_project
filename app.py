import os
import re
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from db import db


app=Flask(__name__)
uri=os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
        uri=uri.replace("postgres://","postgresql://",1)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('uri','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True


app.secret_key='qwer1234'
api=Api(app)
db.init_app(app)


@app.before_first_request
def create_table():
        db.create_all()

jwt=JWT(app,authenticate,identity)

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')

api.add_resource(UserRegister,'/register')

if __name__=='__main__':
        app.run(port=5000,debug=True)