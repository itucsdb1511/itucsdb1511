Parts Implemented by İsmail Serhat Buğa
=======================================


Tables
++++++
Player Table
++++++++++++
* Attributes of the Player Table:

   .. figure:: playertable.png
      :scale: 75 %
      :alt:

      Player Table

* Team players are located on this table.It has 3 attributes and 1 primary key and 1 foreign key.
* Player_ID: Keeps the id number of the player.
* Player_Name: Keeps name of the playerin char type.
* Player_TeamID: Foreign key. It associates team with the player.

**SQL statement that initialize the Player Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Player (
       Player_ID SERIAL PRIMARY KEY NOT NULL,
       Player_Name CHAR(50) NOT NULL,
       Player_TeamID INT REFERENCES Team (Team_ID) ON DELETE CASCADE ON UPDATE CASCADE
                    )




Player Comments Table
+++++++++++++++++++++
* Attributes of the Player Comment Table:

   .. figure:: playercommenttable.png
      :scale: 75 %
      :alt:

      Player Comment Table

* Player comments are located on this table.It has 3 attributes and 1 is primary key.
* Player_Comment_ID: Keeps the id number of the player comments.
* Player_ID: Foreign key. It associates team comments with the player itself.
* Player_Comment_Text:Keeps the comment of the player.

**SQL statement that initialize the Player Comments Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Player_Comments (
        Player_Comment_ID SERIAL PRIMARY KEY NOT NULL,
        Player_ID INTEGER REFERENCES Player(Player_ID) ON DELETE CASCADE ON UPDATE CASCADE,
        PLayer_Comment_Text CHAR(500) NOT NULL)

Methods
+++++++


Player Methods
~~~~~~~~~~~~~~

* Player List
This method list the all of the players in the database. Also in this method player comment for each player are listed too.
Player ID, Player Name and Player Comments listed using the 2 statements.
.. code-block:: python


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
        for player in players:
            statement = """SELECT Player_Comment_Text FROM Player_Comments WHERE Player_ID = {0}"""
            cursor.execute(statement.format(player.ID))
            for Player_Comment_Text in cursor:
                player.Comments.append(Player_Comment_Text)
        isAdmin = session['isValid']
    return render_template('playerlist.html', Players = players, IsAdmin = isAdmin)

* Player Delete
This method deletes the selected player from the *Player* table. Query is *DELETE FROM Player WHERE Player_ID={0}"""*.
Also this methods control the session. If the session value is false then this operations can not be completed.
.. code-block:: python

@app.route('/playerdelete/<id>')
def playerdelete(id):
    if session['isValid'] == False:
        return "You are not authorized"
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """DELETE FROM Player WHERE Player_ID={0}"""
        cursor.execute(statement.format(id))
        connection.commit()
    return redirect(url_for('playerlist'))

* Player Add
This methods adds a new player to the *Player* table. Query is *"""INSERT INTO Player (Player_Name, Player_TeamID) VALUES (%s, %s)"""*.
Also user must select the Team name for the Foreign key. Player_TeamID associates Team table with the Player table.
Query is *"""SELECT Team_ID, Team_Name FROM Team ORDER BY Team_ID"""*
Also this methods control the session. If the session value is false then this operations can not be completed.

.. code-block:: python

@app.route('/addplayer', methods=['POST', 'GET'])
def addplayer():
    if session['isValid'] == False:
        return "You are not authorized"
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            Name = request.form['Name']
            TeamID = request.form['selectedValue']

            query = """CREATE TABLE IF NOT EXISTS Player ( Player_ID SERIAL PRIMARY KEY NOT NULL, Player_Name CHAR(50) NOT NULL, Player_TeamID INT REFERENCES Team (Team_ID) );"""
            cursor.execute(query)
            try:
                queryWithFormat = """INSERT INTO Player (Player_Name, Player_TeamID) VALUES (%s, %s)"""
                cursor.execute(queryWithFormat, (Name, TeamID))
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('playerlist'))
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        retval = ""
        statement = """SELECT Team_ID, Team_Name FROM Team ORDER BY Team_ID"""
        cursor.execute(statement)
        teams=[]
        for Team_ID,Team_Name in cursor:
           team=(Team(Team_ID,Team_Name))
           teams.append(team)
    return render_template('addplayer.html', Teams = teams)



* Add Player Comment
This method adds new comment for the *Player_Comments* table . Query is *"""INSERT INTO Player_Comments (Player_ID, PLayer_Comment_Text) VALUES (%s,%s)"""*
Comments text taken from the user.
.. code-block:: python

@app.route('/addplayercomment/<id>', methods=['POST', 'GET'])
def addplayercomment(id):
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            Comment = request.form['Comment']

            query = """CREATE TABLE IF NOT EXISTS Player_Comments (
                                Player_Comment_ID SERIAL PRIMARY KEY NOT NULL,
                                Player_ID INTEGER REFERENCES Player(Player_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                PLayer_Comment_Text CHAR(500) NOT NULL
                    );"""
            cursor.execute(query)


            try:
                queryWithFormat = """INSERT INTO Player_Comments (Player_ID, PLayer_Comment_Text) VALUES (%s,%s)"""
                cursor.execute(queryWithFormat, (id, Comment))
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('playerlist'))
    return render_template('addplayercomment.html', ID=id)

* Update Player
This method updates City name on the *City* table.
Query is *"""UPDATE Player SET Player_Name='%s' WHERE Player_ID='%s' """*
.. code-block:: python

@app.route('/updateplayer/<id>', methods=['POST', 'GET'])
def updateplayer(id):
    if session['isValid'] == False:
        return "You are not authorized"
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            New_Name = request.form['Name']
            try:
                query = """UPDATE Player SET Player_Name='%s' WHERE Player_ID='%s' """ % (New_Name, id)
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return redirect(url_for('playerlist'))
    return render_template('updateplayer.html', ID=id)


* Search Player
This method searchs a Player object in database by the Player name.
Query is *"""SELECT Player_ID, Player_Name FROM Player WHERE Player_Name like '%{0}%'"""*
And returns the matched player(s) if exists.

.. code-block:: python

@app.route('/searchplayer', methods=['POST', 'GET'])
def searchplayer():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            textstr = request.form['textstr']
            players = []
            try:
                query = """SELECT Player_ID, Player_Name FROM Player WHERE Player_Name like '%{0}%'"""
                cursor.execute(query.format(textstr))
                for Player_ID, Player_Name in cursor:
                    player = Player(Player_ID,Player_Name)
                    players.append(player)
                return render_template('playerlist.html', Players = players)
            except dbapi2.DatabaseError:
                connection.rollback()
                return "error happened"
        return "eeeee"
    return render_template('searchplayer.html')



