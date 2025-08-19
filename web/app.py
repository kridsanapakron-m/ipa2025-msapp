from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient

sample = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
mydb = client["ipa2025_db"]
mycol = mydb["routers"]

ttt = mycol.find()
row = []
for i in ttt:
        row.append(i['_id'])
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
        mydict = { "ip": ip, "username": username, "password": password}
        mycol.insert_one(mydict)
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = int(request.form.get("idx"))
        print(idx)
        myquery = {'_id': row[idx]}
        mycol.delete_one(myquery)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)