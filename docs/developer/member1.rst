Parts Implemented by Member Name
================================

Tables
-------

City Table
~~~~~~~~~~
* Attributes of the City Table:

   .. figure:: citytable.png
      :scale: 75 %
      :alt:

      City Table

* Tournament cities are located on this table.It has 3 attributes and 1 primary key and 1 foreign key.
* *City_ID*: Keeps the id number of the city.
* *City_Name*: Keeps name of the city in char type.
* *City_CountryID*: Foreign key. It associates country with the city.

**SQL statement that initialize the City Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS City (
       City_ID SERIAL PRIMARY KEY NOT NULL,
       City_Name CHAR(50) NOT NULL,
       City_CountryID INT REFERENCES Country (Country_ID) ON DELETE CASCADE ON UPDATE CASCADE)

* Foreign key of the City table has references Country table (*Country_ID*) on *Delete Cascade and Update Cascade*.


City Comment Table
~~~~~~~~~~
* Attributes of the City Comment Table:

   .. figure:: citycommenttable.png
      :scale: 75 %
      :alt:

      City Comment Table

* City comments are located on this table.It has 3 attributes and 1 primary key and 1 foreign key.
* *City_CommentID*: Keeps the id number of the City Comment.
* *City_ID*: Foreign key. It associates city comments with the city.
* *City_Comment_Text*: Keeps the comment of the city.

**SQL statement that initialize the City Comments Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS City_Comments (
       City_Comment_ID SERIAL PRIMARY KEY NOT NULL,
       City_ID INTEGER REFERENCES City(City_ID) ON DELETE CASCADE ON UPDATE CASCADE,
       City_Comment_Text CHAR(500) NOT NULL)

* Foreign key of the City Comments table has references City table (*City_ID*) on *Delete Cascade and Update Cascade*.

Country Table
~~~~~~~~~~
* Attributes of the Country Table:

   .. figure:: countrytable.png
      :scale: 75 %
      :alt:

      Country Table

* Tournament city countries are located on this table.It has 2 attributes and 1 primary key and Country_Name.
* *Country_ID*: Keeps the id number of the country.
* *Country_Name*: Keeps name of the country in char type.

**SQL statement that initialize the Country Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Country (
        Country_ID SERIAL PRIMARY KEY NOT NULL,
        Country_Name CHAR(50) NOT NULL)

Accommodation Table
~~~~~~~~~~
* Attributes of the Accommodation Table:

   .. figure:: accommodationtable.png
      :scale: 75 %
      :alt:

      Accommodation Table


* Tournament accommodations are located on this table.It has 3 attributes and 1 primary key and 1 foreign key.
* *Accommodation_ID*: Keeps the id number of the accommodation .
* *Accommodation_Name*: Keeps name of the hotel in char type.
* *Accommodation_CityID*: Foreign key. It associates city with the hotel.


**SQL statement that initialize the Accommodation Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Accommodation (
       Accommodation_ID SERIAL PRIMARY KEY NOT NULL,
       Accommodation_Name CHAR(50) NOT NULL,
       Accommodation_CityID INT REFERENCES City (City_ID) ON DELETE CASCADE ON UPDATE CASCADE)

* Foreign key of the Accommodation table has references City table (*City_ID*) on *Delete Cascade and Update Cascade*.

Accommodation Comment Table
~~~~~~~~~~
* Attributes of the Accommodation Comment Table:

   .. figure:: accommodationcommenttable.png
      :scale: 75 %
      :alt:

      Accommodation Comments Table

* Tournament accommodations comments are located on this table.It has 3 attributes and 1 is primary key.
* *Accommodation_Comment_ID*:Keepstheidnumberoftheaccommodation comments.
* *Accommodation_ID*: Foreign key. It associates city comments with the city.
* *Accommodation_Comment_Text*:Keeps the comment of the hotel.


**SQL statement that initialize the Accommodation Comments Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Accommodation_Comments (
       Accommodation_Comment_ID SERIAL PRIMARY KEY NOT NULL,
       Accommodation_ID INTEGER REFERENCES Accommodation(Accommodation_ID) ON DELETE CASCADE ON UPDATE CASCADE,
       Accommodation_Comment_Text CHAR(500) NOT NULL)

* Foreign key of the Accommodation Comments table has references Accommodation table (*Accommodation_ID*) on *Delete Cascade and Update Cascade*.

Methods
++++++++

City Methods
~~~~~~~~~~~~~

* City List
This method list the all of the cities in the database. Also in this method city comment from City Comment table are listed too.
City ID, City Name and City Comments listed using the 2 statements.
   .. code-block:: python

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
               print(City_ID)
            for city in cities:
                statement = """SELECT City_Comment_Text FROM City_Comments WHERE City_ID = {0}"""
                cursor.execute(statement.format(city.ID))
                for City_Comment_Text in cursor:
                    city.Comments.append(City_Comment_Text)
            isAdmin = session['isValid']
        return render_template('citylist.html', citylist = cities, IsAdmin = isAdmin)


* City Delete
This method deletes cities from the *City* table. Query is *DELETE FROM City WHERE City_ID={0}"""*.
This method delete the cities according to id number of the *City*.
Also this methods control the session. If the session value is false then this operations can not be completed.
   .. code-block:: python

    @app.route('/citydelete/<id>')
    def citydelete(id):
        if session['isValid'] == False:
            return "You are not authorized"
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM City WHERE City_ID={0}"""
            cursor.execute(statement.format(id))
            connection.commit()
        return redirect(url_for('citylist'))


* City Add
This methods add new city to the *City* table. Query is *"""INSERT INTO City (City_Name, City_CountryID) VALUES (%s, %s)"""*.
Also user must select the Country name for the Foreign key. City_CountryID associates Country table with the City table.
Query is *"""SELECT Country_ID, Country_Name FROM Country ORDER BY Country_ID"""*
Also this methods control the session. If the session value is false then this operations can not be completed.

   .. code-block:: python

    @app.route('/addcity', methods=['POST', 'GET'])
    def addcity():
        if session['isValid'] == False:
            return "You are not authorized"
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                Name = request.form['Name']
                CountryID = request.form['selectedValue']


                query = """CREATE TABLE IF NOT EXISTS City ( City_ID SERIAL PRIMARY KEY NOT NULL, City_Name CHAR(50) NOT NULL, City_CountryID INT REFERENCES Country (Country_ID) ON DELETE CASCADE ON UPDATE CASCADE    );"""
                cursor.execute(query)
                try:
                    queryWithFormat = """INSERT INTO City (City_Name, City_CountryID) VALUES (%s, %s)"""
                    cursor.execute(queryWithFormat, (Name, CountryID))
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "error happened"
            return redirect(url_for('citylist'))
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            retval = ""
            statement = """SELECT Country_ID, Country_Name FROM Country ORDER BY Country_ID"""
            cursor.execute(statement)
            countries=[]
            for Country_ID,Country_Name in cursor:
               country=(Country(Country_ID,Country_Name))
               countries.append(country)
        return render_template('addcity.html', Countries = countries)


* Add City Comment
This method adds new comment for the *City_Comments* table . Query is *"""INSERT INTO City_Comments (City_ID, City_Comment_Text) VALUES (%s,%s)"""*
Comments text taken from the user.
   .. code-block:: python

    @app.route('/addcitycomment/<id>', methods=['POST', 'GET'])
    def addcitycomment(id):
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                Comment = request.form['Comment']

                query = """CREATE TABLE IF NOT EXISTS City_Comments (
                                    City_Comment_ID SERIAL PRIMARY KEY NOT NULL,
                                    City_ID INTEGER REFERENCES City(City_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                    City_Comment_Text CHAR(500) NOT NULL
                        );"""
                cursor.execute(query)


                try:
                    queryWithFormat = """INSERT INTO City_Comments (City_ID, City_Comment_Text) VALUES (%s,%s)"""
                    cursor.execute(queryWithFormat, (id, Comment))
                    connection.commit()
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "error happened"
            return redirect(url_for('citylist'))
        return render_template('addcitycomment.html', ID=id)

* Update City
This method updates City name on the *City* table.
Query is *"""UPDATE City SET City_Name='%s' WHERE City_ID='%s' """*


   .. code-block:: python

    @app.route('/updatecity/<id>', methods=['POST', 'GET'])
    def updatecity(id):
        if session['isValid'] == False:
            return "You are not authorized"
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

* Search City
This method searchs an City object in database by the City name.
Query is *"""SELECT City_ID, City_Name FROM City WHERE City_Name like '%{0}%'"""*
And return the matched city.

   .. code-block:: python

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


Country Methods
~~~~~~~~~~~~~

* Country Add
This methods add new country to the *Country* table. Query is *"""INSERT INTO Country (Country_Name) VALUES ( '{0}' )"""*.
Also this methods control the session. If the session value is false then this operations can not be completed.

   .. code-block:: python

    @app.route('/addcountry', methods=['POST', 'GET'])
    def addcountry():
       if session['isValid'] == False:
          return "You are not authorized"
       if request.method == 'POST':
          with dbapi2.connect(app.config['dsn']) as connection:
              cursor = connection.cursor()

              Name = request.form['Name']

              query = """CREATE TABLE IF NOT EXISTS Country ( Country_ID SERIAL PRIMARY KEY NOT NULL, Country_Name CHAR(50) NOT NULL    );"""
              cursor.execute(query)

              queryWithFormat = """INSERT INTO Country (Country_Name) VALUES ( '{0}' )"""
              cursor.execute(queryWithFormat.format(Name))

          return redirect(url_for('countrylist'))
       return render_template('addcountry.html')

* Country Delete
This method deletes countries from the *Country* table. Query is *DELETE FROM Country WHERE Country_ID={0}"""*.
This method delete the cities according to id number of the *Country*.
Also this methods control the session. If the session value is false then this operations can not be completed.
    
   .. code-block:: python

    @app.route('/countrydelete/<id>')
    def countrydelete(id):
        if session['isValid'] == False:
            return "You are not authorized"
            with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()
               statement = """DELETE FROM Country WHERE Country_ID={0}"""
               cursor.execute(statement.format(id))
               connection.commit()
            return redirect(url_for('countrylist'))

* Country Search
This method searchs an Country object in database by the Country name.
Query is *"""SELECT Country_ID, Country_Name FROM Country WHERE Country_Name like '%{0}%'"""*
And return the matched Country.

   .. code-block:: python

    @app.route('/searchcountry', methods=['POST', 'GET'])
    def searchcountry():
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                textstr = request.form['textstr']
                cities = []
                try:
                    query = """SELECT Country_ID, Country_Name FROM Country WHERE Country_Name like '%{0}%'"""
                    cursor.execute(query.format(textstr))
                    for Country_ID, Country_Name in cursor:
                        country = Country(Country_ID,Country_Name)
                        countries.append(country)
                    return render_template('countrylist.html', countrylist = countries)
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "Something"
            return "Hata"
        return render_template('searchcountry.html')


* Country Update
This method updates Country name on the *Country* table.
Query is *"""UPDATE Country SET Country_Name='%s' WHERE Country_ID='%s' """*


   .. code-block:: python

    @app.route('/updatecountry/<id>', methods=['POST', 'GET'])
    def updatecountry(id):
        if session['isValid'] == False:
            return "You are not authorized"
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                New_Name = request.form['Name']
                try:
                    query = """UPDATE Country SET Country_Name='%s' WHERE Country_ID='%s' """ % (New_Name, id)
                    cursor.execute(query)
                    connection.commit()
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "error happened"
            return redirect(url_for('countrylist'))
        return render_template('updatecountry.html', ID=id)

Accommodation Methods
~~~~~~~~~~~~~

* Accommodation Delete
This method deletes hotels from the *Accommodation* table. Query is *"""DELETE FROM Accommodation WHERE Accommodation_ID={0}"""*.
This method delete the hotels according to id number of the *Accommodation*.
Also this methods control the session. If the session value is false then this operations can not be completed.
   .. code-block:: python

    @app.route('/accommodationdelete/<id>')
    def accommodationdelete(id):
        if session['isValid'] == False:
            return "You are not authorized"
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM Accommodation WHERE Accommodation_ID={0}"""
            cursor.execute(statement.format(id))
            connection.commit()
        return redirect(url_for('accommodationlist'))


* Accommodation Add
This methods add new hotel to the *Accommodation* table. Query is *"""INSERT INTO Accommodation (Accommodation_Name, Accommodation_CityID) VALUES (%s, %s)"""*.
Also user must select the City name for the Foreign key. Accommodation_CityID associates City table with the Accommodation table.
Query is *"""SELECT City_ID, City_Name FROM City ORDER BY City_ID"""*
Also this methods control the session. If the session value is false then this operations can not be completed.

   .. code-block:: python

    @app.route('/addaccommodation', methods=['POST', 'GET'])
    def addaccommodation():
        if session['isValid'] == False:
            return "You are not authorized"
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                Name = request.form['Name']
                CityID = request.form['selectedValue']


                query = """CREATE TABLE IF NOT EXISTS Accommodation ( Accommodation_ID SERIAL PRIMARY KEY NOT NULL, Accommodation_Name CHAR(75) NOT NULL, Accommodation_CityID INT REFERENCES City (City_ID) ON DELETE CASCADE ON UPDATE CASCADE    );"""
                cursor.execute(query)
                try:
                    queryWithFormat = """INSERT INTO Accommodation (Accommodation_Name, Accommodation_CityID) VALUES (%s, %s)"""
                    cursor.execute(queryWithFormat, (Name, AccommodationID))
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "Somethin wrong"
            return redirect(url_for('accommodationlist'))
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            retval = ""
            statement = """SELECT City_ID, City_Name FROM City ORDER BY City_ID"""
            cursor.execute(statement)
            cities=[]
            for City_ID,City_Name in cursor:
               city=(City(City_ID,City_Name))
               cities.append(city)
        return render_template('addaccommodation.html', Cities = cities)


* Add Accommodation Comment
This method adds new comment for the *Accommodation_Comments* table . Query is *"""INSERT INTO Accommodation_Comments (Accommodation_ID, Accommodation_Comment_Text) VALUES (%s,%s)"""*
Comments text taken from the user.
   .. code-block:: python

    @app.route('/addaccommodationcomment/<id>', methods=['POST', 'GET'])
    def addaccommodationcomment(id):
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                Comment = request.form['Comment']

                query = """CREATE TABLE IF NOT EXISTS Accommodation_Comments (
                                    Accommodation_Comment_ID SERIAL PRIMARY KEY NOT NULL,
                                    Accommodation_ID INTEGER REFERENCES Accommodation(Accommodation_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                    Accommodation_Comment_Text CHAR(500) NOT NULL
                        );"""
                cursor.execute(query)


                try:
                    queryWithFormat = """INSERT INTO Accommodation_Comments (Accommodation_ID, Accommodation_Comment_Text) VALUES (%s,%s)"""
                    cursor.execute(queryWithFormat, (id, Comment))
                    connection.commit()
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "Something wrong"
            return redirect(url_for('accommodationlist'))
        return render_template('addaccommodationcomment.html', ID=id)

* Update Accommodation
This method updates Accommodation name on the *Accommodation* table.
Query is *"""UPDATE Accommodation SET Accommodation_Name='%s' WHERE Accommodation_ID='%s' """*


   .. code-block:: python

    @app.route('/updateaccommodation/<id>', methods=['POST', 'GET'])
    def updateaccommodation(id):
        if session['isValid'] == False:
            return "You are not authorized"
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                New_Name = request.form['Name']
                try:
                    query = """UPDATE Accommodation SET Accommodation_Name='%s' WHERE Accommodation_ID='%s' """ % (New_Name, id)
                    cursor.execute(query)
                    connection.commit()
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "Something wrong"
            return redirect(url_for('accommodationlist'))
        return render_template('updateaccommodation.html', ID=id)

* Search Accommodation
This method searchs an Accommodation object in database by the Accommodation name.
Query is *"""SELECT Accommodation_ID, Accommodation_Name FROM Accommodation WHERE Accommodation_Name like '%{0}%'"""*
And return the matched accommodation.

   .. code-block:: python

    @app.route('/searchaccommodation', methods=['POST', 'GET'])
    def searchaccommodationy():
        if request.method == 'POST':
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                textstr = request.form['textstr']
                accommodationies = []
                try:
                    query = """SELECT Accommodation_ID, Accommodation_Name FROM Accommodation WHERE Accommodation_Name like '%{0}%'"""
                    cursor.execute(query.format(textstr))
                    for Accommodation_ID, Accommodation_Name in cursor:
                        accommodation = Accommodation(Accommodation_ID,Accommodation_Name)
                        accommodationies.append(accommodation)
                    return render_template('accommodationlist.html', accommodationlist = accommodationies)
                except dbapi2.DatabaseError:
                    connection.rollback()
                    return "Something wrong"
            return "Wronng"
        return render_template('searchaccommodation.html')
