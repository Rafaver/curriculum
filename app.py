from flask import Flask, render_template  
import requests
from dotenv import load_dotenv,dotenv_values

config= dotenv_values('.env')

app = Flask(__name__)
def get_weather_data(city):
    API_KEY = config ['API_KEY']
    url = f'https://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&q={city}&lang=es&units=metric'
    r = requests.get(url).json()
    print(r)
    return r


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

