from flask_sqlalchemy import SQLAlchemy
import random


db = SQLAlchemy()

BASE_UUID_LENGTH = 32
AVAILABLE_CHARACTERS = '0123456789'


def generate_uuid(digit_length):
    """
    Generates a unique user identifier string based on the number of digits and available characters above. Each
    character has equal chance of being picked per digit.
    """
    list = [random.choice(AVAILABLE_CHARACTERS) for n in range(digit_length)]
    uuid = ''.join(list)
    return uuid


class SimbaFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(BASE_UUID_LENGTH), unique=True, nullable=False)
    food_1 = db.Column(db.String(64), default='Dry Food', unique=True, nullable=False)
    food_1_calories = db.Column(db.Integer(), default=315)
    food_2 = db.Column(db.String(64), default='High Calorie Dry Food', unique=True, nullable=False)
    food_2_calories = db.Column(db.Integer(), default=352)
    food_3 = db.Column(db.String(64), default='Wet Food', unique=True, nullable=False)
    food_3_calories = db.Column(db.Integer(), default=57)

    def __init__(self, uuid_length):
        uuid = generate_uuid(uuid_length)
        while self.query.filter_by(uuid=uuid).count() >= 1:
            uuid = generate_uuid(uuid_length)
        self.uuid = uuid
