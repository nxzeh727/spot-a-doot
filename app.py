from flask import Flask, render_template,jsonify, send_from_directory,redirect,url_for,request
import json
from dotenv import load_dotenv
import os
import requests
from flask_wtf import FlaskForm,CSRFProtect
from wtforms import StringField, FloatField,SubmitField
from wtforms.validators import DataRequired



load_dotenv()
FOURSQUARE_API_KEY = os.environ.get('FOURSQUARE_API_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
csrf = CSRFProtect(app)

class PlacePreferences(FlaskForm):
    lat = FloatField('latitude', validators=[DataRequired()])
    lng = FloatField('longitude', validators=[DataRequired()])
    stuff = StringField('what do you want?', validators=[DataRequired()])
    submit = SubmitField('submit')

@app.route('/spots')
def get_spots():
    with open('spots.json') as f:
        places = json.load(f)
    return jsonify(places)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/form',methods=["GET","POST"])
def form():
    form = PlacePreferences()
    if form.validate_on_submit():
        lat = form.lat.data
        lng = form.lng.data
        stuff = form.stuff.data
        return redirect(url_for('load_map', lat= lat,lng=lng,stuff=stuff))

    return render_template("form.html", form=form)

@app.route('/loadnotsavedspots')
def load_spots():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    stuff = request.args.get('stuff')
    notsavedspots = []

    url = "https://places-api.foursquare.com/places/search"
    ll = f"{lat},{lng}"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {FOURSQUARE_API_KEY}",
        "X-Places-Api-Version": "2025-06-17",
    }
    
    params={
        "query":stuff,
        "ll":ll,
        "radius": 7000,
    }

    response = requests.request("GET", url, headers=headers,params=params)

    resutls = json.loads(response.text)["results"]


    for i in resutls:
        lat = i["latitude"]
        lng = i["longitude"]
        address = i["location"]["formatted_address"]
        name = i["name"]
        notsavedspots.append({
            "name": name,
            "address": address,
            "lat":lat,
            "lng":lng
        })
    
    return notsavedspots

@app.route('/loadmap',methods=["GET","POST"])
def load_map():
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    stuff = request.args.get('stuff')
    return render_template("map.html", lat=lat, lng=lng, stuff=stuff)

if __name__ == '__main__':
    app.run(debug=True)
