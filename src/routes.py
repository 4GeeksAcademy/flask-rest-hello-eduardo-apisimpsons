from flask import Blueprint, jsonify, request
from models import User, db, Character, Location


api=Blueprint("api",__name__)

#TODOS LOS USUARIOS ✅

@api.route("/users", methods = ["GET"])
def get_users():
    users = User.query.all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200 

#OBTENER UN SOLO USUARIO ✅

@api.route("/users/<int:user_id>", methods = ["GET"])
def get_user_id(user_id):
    user = User.query.get(user_id)
    if not  user:
        return jsonify(("User not found")), 404
    return jsonify(user.serialize()), 200

#CREAR UN NUEVO USUARIO ✅

@api.route ("/users", methods = ["POST"])
def create_user():
    data = request.get_json()
    if not data.get("email") or not data.get ("password"):
        return jsonify (("error: email and password is requeried")), 400
    
    new_user = User(
        email = data["email"],
        password = data["password"]
        )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

#EDITAR UN USUARIO ✅

@api.route ("/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user: 
        user.email = data.get("email", user.email)
        user.password = data.get("password", user.password)
        db.session.commit()
        return jsonify(user.serialize()), 200
    
    return jsonify({"error":"user not found"}), 404



#FAVORITOS USUARIO ✅

@api.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user.character_like is None:
        return jsonify({"msg":"no character"}), 404

    if not user: 
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.serialize_favorite()), 200


#CREAR UN CHARACTER ✅

@api.route ("/character", methods = ["POST"])
def create_character():
    data = request.get_json()
    if not data.get("name") or not data.get ("image"):
        return jsonify (("error: name and image is requeried")), 400
    
    new_character = Character (
        name = data["name"],
        image = data["image"],
        quote= data["quote"]

    )
        
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201



# AÑADIR FAVORITOS CHARACTER ✅

@api.route("/users/<int:user_id>/character/<int:character_id>", methods=["POST"])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    if not user or not  character:
        return jsonify({"error": "User or Character not found"}), 404

    if character not in  user.character_like:
        user.character_like.append(character)
        db.session.commit()
        return jsonify({"msg":"character add"}),200
    return jsonify({"msg":"character ya agregado"}), 400

#CREAR UNA LOCATION ✅


@api.route ("/location", methods = ["POST"])
def create_location():
    data = request.get_json()
    if not data.get("name") or not data.get ("image") or not data.get ("town"):
        return jsonify (("error: name, image and town is requeried")), 400
    
    new_location = Location (
        name = data["name"],
        image = data["image"],
        town= data["town"],
        use = data["use"]

    )
        
    db.session.add(new_location)
    db.session.commit()
    return jsonify(new_location.serialize()), 201


# AÑADIR FAVORITOS LOCATION ✅

@api.route("/users/<int:user_id>/location/<int:location_id>", methods=["POST"])
def add_favorite_location(user_id,location_id):
    user = User.query.get(user_id)
    location = Location.query.get(location_id)
    if not user or not  location:
        return jsonify({"error": "User or Location not found"}), 404
    
    if location  in user.location_like:
        user.location_like.append(location)
        db.session.commit()
        

    return jsonify(user.serialize_favorite()), 201

    

      
#OBTENER TODOS LOS CHARACTERS✅

@api.route("/characters", methods = ["GET"])
def get_character():
    characters = Character.query.all()
    response = [character.serialize() for character in characters]
    return jsonify(response), 200

#OBTENER UN CHARACTER✅

@api.route("/characters/<int:character_id>", methods = ["GET"])
def get_character_id(character_id):
    character = Character.query.get(character_id)
    if not  character:
        return jsonify(("Character not found")), 404
    return jsonify(character.serialize()), 200

#OBTENER TODAS LA LOCATIONS ✅

@api.route("/locations", methods = ["GET"])
def get_location():
    locations = Location.query.all()
    response = [location.serialize() for location in locations]
    return jsonify(response), 200


#OBTENER UNA LOCATION ✅


@api.route("/locations/<int:location_id>", methods = ["GET"])
def get_location_id(location_id):
    location = Location.query.get(location_id)
    if not  location:
        return jsonify(("Location not found")), 404
    return jsonify(location.serialize()), 200

#DELETE FAVORTIES LOCATION ✅

@api.route("/users/<int:user_id>/location/<int:location_id>", methods=["DELETE"])
def delete_favorite_location(user_id,location_id):
    user = User.query.get(user_id)
    location = Location.query.get(location_id)
    if not user or not  location:
        return jsonify({"error": "User or Location not found"}), 404
    
    if location  in user.location_like:
        user.location_like.remove(location)
        db.session.commit()
        return jsonify({"msg": "Location remove to favorites"}), 201
    return jsonify({"msg": "Location no favorite"}),400

#DELETE FAVORITES CHARACTER ✅


@api.route("/users/<int:user_id>/character/<int:character_id>", methods=["DELETE"])
def delete_favorite_character(user_id,character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    if not user or not  character:
        return jsonify({"error": "User or character not found"}), 404
    
    if character  in user.character_like:
        user.character_like.remove(character)
        db.session.commit()
        return jsonify({"msg": "Character remove to favorites"}), 201
    return jsonify({"msg": "Character no favorite"}),400

#DELETE CHARACTER
@api.route("/characters/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    db.session.delete(character)  
    db.session.commit()

    return jsonify({"msg": "Character deleted successfully"}), 200  

#DELLETE LOCATION

@api.route("/location/<int:location_id>", methods=["DELETE"])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"error": "Location not found"}), 404

    db.session.delete(location)  
    db.session.commit()

    return jsonify({"msg": "Location deleted successfully"}), 200  

#DELETE USUARIOS

@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)  
    db.session.commit()

    return jsonify({"msg": "User deleted successfully"}), 200  




