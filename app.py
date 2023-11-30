from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
from dotenv import dotenv_values
from sqlalchemy import create_engine,MetaData,Table,column,String,Nullable,Integer
config = dotenv_values('.env')
metaData=MetaData

cities= Table("cities",metaData,
              column('id', Integer(),primary_key=True,autoincrement=True),
              column('id', String(100),Nullable=False,unique=True))
app = Flask(__name__)
app.template_folder = 'Templates'

saved_cities = []

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
            'icon': r['weather'][0]['icon'],
            'date_time': datetime.fromtimestamp(r['dt']).strftime('%Y-%m-%d %H:%M:%S')
        }
    return None

@app.route('/clima', methods=['GET'])
def clima_page():
    return render_template('weather.html', saved_cities=saved_cities)

def save_city(city_data):
    saved_cities.append(city_data)
    return {'success': True, 'saved_cities': saved_cities}  # Retorna la lista actualizada de ciudades guardadas

def delete_city(city):
    global saved_cities
    saved_cities = [city_data for city_data in saved_cities if city_data['city_name'] != city]

@app.route('/weather', methods=['POST'])
def weather():
    city = request.args.get('city') or request.form.get('city')
    weather_data = get_weather_data(city)
    return jsonify(weather_data)

@app.route('/save_city', methods=['POST'])
def save_city_handler():
    city = request.form.get('city')
    weather_data = get_weather_data(city)

    if weather_data:
        response = save_city(weather_data)
        return jsonify(response)
    else:
        return jsonify({'success': False, 'message': 'Error al obtener datos meteorológicos'})

@app.route('/saved_cities', methods=['GET'])
def saved_cities_page():
    return render_template('weather.html', saved_cities=saved_cities)

@app.route('/delete', methods=['POST'])
def delete():
    city = request.form['city']
    delete_city(city)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
