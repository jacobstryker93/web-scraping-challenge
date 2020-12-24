from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


@app.route("/")
def home():
    destination_data = mongo.db.collection.find_one()
    data = scrape(browser)
    return render_template("index.html", data=data)

@app.route("/scrape")
def scrape():
     final_data = scrape_mars.scrape()
     mongo.db.collection.update({}, final_data, upsert=True)
     return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
