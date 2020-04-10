# from app import application, db
from app.classes import User
from app.routes import adherence_model
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import os


def user_from_db(username):
    """
    Helper function to query a specific user from a database.
    """
    user = User.query.filter_by(username=username).first()
    return user


def test_user_from_db():
    """
    Test to ensure that a user's info is correctly entered into database.
    """
    assert user_from_db("andy").email == "cheon.andy@gmail.com"
    assert user_from_db("andy").username == "andy"
    assert user_from_db("andy").check_password("123") is True


def test_adherence_model():
    """
    Test to ensure that the baseline pill prediction model behaves as expected.
    """
    data = "x,y,z\n1,2,3\n4,5,6"
    model_output = adherence_model(data)
    assert model_output.get("pred_string") is not None
    assert model_output.get("pred") is not None
    assert model_output["pred_string"] == "You just took your medication!"
    assert model_output["pred"] == 3.5
