from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class Favorite(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=True)
    id_characters = db.Column(db.Integer, db.ForeignKey("characters.id"),nullable=True)
    id_planets = db.Column(db.Integer, db.ForeignKey("planets.id"),nullable=True)
    id_vehicles = db.Column(db.Integer, db.ForeignKey("vehicles.id"),nullable=True)
    user = db.relationship("User", back_populates="favorites")
    characters = db.relationship("Characters", back_populates="favorites")
    planets = db.relationship("Planets", back_populates="favorites")
    vehicles = db.relationship("Vehicles", back_populates="favorites")

    def __repr__(self):
        return f'{self.id}{self.id_user}{self.characters}{self.planets}'

    def serialize(self):
        return {
            "id_user": self.id_user,
            "user_name": self.user.name,
            "characters_name": self.characters.name,
            "planets_name": self.planets.name,

        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(70))
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    date_inscription = db.Column(db.DateTime(timezone=True), server_default=func.now())
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorite", back_populates="user")

    def __repr__(self):
        return f'{self.name} {self.last_name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    model = db.Column(db.String(50),nullable=False)
    passengers = db.Column(db.String(50),nullable=False)
    length = db.Column(db.Integer,nullable=False)
    diameter = db.Column(db.Integer,nullable=False)
    favorites = db.relationship("Favorite", back_populates="vehicles")

    def __repr__(self):
        return f'{self.name}\n{self.model}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    population = db.Column(db.Integer,nullable=False)
    rotation_period = db.Column(db.Integer,nullable=False)
    orbital_period = db.Column(db.Integer,nullable=False)
    diameter = db.Column(db.Integer,nullable=False)
    favorites = db.relationship("Favorite", back_populates="planets")

    def __repr__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,  
            "population": self.population, 
            "rotation_period": self.rotation_period, 
            "orbital_period": self.orbital_period, 
            "diameter": self.diameter, 
        }
    

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    heigth = db.Column(db.Integer,nullable=False)
    mass = db.Column(db.Integer,nullable=False)
    hair_color = db.Column(db.String(50),nullable=False)
    favorites = db.relationship("Favorite", back_populates="characters")

    def __repr__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "heigth": self.heigth,
            "hair_color": self.hair_color,
        }