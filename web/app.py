from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId
import os

sample = Flask(__name__)

data = []
mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

## ---- mongoDB ----
# connect to mongo
client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]

data = mycol.find()

mycol2 = mydb["interface_status"]
data2 = mycol2.find().sort("timestamp",-1).limit(3)
@sample.route("/")
def main():
    data = mycol.find()
    return render_template("index.html", data=data)

@sample.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        info = { "ip": ip, "username": username, "password":password}
        res = mycol.insert_one(info)
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = int(request.form.get("idx"))
        col = {'_id':data[idx]['_id']}
        res = mycol.delete_one(col)
    except Exception:
        pass
    return redirect(url_for("main"))

@sample.route("/router/<ip>")
def router_detail(ip):
    router = mycol.find_one({"ip": ip})
    status_list = list(mycol2.find({"router_ip": ip}).sort("timestamp", -1).limit(3))
    print(status_list, flush=True)
    return render_template("router_detail.html", router=router, status_list=status_list)

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=5050)