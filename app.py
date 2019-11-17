from flask import Flask, render_template, redirect, url_for,jsonify,request, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField   
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
app = Flask(__name__)


app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'

#Connecting MovieDatabase to sqlalchemy
#using reflection of database

engine = create_engine('sqlite:///MovieNight_API_DATABASE/MovieDB.db',connect_args={'check_same_thread': False})
session = sessionmaker(bind=engine)()
Base = declarative_base()
#movies = Table('MovieTB', metadata, autoload = True, autoload_with=engine)

class Movie(Base):
    __tablename__ = "MovieTB"
    ID = Column(Integer, primary_key = True)
    TITLE = Column(String)
    GENRE = Column(String)
    DESCRIPTION = Column(String)
    POSTER = Column(String)
    RELEASE_DATE = Column(String)
    STATUS = Column(String)
    IMDB_LINK = Column(String)

    def __init__(self, ID, TITLE, DESCRIPTION, POSTER, RELEASE_DATE, STATUS, IMBD_LINK):
        self.ID= ID
        self.TITLE = TITLE
        self.GENRE = GENRE
        self.DESCRIPTION = DESCRIPTION
        self.POSTER = POSTER
        self.RELEASE_DATE = RELEASE_DATE
        self.STATUS = STATUS
        self.IMDB_LINK = IMBD_LINK


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Movie Class for Movie Table in DB
#has a Genre Relationship since
#sqlite columns do not support array values
#values are set to none while we wait for
#API Connection to past tests
class Movie(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(None)
    overview = db.Column(None)
    imbd_link = db.Column(None)
    status = db.Column(None)

    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'),
        nullable=False)
    genre = db.relationship('Genre', 
        backref=db.backref('movies', lazy=True))
    #for debugging in python environment
    def __repr__(self):
        return '<Movie %r>' % self.title

#Genre Class for Genre Table in DB
#has can assign movies to genres via movie Genre 
#relationship, so there is no need to 
#assign a value in the Movie Table, 
#we can just keep track of what movies are in a 
#particular Genre
class Genre(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(None);

    #for debugging in python environment
    def __repr__(self):
        return '<Genre %r>' % self.title


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    #for debugging in python environment
    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField ('password',validators=[InputRequired(),Length(min=8,max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route("/")
def home():
    data =[]
    result = [r.POSTER for r in session.query(Movie).all()]
    for r in result:
        data.append(r)
    return render_template("home.html", data=data)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
   
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('recommend'))

        return home()
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template("login.html",form=form)


@app.route("/signup",methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return home()
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'


    return render_template("signup.html",form=form)


@app.route("/recommend")
#@login_required
def recommend():
    my_movie_list = []
    result = [r.TITLE for r in session.query(Movie).all()]
    for r in result:
        r = r.replace(',', '')
        my_movie_list.append(r)
    list_len = len(my_movie_list)
    return render_template("recommend.html", my_movie_list = my_movie_list, list_len= list_len)
#name=current_user.username goes in return for recc commented out for editing purpose

@app.route("/process", methods = ['POST'])
def process():
    req= []
    req = request.get_json()   #gets userInputedmovies from recommend page
    movie1 = req[0]   #variable to use for query to get movie genre
    print(req)
    res = make_response(jsonify({"message": "JSON received"}),200)
    return res



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)
