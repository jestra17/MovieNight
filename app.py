from flask import Flask, render_template, redirect, url_for,jsonify,request, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField   
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask import session
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import current_user
import logging
import random
app = Flask(__name__)

url = ""

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False 
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MovieNight_API_DATABASE/MovieDB.db'

#Connecting MovieDatabase to sqlalchemy
#using reflection of database

#engine = create_engine('sqlite:///MovieNight_API_DATABASE/MovieDB.db',connect_args={'check_same_thread': False})
#DBsession = sessionmaker(bind=engine)()
#Base = declarative_base()
#movies = Table('MovieTB', metadata, autoload = True, autoload_with=engine)'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UserWatched_table = db.Table('UserWatched', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('MovieTB_ID', db.Integer, db.ForeignKey('MovieTB.ID'))
)
UserWantsToWatch_table = db.Table('UserWantsToWatch', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('MovieTB_ID', db.Integer, db.ForeignKey('MovieTB.ID'))
)

class Movie(db.Model):
    __tablename__ = "MovieTB"
    ID = db.Column(Integer, primary_key = True)
    TITLE = db.Column(String)
    GENRE = db.Column(String)
    DESCRIPTION = db.Column(String)
    POSTER = db.Column(String)
    RELEASE_DATE = db.Column(String)
    STATUS = db.Column(String)
    IMDB_LINK = db.Column(String)

    def __init__(self, ID, TITLE, DESCRIPTION, POSTER, RELEASE_DATE, STATUS, IMBD_LINK):
        self.ID= ID
        self.TITLE = TITLE
        self.GENRE = GENRE
        self.DESCRIPTION = DESCRIPTION
        self.POSTER = POSTER
        self.RELEASE_DATE = RELEASE_DATE
        self.STATUS = STATUS
        self.IMDB_LINK = IMBD_LINK


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    moviesWatched = db.relationship("Movie",
                               secondary=UserWatched_table)
    moviesWantToWatch = db.relationship("Movie",
                               secondary=UserWantsToWatch_table)

db.create_all()

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



##### Babak's working on it

@app.route("/movie/<movieId>",methods=['GET'])
def  movie(movieId):
    all_movie_elements = query = session.query(Movie).order_by(Movie.ID)


    return render_template("movie.html", data = all_movie_elements)





    

@app.route("/")
def home():
    data =[]
    result = [r.POSTER for r in Movie.query.all()]

    myPosterUrls = []
    img_url = [r.POSTER for r in Movie.query.all()]
    img_id = [r.ID for r in Movie.query.all()]
    data = [(id, url) for url,id in zip(img_url, img_id)]
    
    if current_user.is_authenticated:
         return render_template("userHome.html",myPosterUrls = img_url, img_id = img_id)
    else:
         return render_template("home.html",data=data,img_id = img_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
   
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('recommend'))

        return '<h1>Invalid username or password</h1>'
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

        return redirect(url_for('login'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'


    return render_template("signup.html",form=form)


@app.route("/recommend")
#@login_required
def recommend():
    my_movie_list = []
    result = [r.TITLE for r in Movie.query.all()]
    for r in result:
        r = r.replace(',', '')
        my_movie_list.append(r)
    list_len = len(my_movie_list)


    return render_template("recommend.html", my_movie_list = my_movie_list, list_len= list_len)
#name=current_user.username goes in return for recc commented out for editing purpose



@app.route("/process", methods = ['POST'])
def process():
    req= []
    genreList = []
    recMovieList= []
    newGenreList =[]
    randomMovies= []
    
    req = request.get_json()   #gets userInputedmovies from recommend page
    print(req)
    for i,val in enumerate(req):
        for instance in Movie.query.filter_by(TITLE = val):
            genreList.append(instance.GENRE)
    print(genreList)
    
    #iterate over genreList
    for i, val in enumerate(genreList): #iterate over genreList pulling out each value
         tempList = val.split(",")     # separate each string with commas into separate items ("cat, dog" ->"cat","dog" )
         for i, val in enumerate(tempList): # pull each value of newly separated list
            newGenreList.append(val)        #append to new genreList 
    newGenreList= list(set(newGenreList))  #remove duplicates from newGenrelist
    print(newGenreList)

  
    #iterate over newGenreList to get movie posters for movies with listed genres 
    for i, val in enumerate(newGenreList):
        print(val)
        for instance in Movie.query.filter(Movie.GENRE.contains(val)):
            recMovieList.append(instance.POSTER)
    
    print(recMovieList)
    recMovieList = list(set(recMovieList))
    randomMovies = random.sample(recMovieList, 51)
    session['movie_list'] = randomMovies
    res = make_response(jsonify(recMovieList,200))
    return res



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)