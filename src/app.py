"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Starship, Planet, Favorite_character, Favorite_planet, Favorite_starship
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


#----------USER----------
#Obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all() #obtener todos los usuarios de la base de datos
    serialized_user = [user.serialize() for user in users] #Serializar cada usuario en una lista de objetivos serializados
    return jsonify(serialized_user), 200 #Devuelve una respuesta Json con la lista de usuarios serializados

#Obtener un usuario especifico por su ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id) #Obtener el usuario por su ID
    if user is None: #Verificar si existe
        raise APIException('User not found', status_code=400)
    serialized_user = user.serialize()
    return jsonify(serialized_user), 200



#----------FAVORITE CHARACTER----------
#Obtener los personajes favoritos de un usuario especifico
@app.route('/users/<int:user_id>/favorite_characters', methods=['GET'])
def get_user_favorite_characters(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=400)
    favorite_characters = user.favorite_character #Obtener los personajes favoritos del usuario
    serialized_favorite_characters = [fav_char.serialize() for fav_char in favorite_characters]
    return jsonify(serialized_favorite_characters), 200

#Agregar un personaje favorito a un usuario especifico
@app.route('/users/<int:user_id>/favorite_characters', methods=['POST'])
def add_favorite_character(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=400)

    character_id = request.json.get('character_id') #Obtener el ID del personajes de la solicitud Json
    character = Character.query.get(character_id) #Obtener el personaje correspondiente al ID
    if character is None:
        raise APIException('Character not found', status_code=400)

    favorite_character = Favorite_character(user_id=user_id, character_id=character_id)
    db.session.add(favorite_character) # Asignar la instancia de favorite_character a la base de datos
    db.session.commit() #Confirmar lso cambios en la base de datos

    return jsonify({'message': 'Favorite character added successfully'}), 200

#Eliminar un personaje favorito de un usuario especifico
@app.route('/users/<int:user_id>/favorite_characters/<int:fav_character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, fav_character_id):
    favorite_character = Favorite_character.query.get(fav_character_id)
    if favorite_character is None:
        raise APIException('Favorite character not found', status_code=400)

    db.session.delete(favorite_character)
    db.session.commit()

    return jsonify({'message': 'Favorite character deleted successfully'}), 200



# ---------- FAVORITE PLANETS ----------
#Obtener los planetas favoritos de un usuario especifico
@app.route('/users/<int:user_id>/favorite_planets', methods=['GET'])
def get_user_favorite_planets(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=400)
    favorite_planets = user.favorite_planet
    serialized_favorite_planets = [fav_planet.serialize() for fav_planet in favorite_planets]
    return jsonify(serialized_favorite_planets), 200

#Agregar un planeta favorito a un usuario especifico
@app.route('/users/<int:user_id>/favorite_planets', methods=['POST'])
def add_favorite_planet(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=400)

    planet_id = request.json.get('planet_id')
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=400)

    favorite_planet = Favorite_planet(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite_planet)
    db.session.commit()

    return jsonify({'message': 'Favorite planet added successfully'}), 200

#Eliminar un planeta favorito de un usuario especifico
@app.route('/users/<int:user_id>/favorite_planets/<int:fav_planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, fav_planet_id):
    favorite_planet = Favorite_planet.query.get(fav_planet_id)
    if favorite_planet is None:
        raise APIException('Favorite planet not found', status_code=400)

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({'message': 'Favorite planet deleted successfully'}), 200



# ---------- FAVORITE STARSHIPS ----------
#Obtener las naves favoritas de un usuario especifico
@app.route('/users/<int:user_id>/favorite_starships', methods=['GET'])
def get_user_favorite_starships(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=400)
    favorite_starships = user.favorite_starship
    serialized_favorite_starships = [fav_starship.serialize() for fav_starship in favorite_starships]
    return jsonify(serialized_favorite_starships), 200

#Agregar una nave favorita a un usuario especifico
@app.route('/users/<int:user_id>/favorite_starships', methods=['POST'])
def add_favorite_starship(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=400)

    starship_id = request.json.get('starship_id')
    starship = Starship.query.get(starship_id)
    if starship is None:
        raise APIException('Starship not found', status_code=400)

    favorite_starship = Favorite_starship(user_id=user_id, starship_id=starship_id)
    db.session.add(favorite_starship)
    db.session.commit()

    return jsonify({'message': 'Favorite starship added successfully'}), 200

#Eliminar una nave favorita de un usuario especifico
@app.route('/users/<int:user_id>/favorite_starships/<int:fav_starship_id>', methods=['DELETE'])
def delete_favorite_starship(user_id, fav_starship_id):
    favorite_starship = Favorite_starship.query.get(fav_starship_id)
    if favorite_starship is None:
        raise APIException('Favorite starship not found', status_code=400)

    db.session.delete(favorite_starship)
    db.session.commit()

    return jsonify({'message': 'Favorite starship deleted successfully'}), 200



# ---------- CHARACTERS ----------
# Obtener todos los personajes
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()  # Consultar todos los personajes en la base de datos
    serialized_characters = [character.serialize() for character in characters]
    return jsonify(serialized_characters), 200

# Obtener un personaje específico por su ID
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        raise APIException('Character not found', status_code=400)
    serialized_character = character.serialize()
    return jsonify(serialized_character), 200

# Crear un nuevo personaje
@app.route('/characters', methods=['POST'])
def create_character():
    data = request.json # Obtener los datos del personaje del cuerpo de la solicitud en formato JSON
    character = Character( # Crear una instancia del modelo Character y asignar los valores de los campos utilizando los datos recibidos
        name=data.get('name'),
        birth_year=data.get('birth_year'),
        eye_color=data.get('eye_color'),
        gender=data.get('gender'),
        hair_color=data.get('hair_color'),
        height=data.get('height'),
        mass=data.get('mass'),
        skin_color=data.get('skin_color'),
        films=data.get('films'),
        species=data.get('species'),
        vehicles=data.get('vehicles'),
        url=data.get('url'),
        created=data.get('created'),
        edited=data.get('edited')
    )
    db.session.add(character)
    db.session.commit()
    return jsonify(character.serialize()), 200

# Actualizar un personaje existente
@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        raise APIException('Character not found', status_code=400)
    data = request.json
    character.name = data.get('name', character.name)
    character.birth_year = data.get('birth_year', character.birth_year)
    character.eye_color = data.get('eye_color', character.eye_color)
    character.gender = data.get('gender', character.gender)
    character.hair_color = data.get('hair_color', character.hair_color)
    character.height = data.get('height', character.height)
    character.mass = data.get('mass', character.mass)
    character.skin_color = data.get('skin_color', character.skin_color)
    character.films = data.get('films', character.films)
    character.species = data.get('species', character.species)
    character.vehicles = data.get('vehicles', character.vehicles)
    character.url = data.get('url', character.url)
    character.created = data.get('created', character.created)
    character.edited = data.get('edited', character.edited)
    db.session.commit()
    return jsonify(character.serialize()), 200

# Eliminar un personaje existente
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        raise APIException('Character not found', status_code=400)

    db.session.delete(character)
    db.session.commit()

    return jsonify({'message': 'Character deleted successfully'}), 200



# ---------- PLANETS ----------
# Obtener todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets), 200

# Obtener un planeta específico por su ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=400)
    serialized_planet = planet.serialize()
    return jsonify(serialized_planet), 200

# Crear un nuevo planeta
@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    planet = Planet(
        name=data.get('name'),
        diameter=data.get('diameter'),
        rotation_period=data.get('rotation_period'),
        orbital_period=data.get('orbital_period'),
        gravity=data.get('gravity'),
        population=data.get('population'),
        climate=data.get('climate'),
        terrain=data.get('terrain'),
        surface_water=data.get('surface_water'),
        residents=data.get('residents'),
        films=data.get('films'),
        url=data.get('url'),
        created=data.get('created'),
        edited=data.get('edited')
    )
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 200

# Actualizar un planeta existente
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=400)
    data = request.json
    planet.name = data.get('name', planet.name)
    planet.diameter = data.get('diameter', planet.diameter)
    planet.rotation_period = data.get('rotation_period', planet.rotation_period)
    planet.orbital_period = data.get('orbital_period', planet.orbital_period)
    planet.gravity = data.get('gravity', planet.gravity)
    planet.population = data.get('population', planet.population)
    planet.climate = data.get('climate', planet.climate)
    planet.terrain = data.get('terrain', planet.terrain)
    planet.surface_water = data.get('surface_water', planet.surface_water)
    planet.residents = data.get('residents', planet.residents)
    planet.films = data.get('films', planet.films)
    planet.url = data.get('url', planet.url)
    planet.created = data.get('created', planet.created)
    planet.edited = data.get('edited', planet.edited)
    db.session.commit()
    return jsonify(planet.serialize()), 200

# Eliminar un planeta existente
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=400)

    db.session.delete(planet)
    db.session.commit()

    return jsonify({'message': 'Planet deleted successfully'}), 200



# ---------- STARSHIPS ----------
# Obtener todas las naves
@app.route('/starships', methods=['GET'])
def get_all_starships():
    starships = Starship.query.all()
    serialized_starships = [starship.serialize() for starship in starships]
    return jsonify(serialized_starships), 200

# Obtener una nave específico por su ID
@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        raise APIException('Starship not found', status_code=400)
    serialized_starship = starship.serialize()
    return jsonify(serialized_starship), 200

# Crear una nueva nave
@app.route('/starships', methods=['POST'])
def create_starship():
    data = request.json
    starship = Starship(
        name=data.get('name'),
        model=data.get('model'),
        starship_class=data.get('starship_class'),
        manufacturer=data.get('manufacturer'),
        cost_in_credits=data.get('cost_in_credits'),
        length=data.get('length'),
        crew=data.get('crew'),
        passengers=data.get('passengers'),
        max_atmosphering_speed=data.get('max_atmosphering_speed'),
        hyperdrive_rating=data.get('hyperdrive_rating'),
        cargo_capacity=data.get('cargo_capacity'),
        consumables=data.get('consumables'),
        films=data.get('films'),
        created=data.get('created'),
        edited=data.get('edited')
    )
    db.session.add(starship)
    db.session.commit()
    return jsonify(starship.serialize()), 200

# Actualizar una nave existente
@app.route('/starships/<int:starship_id>', methods=['PUT'])
def update_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        raise APIException('Starship not found', status_code=400)
    data = request.json
    starship.name = data.get('name', starship.name)
    starship.model = data.get('model', starship.model)
    starship.starship_class = data.get('starship_class', starship.starship_class)
    starship.manufacturer = data.get('manufacturer', starship.manufacturer)
    starship.cost_in_credits = data.get('cost_in_credits', starship.cost_in_credits)
    starship.length = data.get('length', starship.length)
    starship.crew = data.get('crew', starship.crew)
    starship.passengers = data.get('passengers', starship.passengers)
    starship.max_atmosphering_speed = data.get('max_atmosphering_speed', starship.max_atmosphering_speed)
    starship.hyperdrive_rating = data.get('hyperdrive_rating', starship.hyperdrive_rating)
    starship.cargo_capacity = data.get('cargo_capacity', starship.cargo_capacity)
    starship.consumables = data.get('consumables', starship.consumables)
    starship.films = data.get('films', starship.films)
    starship.created = data.get('created', starship.created)
    starship.edited = data.get('edited', starship.edited)
    db.session.commit()
    return jsonify(starship.serialize()), 200

# Eliminar una nave existente
@app.route('/starships/<int:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        raise APIException('Starship not found', status_code=400)

    db.session.delete(starship)
    db.session.commit()

    return jsonify({'message': 'Starship deleted successfully'}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
