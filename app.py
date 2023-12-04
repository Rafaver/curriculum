from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy

config = dotenv_values('.env')
app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"  # Cambiar a un archivo físico
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo City para la tabla de ciudades
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# Modelo FavoriteCity para las ciudades favoritas
class FavoriteCity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    city = db.relationship('City', backref=db.backref('favorite', lazy=True))

def get_weather_data(city):
    API_KEY = config['API_KEY']
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=es&appid={API_KEY}'
    r = requests.get(url).json()
    return r

@app.route('/weather', methods=['POST'])
def weather():
    city = request.args.get('city')
    if city:
        weather_data = get_weather_data(city)
        if weather_data.get('cod') == 200:
            return jsonify({
                'city_name': weather_data['name'],
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'],
                'icon': weather_data['weather'][0]['icon']
            })
    return jsonify({'error': 'Ciudad no encontrada o no existente. Por favor, ingrese un nombre de ciudad válido.'}), 404

@app.route('/clima', methods=['GET', 'POST'])
def clima():
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            city_exists = City.query.filter_by(name=new_city).first()
            if not city_exists:
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()

    cities = City.query.all()
    weather_data = []

    for city in cities:
        r = get_weather_data(city.name)
        if r.get('cod') == 200:
            weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon']
            }
            weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

@app.route('/save_city', methods=['POST'])
def save_city():
    data = request.get_json()  # Si se espera un JSON en la solicitud POST
    city_name = data.get('city') if data else request.form.get('city')
    if city_name:
        city = City.query.filter_by(name=city_name).first()
        if city is None:
            new_city = City(name=city_name)
            db.session.add(new_city)
            db.session.commit()
            return jsonify({'success': True})
    return jsonify({'error': 'Error al guardar la ciudad en favoritos'}), 404

@app.route('/delete_city/<name>', methods=['GET'])
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    if city:
        db.session.delete(city)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Error al borrar la ciudad de favoritos'}), 404

if __name__ == '__main__':
    app.run(debug=True)
