Parts Implemented by Cem Yusuf Aydoğdu
================================


Tables
++++++++
Team Table
~~~~~~~~~~~
* Attributes of the Team Table:

   .. figure:: teamtable.png
      :scale: 75 %
      :alt:

      Team Table 

* Information about teams are located on this table.It has 4 attributes and 1 is primary key. 
* Team_ID: Keeps the id number of the team.
* Team_Name: Keeps the name of the theam.
* Team_CountryID:Keeps the Country information about the team. Foreign key.
* Team_Total_Points:Keeps the team tournament points

**SQL statement that initialize the Team Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Team (
       Team_ID SERIAL PRIMARY KEY NOT NULL,
       Team_Name CHAR(50) NOT NULL,
       Team_CountryID INT REFERENCES Country (Country_ID) ON DELETE CASCADE ON UPDATE CASCADE,
       Team_Total_Points INT DEFAULT 0)


Team Comments Table
~~~~~~~~~~~
* Attributes of the Team Comments Table:

   .. figure:: teamcommenttable.png
      :scale: 75 %
      :alt:

      Team Comment Table 

* Team comments are located on this table.It has 3 attributes and 1 is primary key. 
* Team_Comment_ID: Keeps the id number of the team comments.
* Team_ID: Foreign key. It associates team comments with the team itself. 
* Team_Comment_Text:Keeps the comment of the team.

**SQL statement that initialize the Team Comments Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Team_Comments (
      Team_Comment_ID SERIAL PRIMARY KEY NOT NULL,
      Team_ID INTEGER REFERENCES Team(Team_ID) ON DELETE CASCADE ON UPDATE CASCADE,
      Team_Comment_Text CHAR(500) NOT NULL)
      
      
Admin Table
~~~~~~~~~~~
* Attributes of the Admin Table:

   .. figure:: admintable.png
      :scale: 75 %
      :alt:

      Admin Table


* Admin are located on this table.It has 3 attributes and 1 primary key and 1 foreign key. 
* Admin_ID: Keeps the id number of the Admin.
* Admin_Username: Keeps username of the admin in char type.
* Admin_Password :Keeps password of the admin in char type.


**SQL statement that initialize the Admin Table:**

   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Admin (
         Admin_ID SERIAL PRIMARY KEY NOT NULL,
         Admin_Username CHAR(50) NOT NULL,
         Admin_Password CHAR(50) NOT NULL
                    )
                


Methods
++++++

Team Methods
~~~~~~~~~~~~~


team list

   .. code-block:: python

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
            for team in teams:
               statement = """SELECT Team_Comment_Text FROM Team_Comments WHERE Team_ID = {0}"""
               cursor.execute(statement.format(team.ID))
               for Team_Comment_Text in cursor:
                   team.Comments.append(Team_Comment_Text)
            isAdmin = session['isValid']
        return render_template('teamlist.html', Teams=teams, IsAdmin = isAdmin)



add team

   .. code-block:: python

    @app.route('/addteam', methods=['POST', 'GET'])
    def addteam():
        if request.method == 'POST':
            if session['isValid'] == False:
                return "You are not authorized"
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                Name = request.form['Name']
                CountryID = request.form['selectedValue']

                query = """CREATE TABLE IF NOT EXISTS Team (
                                    Team_ID SERIAL PRIMARY KEY NOT NULL,
                                    Team_Name CHAR(50) NOT NULL,
                                    Team_CountryID INT REFERENCES Country (Country_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                    Team_Total_Points INT DEFAULT 0
                        );"""
                cursor.execute(query)
                try:
                    queryWithFormat = """INSERT INTO Team (Team_Name, Team_CountryID) VALUES (%s, %s)"""
                    cursor.execute(queryWithFormat, (Name, CountryID))
                    connection.commit()
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "error happened"
            return redirect(url_for('teamlist'))
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            retval = ""
            statement = """SELECT Country_ID, Country_Name FROM Country ORDER BY Country_ID"""
            cursor.execute(statement)
            countries=[]
            for Country_ID,Country_Name in cursor:
               country=(Country(Country_ID, Country_Name))
               countries.append(country)
        return render_template('addteam.html', Countries = countries)


delete team

   .. code-block:: python

    @app.route('/teamdelete/<id>')
    def teamdelete(id):
        if session['isValid'] == False:
            return "You are not authorized"
        with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """DELETE FROM Team WHERE Team_ID={0}"""
                cursor.execute(statement.format(id))
                connection.commit()
        return redirect(url_for('teamlist'))



update team

   .. code-block:: python

    @app.route('/updateteam/<id>', methods=['POST', 'GET'])
    def updateteam(id):
        if session['isValid'] == False:
            return "You are not authorized"
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


add team comment

   .. code-block:: python

    def addteamcomment(id):
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                Comment = request.form['Comment']
                query = """CREATE TABLE IF NOT EXISTS Team_Comments (
                                    Team_Comment_ID SERIAL PRIMARY KEY NOT NULL,
                                    Team_ID INTEGER REFERENCES Team(Team_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                    Team_Comment_Text CHAR(500) NOT NULL
                        );"""
                cursor.execute(query)
                try:
                    query = """INSERT INTO Team_Comments (Team_ID, Team_Comment_Text)
                        VALUES (%s, %s)"""
                    cursor.execute(query, (id, Comment))
                    connection.commit()
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "error happened"
            return redirect(url_for('teamlist'))
        return render_template('addteamcomment.html', ID=id)


search team

   .. code-block:: python

    @app.route('/searchteam', methods=['POST', 'GET'])
    def searchteam():
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                textstr = request.form['textstr']
                teams = []
                try:
                    query = """SELECT Team_ID, Team_Name FROM Team WHERE Team_Name like '%{0}%'"""
                    cursor.execute(query.format(textstr))
                    for Team_ID, Team_Name in cursor:
                        team = Team(Team_ID,Team_Name)
                        teams.append(team)
                    return render_template('teamlist.html', team_list = teams)
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "error happened"
            return "eeeee"
        return render_template('searchteam.html')
