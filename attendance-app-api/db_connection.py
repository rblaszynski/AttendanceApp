import pyodbc
import json
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'localhost'
database = 'AttendanceApp_db'
username = 'root'
password = 'root'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cursor.execute("select * from Obecnosci;")
data = []
rows = cursor.fetchall()
for row in rows:
    data.append([x for x in row])

print(data)


def query_db(query, args=(), one=False):
    cur = cnxn.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


my_query = query_db("select * from Obecnosci;", )

json_output = json.dumps(my_query)
print(json_output)
