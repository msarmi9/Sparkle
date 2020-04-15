from app import db
from app.classes import User
from app.routes import adherence_model


def user_from_db(username):
    user = User.query.filter_by(username=username).first()
    return user


def test_user_from_db():
    # creating dummy user
    user = User(username="andy", email="cheon.andy@gmail.com", password="123")
    db.session.add(user)
    db.session.commit()
   
    # verifying dummy user in db
    assert user_from_db("andy").email == "cheon.andy@gmail.com"
    assert user_from_db("andy").username == "andy"
    assert user_from_db("andy").check_password("123") == True


def test_adherence_model():
    data = "x,y,z\n1,2,3\n4,5,6"
    model_output = adherence_model(data)
    assert model_output.get("pred_string") is not None
    assert model_output.get("pred") is not None
    assert model_output["pred_string"] == "You just took your medication!"
    assert model_output["pred"] == 3.5
