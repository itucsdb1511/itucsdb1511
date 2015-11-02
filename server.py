import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask.helpers import url_for
import psycopg2

class City:
        def __init__(self, ID, Name):
            self.ID = ID
            self.Name = Name




class Team:
    def __init__(self,ID,Name):
        self.ID = ID
        self.Name = Name

app = Flask(__name__)
def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/teamlist')
def teamlist():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        retval = ""
        statement = """SELECT Team_ID, Team_Name FROM Team ORDER BY Team_ID"""
        cursor.execute(statement)
        teams=[]
        for Team_ID,Team_Name in cursor:
           team=(Team(Team_ID,Team_Name))
           teams.append(team)
    return render_template('teamlist.html', team_list=teams)



@app.route('/riderlist')
def riderlist():
    now = datetime.datetime.now()
    return render_template('riderlist.html', current_time=now.ctime())

@app.route('/home')
def home2():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/citylist')
def citylist():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        retval = ""
        statement = """SELECT City_ID, City_Name FROM City ORDER BY City_ID"""
        cursor.execute(statement)
        cities=[]
        for City_ID,City_Name in cursor:
           city=(City(City_ID,City_Name))
           cities.append(city)
    return render_template('citylist.html', citylist=teams)

@app.route('/citydelete/<id>')
def citydelete(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """DELETE FROM City WHERE City_ID={0}"""
        cursor.execute(statement.format(id))
        connection.commit()
    return redirect(url_for('citylist'))

@app.route('/addcity', methods=['POST', 'GET'])
def addcity():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            ID = request.form['ID']
            Name = request.form['Name']

            query = """CREATE TABLE IF NOT EXISTS City ( City_ID INT PRIMARY KEY NOT NULL, City_Name CHAR(50) NOT NULL    );"""
            cursor.execute(query)
            try:
                queryWithFormat = """INSERT INTO City (City_ID, City_Name) VALUES (%s, %s)"""
                cursor.execute(queryWithFormat, (ID, Name))
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('citylist'))
    return render_template('addcity.html')


@app.route('/playerlist')
def playerlist():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        retval = ""
        statement = """SELECT Player_ID, Player_Name FROM Player ORDER BY Player_ID"""
        cursor.execute(statement)
        for Player_ID, Player_Name in cursor:
            retval += "Player_ID = {0} and Player_Name = {1} <br>".format(Player_ID,Player_Name)
    return retval

@app.route('/playerdelete/<id>')
def playerdelete(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """DELETE FROM Player WHERE Player_ID={0}"""
        cursor.execute(statement.format(id))
        connection.commit()
    return redirect(url_for('playerlist'))

@app.route('/addplayer', methods=['POST', 'GET'])
def addplayer():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            ID = request.form['ID']
            Name = request.form['Name']

            query = """CREATE TABLE IF NOT EXISTS Player ( Player_ID INT PRIMARY KEY NOT NULL, Player_Name CHAR(50) NOT NULL    );"""
            cursor.execute(query)
            try:
                queryWithFormat = """INSERT INTO Player (Player_ID, Player_Name) VALUES (%s, %s)"""
                cursor.execute(queryWithFormat, (ID, Name))
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('playerlist'))
    return render_template('addplayer.html')

@app.route('/tournamentlist')
def tournamentlist():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        retval = ""
        statement = """SELECT Tournament_ID, Tournament_Name FROM Tournament ORDER BY Tournament_ID"""
        cursor.execute(statement)
        for Tournament_ID, Tournament_Name in cursor:
            retval += "Tournament_ID = {0} and Tournament_Name = {1} <br>".format(Tournament_ID,Tournament_Name)
    return retval

@app.route('/tournamentdelete/<id>')
def tournamentdelete(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """DELETE FROM Tournament WHERE Tournament_ID={0}"""
        cursor.execute(statement.format(id))
        connection.commit()
    return redirect(url_for('tournamentlist'))

@app.route('/addtournament', methods=['POST', 'GET'])
def addtournament():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            ID = request.form['ID']
            Name = request.form['Name']

            query = """CREATE TABLE IF NOT EXISTS Tournament ( Tournament_ID INT PRIMARY KEY NOT NULL, Tournament_Name CHAR(50) NOT NULL    );"""
            cursor.execute(query)
            try:
                queryWithFormat = """INSERT INTO Tournament (Tournament_ID, Tournament_Name) VALUES (%s, %s)"""
                cursor.execute(queryWithFormat, (ID, Name))
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('tournamentlist'))
    return render_template('addtournament.html')


@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS City (
                                City_ID INT PRIMARY KEY NOT NULL,
                                City_Name CHAR(50) NOT NULL
                    );"""
        cursor.execute(query)


        connection.commit()
    return redirect(url_for('home_page'))


@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count
@app.route('/city')
def city_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query  = "SELECT city_id FROM CITY "
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count



if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """dbname=itucsdb host=localhost port=54321 user=vagrant password=vagrant"""

    app.run(host='0.0.0.0', port=port, debug=debug)
