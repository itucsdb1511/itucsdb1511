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

class Player:
    def __init__(self,ID,Name):
        self.ID = ID
        self.Name = Name

class Tournament:
    def __init__(self,ID,Name):
        self.ID = ID
        self.Name = Name

class Comment:
    def __init__(self,ID,Text):
        self.ID = ID
        self.Text = Text

app = Flask(__name__)


def connect_db():
    conn = psycopg2.connect(app.config['dsn'])
    cursor = conn.cursor()
    return conn, cursor

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
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


@app.route('/riderlist')
def riderlist():
    now = datetime.datetime.now()
    return render_template('riderlist.html', current_time=now.ctime())

@app.route('/home')
def home2():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


#----------------------------------------------section city------------------------------

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
    return render_template('citylist.html', citylist=cities)

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
    
    
    @app.route('/updatecity/<id>', methods=['POST', 'GET'])
def updatecity(id):
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            New_Name = request.form['Name']
            try:
                query = """UPDATE City SET City_Name='%s' WHERE City_ID='%s' """ % (New_Name, id)
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('citylist'))
    return render_template('updatecity.html', ID=id)

@app.route('/searchcity', methods=['POST', 'GET'])
def searchcity():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            textstr = request.form['textstr']
            cities = []
            try:
                query = """SELECT City_ID, City_Name FROM City WHERE City_Name like '%{0}%'"""
                cursor.execute(query.format(textstr))
                for City_ID, City_Name in cursor:
                    city = City(City_ID,City_Name)
                    cities.append(city)
                return render_template('citylist.html', citylist = cities)
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return "eeeee"
    return render_template('searchcity.html')

    """<script>
    function deleter(id) {
        window.location.href("/citydelete/id=" + id);
    }
    </script>"""

#----------------------------------------------section player------------------------------

@app.route('/playerlist')
def playerlist():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        players = []
        statement = """SELECT Player_ID, Player_Name FROM Player ORDER BY Player_ID"""
        cursor.execute(statement)
        for Player_ID, Player_Name in cursor:
            player = Player(Player_ID,Player_Name)
            players.append(player)
    return render_template('playerlist.html', Players = players)

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

#----------------------------------------------section tournament------------------------------

@app.route('/tournamentlist')
def tournamentlist():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        retval = ""
        statement = """SELECT Tournament_ID, Tournament_Name FROM Tournament ORDER BY Tournament_ID"""
        cursor.execute(statement)
        tournaments = []
        for Tournament_ID, Tournament_Name in cursor:
            tournament=(Tournament(Tournament_ID, Tournament_Name))
            tournaments.append(tournament)
    return render_template('tournamentlist.html', tournamentlist=tournaments)

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

@app.route('/updatetournament/<id>', methods=['POST', 'GET'])
def updatetournament(id):
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            New_Name = request.form['Name']
            try:
                query = """UPDATE Tournament SET Tournament_Name='%s' WHERE Tournament_ID='%s' """ % (New_Name, id)
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('tournamentlist'))
    return render_template('updatetournament.html', ID=id)
    
@app.route('/tournamentcomments/<id>')
def tournamentcomments(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        retval = ""
        statement = """SELECT Tournament_Comment_ID, Tournament_Comment_Text
                        FROM Tournament_Comments WHERE Tournament_ID=%s
                        ORDER BY Tournament_Comment_ID""" % (id)
        cursor.execute(statement)
        comments=[]
        for Tournament_Comment_ID,Tournament_Comment_Text in cursor:
           comment=(Tournament(Tournament_Comment_ID,Tournament_Comment_Text))
           comments.append(comment)
    return render_template('tournamentcomments.html', ID=id ,commentlist=comments)

@app.route('/addtournamentcomment', methods=['POST', 'GET'])
def addtournamentcomment():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            Comment_ID = request.form['Comment_ID']
            Text = request.form['Text']
            Tournament_ID = request.form['Tournament_ID']
            try:
                query = """INSERT INTO Tournament_Comments (Tournament_Comment_ID, Tournament_ID, Tournament_Comment_Text)
                    VALUES (%s, %s, %s)"""
                cursor.execute(query, (Comment_ID, Tournament_ID, Text))
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('tournamentlist'))
    return render_template('tournamentcomments.html', ID=Tournament_ID)


#----------------------------------------------section team------------------------------
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


@app.route('/addteam', methods=['POST', 'GET'])
def addteam():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            ID = request.form['ID']
            Name = request.form['Name']

            query = """CREATE TABLE IF NOT EXISTS Team ( Team_ID INT PRIMARY KEY NOT NULL, Team_Name CHAR(50) NOT NULL    );"""
            cursor.execute(query)
            try:
                queryWithFormat = """INSERT INTO Team (Team_ID, Team_Name) VALUES (%s, %s)"""
                cursor.execute(queryWithFormat, (ID, Name))
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('teamlist'))
    return render_template('addteam.html')

@app.route('/teamdelete/<id>')
def teamdelete(id):
    with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM Team WHERE Team_ID={0}"""
            cursor.execute(statement.format(id))
            connection.commit()
    return redirect(url_for('teamlist'))

@app.route('/updateteam/<id>', methods=['POST', 'GET'])
def updateteam(id):
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            New_Name = request.form['Name']

            try:
                query = """UPDATE Team SET Team_Name='%s' WHERE Team_ID='%s' """ % (New_Name, id)
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('teamlist'))
    return render_template('updateteam.html', ID=id)

@app.route('/teamcomments/<id>')
def teamcomments(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        retval = ""
        statement = """SELECT Team_Comment_ID, Team_Comment_Text
                        FROM Team_Comments WHERE Team_ID=%s
                        ORDER BY Team_Comment_ID""" % (id)
        cursor.execute(statement)
        comments=[]
        for Team_Comment_ID,Team_Comment_Text in cursor:
           comment=(Team(Team_Comment_ID,Team_Comment_Text))
           comments.append(comment)
    return render_template('teamcomments.html', ID=id ,commentlist=comments)

@app.route('/addteamcomment', methods=['POST', 'GET'])
def addteamcomment():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            Comment_ID = request.form['Comment_ID']
            Text = request.form['Text']
            Team_ID = request.form['Team_ID']
            try:
                query = """INSERT INTO Team_Comments (Team_Comment_ID, Team_ID, Team_Comment_Text)
                    VALUES (%s, %s, %s)"""
                cursor.execute(query, (Comment_ID, Team_ID, Text))
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('teamlist'))
    return render_template('teamcomments.html', ID=Team_ID)

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

        query = """CREATE TABLE IF NOT EXISTS Player (
                                Player_ID INT PRIMARY KEY NOT NULL,
                                Player_Name CHAR(50) NOT NULL
                    );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Tournament (
                                Tournament_ID INT PRIMARY KEY NOT NULL,
                                Tournament_Name CHAR(50) NOT NULL
                    );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Team (
                                Team_ID INT PRIMARY KEY NOT NULL,
                                Team_Name CHAR(50) NOT NULL
                    );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Team_Comments (
                                Team_Comment_ID INT PRIMARY KEY NOT NULL,
                                Team_ID INTEGER REFERENCES Team(Team_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                Team_Comment_Text CHAR(500) NOT NULL
                    );"""
        cursor.execute(query)
        
        query = """CREATE TABLE IF NOT EXISTS Tournament_Comments (
                                Tournament_Comment_ID INT PRIMARY KEY NOT NULL,
                                Tournament_ID INTEGER REFERENCES Tournament(Tournament_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                Tournament_Comment_Text CHAR(500) NOT NULL
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
