
# imports for SQL data part
import pyodbc
from datetime import datetime, timedelta
import pandas as pd

cnxn_str = (
       "Driver={SQL Server Native Client 11.0};"
       "Server=UKXXX00123,45600;"
       "Database=DB01;"
       "UID=JoeBloggs;"
       "PWD=Password123;"
)

#cnxn = pyodbc.connect(cnxn_str)
cnxn = pyodbc.connect(cnxn_str)

cnxn = pyodbc.connect(cnxn_str)  # initialise connection (assume we have already defined cnxn_str)

# build up our query string
query = ("SELECT * FROM customers "
         f"WHERE joinDate > '{date}'")

# execute the query and read to a dataframe in Python
data = pd.read_sql(query, cnxn)

del cnxn  # close the connection
