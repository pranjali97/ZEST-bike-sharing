# ZEST-bike-sharing
This is a Python flask based project that uses sqlite 3 database to store information.
The back-end codes have two files that invoke the most functionality.

File main.py:
  This is the main driver file that has all the api end points and invokes all the functions.
  All of the input data is received here from the front-end templates. Post validation, this data is forwarded to a file (models.py) that handles all the database related functionality.

File models.py 
  This file makes all the communications with the database.
  The file receives various parameters from main.py and post validation, uses appropriate queries to insert, delete and update the database.
  
  
  
  
