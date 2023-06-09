from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------USER----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_starship = db.relationship('Favorite_starship', backref='user', lazy=True) 
    favorite_planet = db.relationship('Favorite_planet', backref='user', lazy=True)
    favorite_character = db.relationship('Favorite_character', backref='user', lazy=True)
    
    def __repr__(self):
        return str(self.email)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
        }

#----------FAVORITE CHARACTER----------
class Favorite_character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Define la columna user_id como clave foránea relacionada con la tabla 'user'
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    def __repr__(self):
        return str(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

#----------FAVORITE PLANET----------
class Favorite_planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def __repr__(self):
        return str(self.user_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

#----------FAVORITE STARSHIP----------
class Favorite_starship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Define la columna user_id como clave foránea relacionada con la tabla 'user'
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'))

    def __repr__(self):
        return str(self.user_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id
        }

#----------CHARACTER----------
class Character(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    birth_year = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    mass = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)
    films = db.Column(db.String(250), nullable=False)
    species = db.Column(db.String(250), nullable=False)
    vehicles = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(250), nullable=False)
    edited = db.Column(db.String(250), nullable=False)
    favorite_character = db.relationship('Favorite_character', backref='character', lazy=True)

    def __repr__(self):
        return str(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "films": self.films,
            "species": self.species,
            "vehicles": self.vehicles,
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }

#----------PLANET----------
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    diameter = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.String(250), nullable=False)
    residents = db.Column(db.String(250), nullable=False)
    films = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(250), nullable=False)
    edited = db.Column(db.String(250), nullable=False)
    favorite_planet = db.relationship('Favorite_planet', backref='planet', lazy=True)

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "residents": self.residents,
            "films": self.films,
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }
    

#----------STARSHIP----------
class Starship(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    starship_class = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    cost_in_credits = db.Column(db.String(250), nullable=False, unique=True)
    length = db.Column(db.String(250), nullable=False)
    crew = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.String(250), nullable=False)
    max_atmosphering_speed = db.Column(db.String(250), nullable=False)
    hyperdrive_rating = db.Column(db.String(250), nullable=False)
    cargo_capacity = db.Column(db.String(250), nullable=False)
    consumables = db.Column(db.String(250), nullable=False)
    films = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(250), nullable=False)
    edited = db.Column(db.String(250), nullable=False)
    favorite_starship = db.relationship('Favorite_starship', backref='starship', lazy=True)

    def __repr__(self):
        return str(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "hyperdrive_rating": self.hyperdrive_rating,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "films": self.films,
            "created": self.created,
            "edited": self.edited,
        }
