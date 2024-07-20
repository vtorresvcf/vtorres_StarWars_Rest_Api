"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User,Vehicles, Planets, Characters, Favorite
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/people', methods=['GET'])
def get_people():
    characters= Characters.query.all()
    characters= [character.serialize() for character in characters]
    return jsonify({"msg":"ok to list peoples",
            "data": characters}), 200


@api.route('/people/<int:id>', methods=['GET'])
def get_peopleId(id):
    character= Characters.query.get(id)
    
    if character is None:
        error_response ={
            "msg": "People not found"
        }
        return jsonify(error_response), 404
    else:
        character= character.serialize()
        return jsonify({"msg":"ok to people",
                "data": character}), 200
    
@api.route('/planets', methods=['GET'])
def get_planets():
    planets= Planets.query.all()
    planets= [planet.serialize() for planet in planets]
   
    return jsonify({"msg":"ok to list planets",
                    "data": planets}), 200

@api.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet= Planets.query.get(id)
    if planet is None:
        error_response ={
            "msg": "Planet not found"
        }
        return jsonify(error_response), 404
    else:
        planet= planet.serialize()
    
    return jsonify({"msg":"ok to planet",
                    "data": planet}), 200
    

@api.route('/users', methods=['GET'])
def get_users():
    users= User.query.all()
    users= [user.serialize() for user in users]
   
    return jsonify({"msg":"ok",
                    "data": users}), 200

@api.route('/users/<int:id_user>/favorites', methods=['GET'])
def get_users_favorites(id_user):
    userFavorite= User.query.filter_by(id=id_user).first()
    if userFavorite is None:
        error_response = {
            "error": "User not found"
        }
        return jsonify(error_response), 404
    
    favorites = userFavorite.favorites
    user_filter_favorite= [favorite.serialize() for favorite in favorites]
    return jsonify({"msg":"ok",
                    "data": user_filter_favorite}), 200

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    user_id_data = request.json['user_id']
    favorite_planet_exist= Favorite.query.filter_by(id_user=user_id_data, id_planets=planet_id).first()
    if favorite_planet_exist:
        return jsonify({
            "msg": f'No se puede añadir, Planet ${planet_id} ya esta agregado al usuario ${user_id_data}'
        }),400
    else:
        favorite = Favorite(id_user=user_id_data, id_planets=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'msg': f'Planet {planet_id} ha sido agregado a favorito del usuario {user_id_data}'}),200

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(people_id):
    user_id_date = request.json['user_id']
    people_favorite_exist= Favorite.query.filter_by(id_user=user_id_date, id_characters=people_id).first()
    if people_favorite_exist:
        return jsonify({
            "msg": f'No se puede añadir, People {people_id} ya está agregado al usuario {user_id_date} '
        }),400
    else:
        favorite = Favorite(id_user=user_id_date, id_characters=people_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'msg': f'People {people_id} ha sido agregado a favorito del usuario {user_id_date}'}),200

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):
    user_id_date = request.json['user_id']
    people_favorite_exist= Favorite.query.filter_by(id_user=user_id_date, id_characters=people_id).first()
    if people_favorite_exist: 
        db.session.delete(people_favorite_exist)
        db.session.commit()
        return jsonify({'msg': f'People {people_id} ha sido eliminado de favorito del usuario {user_id_date}'}),200
    else:
        return jsonify({
            "msg": f'No se puede eliminar, People {people_id} no está en favorito del usuario {user_id_date} '
        }),404
    
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    user_id_date = request.json['user_id']
    planet_favorite_exist= Favorite.query.filter_by(id_user=user_id_date, id_planets=planet_id).first()
    if planet_favorite_exist: 
        db.session.delete(planet_favorite_exist)
        db.session.commit()
        return jsonify({'msg': f'Planet {planet_id} ha sido eliminado de favorito del usuario {user_id_date}'}),200
    else:
        return jsonify({
            "msg": f'No se puede eliminar, Planet {planet_id} no está en favorito del usuario {user_id_date} '
        }),404

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3245, debug=True)

