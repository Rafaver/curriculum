from flask import Flask, render_template, request
import requests
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
import os

config = dotenv_values('.env')

app = Flask(__name__)

# Ajusta la ubicación de las plantillas
app.template_folder = 'Templates'

def get_weather_data(city):
    API_KEY = config['API_KEY']
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=es&units=metric'
    r = requests.get(url).json()
    return r

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather_data(city)
        if weather_data['cod'] == 200:
            weather_data = {
                'city_name': city,
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'description': weather_data['weather'][0]['description'],
                'date_time': datetime.fromtimestamp(weather_data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            }
    return render_template('weather.html', weather_data=weather_data)

@app.route('/al')
def hello_al():
    get_weather_data('Guayaquil')
    return get_weather_data('Guayaquil')  

@app.route('/albert')
def hello_albert():
    return render_template("ug.html")  

@app.route('/alfred')
def hello_alfred():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
