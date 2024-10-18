"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, Character, Planet, Starship, Comment
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
#db = SQLAlchemy(app)

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


##Create an API that connects to a database and implements the following endpoints (very similar to SWAPI.dev or SWAPI.tech):
#[GET] /people Get a list of all the people in the database.
@app.route('/people', methods=['GET'])
def get_all_people():
    try:
        # Query all characters from the database
        characters = Character.query.all()
        #serialize the rssults
        characters_list = [character.serialize() for character in characters]
        #return th serialized list
        return jsonify(characters_list), 200
    except Exception as error:
        print(error)
        return jsonify({"message": "Error fetching people from database"}), 500


#[GET] /people/<int:people_id> Get one single person's information.
@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    try:
        #do the query for the peopli_id
        character = Character.query.get(people_id)

        #if character is not found, return 404
        if character is None:
            return jsonify({"message": "Person not found"}), 404
        
        #serialize the result of request
        character_data = character.serialize()

        #return serialized person    
        return jsonify(character_data), 200
    except Exception as error:  
        print(error)
        return jsonify({"message": "Error fetching persona from database"}), 500


#[GET] /planets Get a list of all the planets in the database.
@app.route('/planets', methods=['GET'])
def get_all_the_planets():
    try:
        planets = Planet.query.all()

        planets_lists = [planet.serialize() for planet in planets]

        return jsonify(planets_lists), 200
    except Exception as  error:
        print(error)
        return jsonify({"message": "Error fetching planets from database"}), 500



#[GET] /planets/<int:planet_id> Get one single planet's information.
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)

        if planet in None:
            return jsonify({"message": "planet not found"}), 404
        
        planet_data =planet.serialize()

        return jsonify(planet_data), 200
    except Exception as error:
        print(error)
        return jsonify({"message": "Error fetching planet from the dstabase"}), 500

#[GET] /starships Get a list of all the starships in the database.
@app.route('/starships', methods=['GET'])
def get_all_the_starships():
    try:
        # Realiza la consulta para obtener todas las naves estelares
        starships = Starship.query.all()
        
        # Serializa los resultados de la consulta
        starships_list = [starship.serialize() for starship in starships]

        # Retorna la lista serializada de naves estelares
        return jsonify(starships_list), 200
    except Exception as error:
        print(error)
        return jsonify({"message": "Error fetching starships from the database"}), 500


#[GET] /starships/<int:planet_id> Get one single planet's information.
@app.route('/starships/<int:starship>', methods=['GET'])
def get_a_starship(starship_id):
    try:
        starship = Starship.query.get(starship_id)

        if starship in None:
            return jsonify({"message": "starship not found"}), 404
        
        starship_data =starship.serialize()

        return jsonify(starship_data), 200
    except Exception as error:
        print(error)
        return jsonify({"message": "Error fetching starship from the dstabase"})


##Additionally, create the following endpoints to allow your StarWars blog to have users and favorites:
#[POST] /users Create users. 
@app.route("/user", methods=["POST"])
def create_user():
    #Extract data from request
    data = request.json
    #Verifying we are receiving all required data in the request
    email_exists = data.get("email")
    password_exists = data.get("password")
    #Returning 400 if data is not correct  
    if None in [email_exists, password_exists]:
        return jsonify({
            "message": "Email and Password are Required"
        }), 400
    #Email Verification
    #We create new user
    new_user = User(email=email_exists, password=password_exists, is_active=True)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({}), 201


#[GET] /users Get a list of all the blog post users. [POSTS.COMMENTS]
@app.route('/users', methods=["GET"])
def get_users():
    try:
        # Realiza la consulta para obtener todas las naves estelares
        users = User.query.all()

        if not users:
            return jsonify({"message": "No users found"}), 404
        
        # Serializa los resultados de la consulta
        users_list = [user.serialize() for user in users]

        # Retorna la lista serializada de naves estelares
        return jsonify(users_list), 200
    except Exception as error:
        print(error)
        return jsonify({"message": "Error fetching users from the database"}), 500

#[GET] /users/favorites Get all the favorites that belong to the current user.
@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_users_favorites(user_id):
    try:
        # Obtén el ID del usuario actual (por ejemplo, desde un token de autenticación)

        if not user_id:
            return jsonify({"message": "User ID is missing"}), 400
        
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"message": "user has not favorites"}), 404
        
        favorites_data =[favorite.serialize() for favorite in user.favorites]

        if not favorites_data:
            return jsonify({"message": "User has no favorites"}), 404

        return jsonify(favorites_data), 200
    
    except Exception as error:
        print(error)
        return jsonify({"message": "Error fetching starship from the database"})

#[POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.
@app.route("/favorites/user/<int:user_id>/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet_to_user(planet_id, user_id):
    #Verifying we are receiving all required data in the request
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    
    #Check if the planet is already a favorite
    existing_favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"message": "Planet already a favorite"}), 400 
    
    #Add a new favorite
    new_favorite = Favorite(user_id= user_id, planet_id= planet_id)
    try:
        db.session.add(new_favorite)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({"massage": "Planet added to favorites"}), 201


#[POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.
@app.route("/favorites/user/<int:user_id>/people/<int:people_id>", methods=["POST"])
def add_favorite_character_to_user(people_id, user_id):
    
    #Verifying we are receiving all required data in the request
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    
    #Check if the people is already a favorite
    existing_favorite = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if existing_favorite:
        return jsonify({"message": "Character already a favorite"}), 400 
    
    #Add a new favorite
    new_favorite = Favorite(user_id= user_id, character_id= people_id)
    try:
        db.session.add(new_favorite)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({"massage": "Character added to favorites"}), 201

#[POST] /favorite/starship/<int:starship_id> Add new favorite starship to the current user with the starship id = starship_id.
@app.route("/favorites/user/<int:user_id>/starship/<int:starship_id>", methods=["POST"])
def add_favorite_starship_to_user(starship_id, user_id):
    #Verifying we are receiving all required data in the request
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    
    #Check if the starship is already a favorite
    existing_favorite = Favorite.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    if existing_favorite:
        return jsonify({"message": "Starship already a favorite"}), 400 
    
    #Add a new favorite
    new_favorite = Favorite(user_id= user_id, starship_id= starship_id)
    try:
        db.session.add(new_favorite)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({"massage": "Starship added to favorites"}), 201


#[DELETE] /favorite/planet/<int:planet_id> Delete a favorite planet with the id = planet_id.
@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    try:
        # Obtén el ID del usuario actual (por ejemplo, desde un token de autenticación)
        user_id = request.args.get('user_id', type=int)  # Suponiendo que el ID del usuario se pasa como parámetro

        if not user_id:
            return jsonify({"message": "User ID is required"}), 400
        
        # Busca el registro de favorito correspondiente al usuario y al planeta
        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

        if not favorite:
            return jsonify({"message": "Favorite planet not found"}), 404
        
        # Elimina el registro de favorito
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Favorite planet deleted successfully"}), 200
    except Exception as error:
        print(error)
        return jsonify({"message": "Error deleting favorite planet from the database"}), 500

#[DELETE] /favorite/people/<int:people_id> Delete a favorite people with the id = people_id.
@app.route("/favorites/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_caracter(people_id):
     try:
        # Obtén el ID del usuario actual (por ejemplo, desde un token de autenticación)
        user_id = request.args.get('user_id', type=int)  # Suponiendo que el ID del usuario se pasa como parámetro

        if not user_id:
            return jsonify({"message": "User ID is required"}), 400
        
        # Busca el registro de favorito correspondiente al usuario y al character
        favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()

        if not favorite:
            return jsonify({"message": "Favorite people not found"}), 404
        
        # Elimina el registro de favorito
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Favorite people deleted successfully"}), 200
     except Exception as error:
        print(error)
        return jsonify({"message": "Error deleting favorite planet from the database"}), 500

#[DELETE] /favorite/starship/<int:starship_id> Delete a favorite starship with the id = starship_id.
@app.route("/favorites/starship/<int:starship_id>", methods=["DELETE"])
def delete_favorite_starship(starship_id):
     try:
        # Obtén el ID del usuario actual (por ejemplo, desde un token de autenticación)
        user_id = request.args.get('user_id', type=int)  # Suponiendo que el ID del usuario se pasa como parámetro

        if not user_id:
            return jsonify({"message": "User ID is required"}), 400
        
        # Busca el registro de favorito correspondiente al usuario y al character
        favorite = Favorite.query.filter_by(user_id=user_id, starship_id=starship_id).first()

        if not favorite:
            return jsonify({"message": "Favorite starship not found"}), 404
        
        # Elimina el registro de favorito
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Favorite starship deleted successfully"}), 200
     except Exception as error:
        print(error)
        return jsonify({"message": "Error deleting favorite planet from the database"}), 500
    

###Additionally, create the following endpoints to allow users comment elements:

#[POST] /comment/planet/<int:planet_id> Add a new comment planet to the current user with the planet id = planet_id.
@app.route("/comment/planet/<int:planet_id>", methods=["POST"])
def add_comment_in_planet(planet_id):
    #Extract data from request
    user_id= request.json.get("user_id")
    comment_text = request.json.get("comment_text")

    #Verifying we are receiving all required data in the request
    if not user_id or not comment_text:
        return jsonify({"message": "User ID and comment text are required"}), 400
    
    #Add a comment
    new_comment = Comment(user_id= user_id, planet_id= planet_id, comment_text=comment_text, is_active=True)
    try:
        db.session.add(new_comment)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({"massage": "Comment added to planet"}), 201


#[POST] /comment/people/<int:people_id> Add new comment people to the current user with the people id = people_id.
@app.route("/comments/people/>int:people_id>", methods=["POST"])
def add_comment_in_character(people_id):
    #Extract data from request
    user_id= request.json.get("user_id")
    comment_text = request.json.get("comment_text")

    #Verifying we are receiving all required data in the request
    if not user_id or not comment_text:
        return jsonify({"message": "User ID and comment text are required"}), 400
    
    #Add a comment
    new_comment = Comment(user_id= user_id, people_id= people_id, comment_text=comment_text, is_active=True)
    try:
        db.session.add(new_comment)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({"massage": "Comment added to character"}), 201

#[POST] /comment/starship/<int:starship_id> Add new comment starship to the current user with the starship id = starship_id.
@app.route("/comments/starship/>int:starship_id>", methods=["POST"])
def add_comment_in_starship(starship_id):
    #Extract data from request
    user_id= request.json.get("user_id")
    comment_text = request.json.get("comment_text")

    #Verifying we are receiving all required data in the request
    if not user_id or not comment_text:
        return jsonify({"message": "User ID and comment text are required"}), 400
    
    #Add a comment
    new_comment = Comment(user_id= user_id, starship_id= starship_id, comment_text=comment_text, is_active=True)
    try:
        db.session.add(new_comment)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({"massage": "Comment added to starship"}), 201

###+4 Create also endpoints to add (POST), update (PUT), and delete (DELETE) character, planet and starship. That way all the database information can be managed using the API instead of having to rely on the Flask admin to create the planets and people.


# new_user = User(email="john.doe@example.com", password="password123", is_active=True)
# db.session.add(new_user)
# db.session.commit()


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

