from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "61c3f76be3ec92c7ef9b556d61349485"  # OpenWeatherMap API Key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.form.get("city")
    if not city:
        return jsonify({"error": "City name is required"}), 400

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
        }
        return jsonify(weather_data)
    else:
        return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
