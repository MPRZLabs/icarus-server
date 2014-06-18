#!/usr/bin/env python3

import weatherpy, json, datetime
from flask import Flask, Response, render_template, url_for

app = Flask(__name__)
wt = None
wta = None

def datetime_to_array(dt):
  return {
    "year": dt.year,
    "month": dt.month,
    "day": dt.day,
    "hour": dt.hour,
    "minute": dt.minute,
    "second": dt.second,
    "microsecond": dt.microsecond,
  }
def forecast_to_array(fc):
  return {
    "time": datetime_to_array(fc.date),
    "weekday": fc.day,
    "temperature": {
      "high": fc.high,
      "low": fc.low
    },
    "text": fc.text
  }
def weather_to_array(w):
  ww = {
    'location': {
      'city': w.location.city,
      'country': w.location.country,
      'region': w.location.region
    },
    'sun': {
      'set': w.astronomy.sunset,
      'rise': w.astronomy.sunrise
    },
    'humidity': w.atmosphere.humidity,
    'pressure': w.atmosphere.pressure,
    'text': w.condition.text,
    'checktime': datetime_to_array(w.condition.date),
    'temperature': w.condition.temperature,
    'wind': {
      'chill': w.wind.chill,
      'direction': w.wind.direction,
      'speed': w.wind.speed
    },
    'forecasts': [
    ]
  }
  for f in w.forecasts:
    ww['forecasts'].append(forecast_to_array(f))
  return ww

def weather_refresh():
  global wt, wta
  wt = weatherpy.Response("Icarus Phase 2 Server", 508942, metric=True)
  wta = None

def weather_object():
  global wt
  if wt is None:
    weather_refresh()
  return wt

def weather_array():
  global wta
  if wta is None:
    wta = weather_to_array(weather_object())
  return wta

@app.route('/')
def page_home():
  return Response(response=render_template("home.html",url_for=url_for,weather=weather_array()),status=200,mimetype="text/html")

@app.route('/weather')
def page_weather():
  return Response(response=render_template("weather.html",url_for=url_for,weather=weather_array()),status=200,mimetype="text/html")

@app.route('/api/weather/json')
def api_weather_json():
  return Response(response=json.dumps(weather_array(),sort_keys=True),status=200,mimetype="application/json")

@app.route('/api/weather/json_pretty')
def api_weather_json_pretty():
  return Response(response=json.dumps(weather_array(),sort_keys=True,indent=2),status=200,mimetype="application/json")

@app.route('/api/weather/refresh')
def api_weather_refresh():
  weather_refresh()
  return ""

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8088, debug=True)
