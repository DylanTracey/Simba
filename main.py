from math import floor

from flask import Flask
from flask import request, redirect, url_for, render_template, make_response
import os
from urllib.parse import quote
from models import db, SimbaFood
import datetime


app = Flask(__name__)
app.jinja_env.filters['quote'] = lambda u: quote(u)
app.config.from_object(os.environ['APPLICATION_CONFIGURATION'])
db.init_app(app)
with app.app_context():
    db.create_all()


def append_cookie(response, uuid):
    """
    Appends a cookie unique user identifier string onto the HTTP response.
    """
    expire_date = datetime.datetime.now() + datetime.timedelta(days=100)
    response.set_cookie('id', uuid, expires=expire_date)
    return response


def implicit_user_login(uuid, uuid_length=32):
    """
    Gets a user model object based on the unique identifier string and the user model desired.
    """
    user = SimbaFood.query.filter_by(uuid=uuid).first()
    if user is None:
        user = SimbaFood(uuid_length)
        db.session.add(user)
        db.session.commit()
    return user


@app.route('/')
def hello_world():
    uuid = request.cookies.get('id')
    user = implicit_user_login(uuid)

    food1 = request.args.get('food1') or 0
    food2 = request.args.get('food2') or 0
    food3 = request.args.get('food3') or 0

    food1calories = floor(int(food1) * user.food_1_calories / 100)
    food2calories = floor(int(food2) * user.food_2_calories / 100)
    food3calories = floor(int(food3) * user.food_3_calories / 100)

    total = food1calories + food2calories + food3calories


    response = make_response(render_template('get.html', user=user, food1=food1, food2=food2, food3=food3, total=total))


    if uuid is None:
        response = append_cookie(response, user.uuid)
    return response


if __name__ == '__main__':
    app.run()
