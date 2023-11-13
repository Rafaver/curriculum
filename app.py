from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
import os

config = dotenv_values('.env')

app = Flask(__name__)
app.template_folder = 'Templates'

saved_cities = []  # Lista para almacenar temporalmente las ciudades guardadas

def get_weather_data(city):
    API_KEY = config['API_KEY']
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=es&units=metric'
    r = requests.get(url).json()
    if r.get('cod') == 200:
        return {
            'city_name': city,
            'temperature': r['main']['temp'],
            'humidity': r['main']['humidity'],
            'description': r['weather'][0]['description'],
            'date_time': datetime.fromtimestamp(r['dt']).strftime('%Y-%m-%d %H:%M:%S')
        }
    return None

def save_city(city_data):
    saved_cities.append(city_data)
    return {'success': True}

def delete_city(city):
    saved_cities[:] = [city_data for city_data in saved_cities if city_data['city_name'] != city]

@app.route('/')
def index():
    return render_template('weather.html', saved_cities=saved_cities)

@app.route('/weather', methods=['POST'])
def weather():
    city = request.args.get('city') or request.form.get('city')
    weather_data = get_weather_data(city)
    return jsonify(weather_data)

@app.route('/save_city', methods=['POST'])
def save_city_route():
    city_data = request.get_json()
    response = save_city(city_data)
    return jsonify(response)

@app.route('/delete', methods=['POST'])
def delete():
    city = request.form['city']
    delete_city(city)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
