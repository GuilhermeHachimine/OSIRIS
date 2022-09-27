from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin

import json
from flask_sqlalchemy import SQLAlchemy
import os
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funnymovies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    genre = db.Column(db.String(64), nullable=False)
    director = db.Column(db.String(128), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    def toDict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'director': self.director,
            'rate': self.rate
        }
    @staticmethod
    def new(movie_dict: dict) -> 'Movie':
        movie = Movie(
            title=movie_dict['title'],
            genre=movie_dict['genre'],
            director=movie_dict['director'],
            rate=movie_dict['rate']
        )
        db.session.add(movie)
        db.session.commit()
        return movie

@app.route('/movies', methods=['GET'])
def get_movies():
    ret = []
    for movie in Movie.query.all():
        ret.append(movie.toDict())
    return jsonify(ret)

@app.route('/movies/new', methods=['POST'])
def new_movie():
    try:
        movie_dict = request.get_json()
        Movie.new(movie_dict)
        return Response(status=201)
    except KeyError:
        return Response(status=400)


@app.route('/OSIRIS/', methods=['GET'])
@cross_origin()
def GetOsiris():
    path = request.args.get('path')
    file = request.args.get('file')
    print("PATH is:")
    print(path)
    print("FILE is:")
    print(file)

    if(file):
        with open(path+'\\'+file) as f:
            fileList = f.readlines()
            dir_list2 = list(map(lambda x: os.path.join(os.path.abspath(replace_last(path,"[00]","")), x),fileList))
            return Response(json.dumps(dir_list2))
    else:
        try:
            dir_list = os.listdir(path)  
            dir_list2 = list(map(lambda x: os.path.join(os.path.abspath(path), x),os.listdir(path)))
            return Response(json.dumps(dir_list2))
        except KeyError:
            return Response(status=400)


@app.route('/OSIRIS/openFolder', methods=['GET'])
@cross_origin()
def GetOsirisFolder():
    print('INSIDE OPEN FOLDER')
    path = request.args.get('path')
    file = request.args.get('file')
    print("PATH is:")
    print(path)
    print("FILE is:")
    print(file)
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    auxPath = os.path.normpath(path)
    subprocess.run([FILEBROWSER_PATH, auxPath])
    return Response(status=200)



def replace_last(source_string, replace_what, replace_with):
    if replace_what in source_string:
        head, _sep, tail = source_string.rpartition(replace_what)
        return head + replace_with + tail
    else :
        return source_string



@app.route('/auto', methods=['GET'])
@cross_origin()
def GetAutoComplete():
    path = request.args.get('path')
    file = request.args.get('file')
    if(file):
        with open(path+'\\'+file+'.txt') as f:
            fileList = f.readlines()
            fileReturn = []
            for file in fileList:
                if file.find('.') == -1:
                    fileReturn.append(file)
            fileReturn.sort()
            return Response(json.dumps(fileReturn))
    else:
        try:
            dir_list = os.listdir(path)  
            fileReturn = []
            for file in dir_list:
                if file.find('.') == -1:
                    fileReturn.append(file)
            fileReturn.sort()
            return Response(json.dumps(fileReturn))
        except KeyError:
            return Response(status=400)


@app.route('/autoFile', methods=['GET'])
@cross_origin()
def GetAutoFileComplete():
    path = request.args.get('path')
    file = request.args.get('file')
    if(file):
        with open(path+'\\'+file+'.txt') as f:
            fileList = f.readlines()
            fileReturn = []
            for file in fileList:
                if file.find('.') == -1:
                    fileReturn.append(file)
            fileReturn.sort()
            return Response(json.dumps(fileReturn))
    else:
        try:
            dir_list = os.listdir(path)  
            fileReturn = []
            for file in dir_list:
                if file.find('.txt') != -1:
                    fileReturn.append(file)
            fileReturn.sort()
            return Response(json.dumps(fileReturn))
        except KeyError:
            return Response(status=400)
