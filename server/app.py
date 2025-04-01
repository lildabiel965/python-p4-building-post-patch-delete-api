#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games', methods=['GET', 'POST'])
def games():
    if request.method == 'GET':
        games = [{
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        } for game in Game.query.all()]
        return make_response(games, 200)
    
    elif request.method == 'POST':
        data = request.json
        if not data or not all(key in data for key in ("title", "genre", "platform", "price")):
            return make_response({"message": "Invalid input."}, 400)

        new_game = Game(
            title=data.get("title"),
            genre=data.get("genre"),
            platform=data.get("platform"),
            price=data.get("price"),
        )

        try:
            db.session.add(new_game)
            db.session.commit()
            return make_response(new_game.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

@app.route('/games/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    if game is None:
        return make_response({"message": "Game not found."}, 404)

    if request.method == 'GET':
        return make_response(game.to_dict(), 200)

    elif request.method == 'PATCH':
        data = request.json
        if not data:
            return make_response({"message": "Invalid input."}, 400)

        for attr in data:
            setattr(game, attr, data.get(attr))

        try:
            db.session.commit()
            return make_response(game.to_dict(), 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

    elif request.method == 'DELETE':
        try:
            db.session.delete(game)
            db.session.commit()
            return make_response({"delete_successful": True, "message": "Game deleted."}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(reviews, 200)

    elif request.method == 'POST':
        data = request.json
        if not data or not all(key in data for key in ("score", "comment", "game_id", "user_id")):
            return make_response({"message": "Invalid input."}, 400)

        new_review = Review(
            score=data.get("score"),
            comment=data.get("comment"),
            game_id=data.get("game_id"),
            user_id=data.get("user_id"),
        )

        try:
            db.session.add(new_review)
            db.session.commit()
            return make_response(new_review.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    review = Review.query.filter(Review.id == id).first()

    if review is None:
        return make_response({"message": "Review not found."}, 404)

    if request.method == 'GET':
        return make_response(review.to_dict(), 200)

    elif request.method == 'PATCH':
        data = request.json
        if not data:
            return make_response({"message": "Invalid input."}, 400)

        for attr in data:
            setattr(review, attr, data.get(attr))

        try:
            db.session.commit()
            return make_response(review.to_dict(), 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

    elif request.method == 'DELETE':
        try:
            db.session.delete(review)
            db.session.commit()
            return make_response({"delete_successful": True, "message": "Review deleted."}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users, 200)
    
    elif request.method == 'POST':
        data = request.json
        if not data or "name" not in data:
            return make_response({"message": "Name is required."}, 400)

        new_user = User(
            name=data.get("name")
            # Add other fields as needed
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

@app.route('/users/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def user_by_id(id):
    user = User.query.filter(User.id == id).first()

    if user is None:
        return make_response({"message": "User not found."}, 404)

    if request.method == 'GET':
        return make_response(user.to_dict(), 200)

    elif request.method == 'PATCH':
        data = request.json
        if not data:
            return make_response({"message": "Invalid input."}, 400)

        for attr in data:
            setattr(user, attr, data.get(attr))

        try:
            db.session.commit()
            return make_response(user.to_dict(), 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

    elif request.method == 'DELETE':
        try:
            db.session.delete(user)
            db.session.commit()
            return make_response({"delete_successful": True, "message": "User deleted."}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": str(e)}, 500)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
