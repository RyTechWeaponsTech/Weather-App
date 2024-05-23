from flask import Flask, render_template, request
from api import API_KEY
import requests
import os

# get gps coordinate from geopy
import json


app = Flask(__name__)

API_KEY = API_KEY
API_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&mode=json&units=metric&appid={}"

output_directory = "weather_json/"

os.makedirs(output_directory, exist_ok=True)

# function to access query api of all cities
def query_api(city):
    print(API_URL.format(city, API_KEY))
    data = requests.get(API_URL.format(city, API_KEY)).json()
    with open(f"weather_json/{city}_weather.json", "w") as json_file:
        json.dump(data, json_file)
    
    return data

@app.route("/")
def index():
    resp = query_api("Jakarta")
    print(resp)
    city = resp["name"]
    temp = resp["main"]["temp"]
    country = resp["sys"]["country"]
    weather = resp["weather"][0]["description"]
    iconcode = resp["weather"][0]["icon"]
    humidity = resp["main"]["humidity"]
    feels_like = resp["main"]["feels_like"]
    
    return render_template(
        "index.html",
        city=city,
        temp=temp,
        country=country,
        weather=weather,
        iconcode=iconcode,
        humidity=humidity,
        feels_like=feels_like,
    )
    
@app.route("/results", methods=["GET", "POST"])
def result():
    input_city = request.form.get("city")
    resp = query_api(input_city)
    error = None
    if resp:
        if len(resp) <= 2:
            error = resp["message"]
        else:
            temp = resp["main"]["temp"]
            city = resp["name"]
            country = resp["sys"]["country"]
            weather = resp["weather"][0]["description"]
            iconcode = resp["weather"][0]["icon"]
            humidity = resp["main"]["humidity"]
            feels_like = resp["main"]["feels_like"]
            return render_template(
                "index.html",
                city=city,
                temp=temp,
                country=country,
                weather=weather,
                iconcode=iconcode,
                humidity=humidity,
                feels_like=feels_like,
                )    
    return render_template("index.html", error=error)

if "__main__" == __name__:
    app.run(debug=True, port=8081)
    