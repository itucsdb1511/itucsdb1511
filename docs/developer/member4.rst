Parts Implemented by Alper Kocabiyik
================================


Tables
++++++++
Tournament Table
~~~~~~~~~~~
* Attributes of the Tournament Table: 

* Information about tournaments are located on this table.It has 3 attributes and 1 is primary key. 
* Tournament_ID: Keeps the id number of the tournament.
* Tournament_Name: Keeps the name of the tournament.
* Tournament_CityID:Keeps the Country information about the tournament. Foreign key.

**SQL statement that initialize the Team Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Tournament (
       Tournament_ID SERIAL PRIMARY KEY NOT NULL,
       Tournament_Name CHAR(50) NOT NULL,
       Tournament_CityID INT REFERENCES City (City_ID) ON DELETE CASCADE ON UPDATE CASCADE)


Tournament Comments Table
~~~~~~~~~~~
* Attributes of the Tournament Comments Table:

* Team comments are located on this table.It has 3 attributes and 1 is primary key. 
* Tournament_Comment_ID: Keeps the id number of the tournament comments.
* Tournament_ID: Foreign key. It associates team comments with the tournament itself. 
* Tournament_Comment_Text:Keeps the comment of the tournament.

**SQL statement that initialize the Tournament Comments Table:**
   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Tournament_Comments (
      Tournament_Comment_ID SERIAL PRIMARY KEY NOT NULL,
      Tournament_ID INTEGER REFERENCES Tournament(Tournament_ID) ON DELETE CASCADE ON UPDATE CASCADE,
      Tournament_Comment_Text CHAR(500) NOT NULL)
      
      
Author Table
~~~~~~~~~~~
* Attributes of the Author Table:

* Authors are located on this table.It has 3 attributes and 1 primary key. 
* Author_Student_ID: Keeps the id number of the Author.
* Author_Name: Keeps name of the author in char type.
* Author_Work_Description: Keeps password of the author in char type.


**SQL statement that initialize the Author Table:**

   .. code-block:: sql

    CREATE TABLE IF NOT EXISTS Author (
         Author_Student_ID INT PRIMARY KEY NOT NULL,
         Author_Name CHAR(50) NOT NULL,
         Author_Work_Description CHAR(500) NOT NULL
                    )
                


Methods
++++++

Tournament Methods
~~~~~~~~~~~~~


* Tournament List
This method list the all of the tournaments in the database. Also in this method tournament comment from Tournament Comment table are listed too.

* Add Tournament
This methods add a new tournament to the *Tournament* table. Query is *"""INSERT INTO Tournament (Tournament_Name, Tournament_CityID) VALUES (%s, %s)"""*.
Also this methods control the session. If the session value is false then this operations can not be completed.

* Tournament Delete
This method deletes tournaments from the *Tournament* table. Query is *DELETE FROM Tournament WHERE Tournament_ID={0}*. 
Tournament comments and players connected to corresponding tournament ID are also deleted because of the foreign key.
Also this methods control the session. If the session value is false then this operations can not be completed.

* Update Tournament
This method updates team name on the *Team* table.
Query is *UPDATE Team SET Team_Name='%s' WHERE Team_ID='%s'*
Also this methods control the session. If the session value is false then this operations can not be completed.

* Add Tournament Comment
This method adds new comment for the *Tournament_Comments* table . Query is *INSERT INTO Tournament_Comments 
(Tournament_ID, Tournament_Comment_Text) VALUES (%s, %s)*
Comments text taken from the user.

* Search Tournament
This method searchs an Tournament object in database by the Tournament name.
Query is *SELECT Tournament_ID, Tournament_Name FROM Tournament WHERE Tournament_Name like '%{0}%'*
