Developer Guide
===============

Database design has 14 tables. UML Entity-Relationship diagram of the design is given below.


   .. figure:: erDiag.png
      :scale: 100 %
      :alt:

      ER diagram of the database


Classes
++++++
Classes are used for Add/Delete/Update/Search operations. They are implemented for all main tables.


   .. code-block:: python

    class City:
        def __init__(self, ID, Name):
            self.ID = ID
            self.Name = Name
            self.Comments = [];

    class Team:
        def __init__(self,ID,Name):
            self.ID = ID
            self.Name = Name
            self.Comments = []

    class Player:
        def __init__(self,ID,Name):
            self.ID = ID
            self.Name = Name
            self.Comments = []

    class Tournament:
        def __init__(self,ID,Name):
            self.ID = ID
            self.Name = Name
            self.Comments = []

    class Country:
        def __init__(self, ID, Name):
            self.ID = ID
            self.Name = Name

    class Author:
        def __init__(self,ID,Name,WorkDescription):
            self.ID = ID
            self.Name = Name
            self.WorkDescription = WorkDescription

    class Accommodation:
        def __init__(self, ID, Name):
            self.ID = ID
            self.Name = Name
            self.Comments= []


Code
++++

.. toctree::

   member1
   member2
   member3
   member4
   member5
