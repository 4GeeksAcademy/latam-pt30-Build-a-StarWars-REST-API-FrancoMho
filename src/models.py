from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

####### USER ######

class User(db.Model):
    __tablename__ = 'user'
    # PK
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    #CHILDREN | FAVORITES | ONE TO MANY
    favorites= db.relationship('Favorite', backref='user', lazy=True)
    #CHILDREN | COMMENT | ONE TO MANY
    comment = db.relationship('Comment', backref='user', lazy=True)
    #CHILDREN | POST | ONE TO MANY
    # post = db.relationship('post', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }



####### MEDIA DATABASE ######


class Character(db.Model):
    __tablename__ = 'character'
    # PK
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    age = db.Column(db.Integer)
    heigth = db.Column(db.Integer)
    eye_color = db.Column(db.String(50))
    #CHILDREN | FAVORITE | ONE TO MANY
    favorite = db.relationship('Favorite', backref='character', lazy=True)
    #CHILDREN | COMMENTS | ONE TO MANY
    comment = db.relationship('Comment', backref='character', lazy=True)

class Planet(db.Model):
    __tablename__ = 'planet'
   # PK
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(250))
    #CHILDREN | FAVORITE | ONE TO MANY
    favorites = db.relationship('Favorite', backref='planet', lazy=True)
    #CHILDREN | COMMENTS | ONE TO MANY
    comment = db.relationship('Comment', backref='planet', lazy=True)

class Starship(db.Model):
    __tablename__ = 'starship'
   # PK 
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(250))
    starship_class = db.Column(db.String(250))
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    #CHILDREN | FAVORITE | ONE TO MANY
    favorites = db.relationship('Favorite', backref='starship', lazy=True)
    #CHILDREN | FAVORITE | ONE TO MANY
    comments = db.relationship('Comment', backref='starship', lazy=True)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    # PK
    id = db.Column(db.Integer, primary_key=True)

    # FK USER.
    #user = db.relationship('user', backref='favorites', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # FK CHARACTERS.
    #character = db.relationship('characters', backref='favorites', lazy=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    # FK PLANETS.
    #planet = db.relationship('planet', backref='favorites', lazy=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    # FK STARSHIPS.
    #starship = db.relationship('starship', backref='favorites', lazy=True)
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'))


####### SOCIAL MEDIA STRUCTURE DATABASE ######


class Comment(db.Model):
    __tablename__ = 'comment'

    # PK
    id = db.Column(db.Integer, primary_key=True)
    # INFO | the comment text
    comment_text = db.Column(db.String(250))
    # FK | USER | ONE TO MANY
    #user = db.relationship('user', back_populates='comments' )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # FK | CHARACTER | ONE TO MANY
    #character = db.relationship('character', back_populates='comments' )
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    # FK | PLANET | ONE TO MANY
    #planet = db.relationship('post', back_populates='comments' )
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    # FK | STARSHIP | ONE TO MANY
    #starship = db.relationship('post', back_populates='comments' )
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'))

# class Post(db.Model):
#     __tablename__ = 'post'

#     # PK
#     id = db.Column(db.Integer, primary_key=True)
#     # INFO
#     # FK | USER | ONE TO MANY
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('user', back_populates='posts' )
#     #CHILDREN | COMMENT | ONE TO MANY
#     comment = db.relationship('comment', back_populates='post' )
#     #CHILDREN | MEDIA | ONE TO MANY
#     media = db.relationship('media', back_populates='post' )



## Draw from SQLAlchemy db.Model