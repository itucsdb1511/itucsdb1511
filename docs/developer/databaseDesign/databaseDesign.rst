Database Design
---------------

Database design has 14 tables. UML Entity-Relationship diagram of the design is given below.


   .. figure:: erDiag.png
      :scale: 100 %
      :alt:

      ER diagram of the database
      
      
Tables
-----

City Table
++++++++
* Attributes of the City Table:

   .. figure:: citytable.png
      :scale: 75 %
      :alt:

      City Table 

* Tournament cities are located on this table.It has 3 attributes and 1 primary key and 1 foreign key.
* City_ID: Keeps the id number of the city.
* City_Name: Keeps name of the city in char type.
* City_CountryID: Foreign key. It associates country with the city.

**SQL statement that initialize the City Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS City (
       City_ID SERIAL PRIMARY KEY NOT NULL,
       City_Name CHAR(50) NOT NULL,
       City_CountryID INT REFERENCES Country (Country_ID) ON DELETE CASCADE ON UPDATE CASCADE)
  



City Comment Table
++++++++
* Attributes of the City Comment Table:

   .. figure:: citycommenttable.png
      :scale: 75 %
      :alt:

      City Comment Table 

* City comments are located on this table.It has 3 attributes and 1 primary key and 1 foreign key. 
* City_CommentID: Keeps the id number of the City Comment.
* City_ID: Foreign key. It associates city comments with the city.
* City_Comment_Text: Keeps the comment of the city.

**SQL statement that initialize the City Comments Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS City_Comments (
       City_Comment_ID SERIAL PRIMARY KEY NOT NULL,
       City_ID INTEGER REFERENCES City(City_ID) ON DELETE CASCADE ON UPDATE CASCADE,
       City_Comment_Text CHAR(500) NOT NULL)
  


Country Table
++++++++
* Attributes of the Country Table:

   .. figure:: countrytable.png
      :scale: 75 %
      :alt:

      Country Table 

* Tournament city countries are located on this table.It has 2 attributes and 1 primary key and Country_Name.
* Country_ID: Keeps the id number of the country.
* Country_Name: Keeps name of the country in char type.

**SQL statement that initialize the Country Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Country (
        Country_ID SERIAL PRIMARY KEY NOT NULL,
        Country_Name CHAR(50) NOT NULL)

Accommodation Table
++++++++
* Attributes of the Accommodation Table:

   .. figure:: accommodationtable.png
      :scale: 75 %
      :alt:

      Accommodation Table 


* Tournament accommodations are located on this table.It has 3 attributes and 1 primary key and 1 foreign key.
* Accommodation_ID: Keeps the id number of the accommodation . Accommodation_Name: Keeps name of the hotel in char type.
* Accommodation_CityID: Foreign key. It associates city with the hotel.


**SQL statement that initialize the Accommodation Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Accommodation (
       Accommodation_ID SERIAL PRIMARY KEY NOT NULL,
       Accommodation_Name CHAR(50) NOT NULL,
       Accommodation_CityID INT REFERENCES City (City_ID) ON DELETE CASCADE ON UPDATE CASCADE)


Accommodation Comment Table
++++++++
* Attributes of the Accommodation Comment Table:

   .. figure:: accommodationcommenttable.png
      :scale: 75 %
      :alt:

      Accommodation Comments Table 

* Tournament accommodations comments are located on this table.It has 3 attributes and 1 is primary key.
* Accommodation_Comment_ID:Keepstheidnumberoftheaccommodation comments. 
* Accommodation_ID: Foreign key. It associates city comments with the city. 
* Accommodation_Comment_Text:Keeps the comment of the hotel.


**SQL statement that initialize the Accommodation Comments Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Accommodation_Comments (
       Accommodation_Comment_ID SERIAL PRIMARY KEY NOT NULL,
       Accommodation_ID INTEGER REFERENCES Accommodation(Accommodation_ID) ON DELETE CASCADE ON UPDATE CASCADE,
       Accommodation_Comment_Text CHAR(500) NOT NULL)


Team Table
++++++++
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
++++++++
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



Player Table
++++++++
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
++++++++
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
                    



Admin Table
++++++++
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
