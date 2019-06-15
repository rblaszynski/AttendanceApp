import datetime
from flask import Flask, jsonify, make_response, request
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

# test
print(data)


def query_db(query, args=(), one=False):
    cur = cnxn.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    # cur.connection.close()
    return (r[0] if r else None) if one else r


# test
my_query = query_db("select Studenci.id, Studenci.firstName, Studenci.lastName, Obecnosci.[group] from Studenci, Obecnosci WHERE Studenci.id = Obecnosci.id;", )
print(my_query)
# my_query2 = query_db("select Studenci.id, Studenci.firstName, Studenci.lastName, Obecnosci.[group] from Studenci, Obecnosci WHERE Studenci.id = Obecnosci.id;", )
# print(my_query2)
# json_output = json.dumps(my_query)
# print(json_output)


app = Flask(__name__, static_url_path="")
students = [
    {'id': 111111, 'firstName': 'Michał', 'lastName': 'Andrzejewski', 'group': 'TI-1'},
    {'id': 222222, 'firstName': 'Przemysław', 'lastName': 'Barłóg', 'group': 'TI-2'},
    {'id': 333333, 'firstName': 'Dominik', 'lastName': 'Błaszczyk', 'group': 'TI-3'},
    {'id': 444444, 'firstName': 'Robert', 'lastName': 'Błaszyński', 'group': 'TI-4'},
]

students_attendance = [
    {'id': 111111, 'firstName': 'Michał', 'lastName': 'Andrzejewski', 'group': 'TI-1', 'isPresent': True},
    {'id': 222222, 'firstName': 'Przemysław', 'lastName': 'Barłóg', 'group': 'TI-2', 'isPresent': True},
    {'id': 333333, 'firstName': 'Dominik', 'lastName': 'Błaszczyk', 'group': 'TI-3', 'isPresent': False},
    {'id': 444444, 'firstName': 'Adam', 'lastName': 'Błaszyński', 'group': 'TI-4', 'isPresent': False},
]

calendar_data = [
    {'title': 'TSM', 'color': {'primary': '#ad2121'},
     'start': datetime.datetime.now() - datetime.timedelta(minutes=360),
     'end': datetime.datetime.now() - datetime.timedelta(minutes=300), 'meta': {'location': "A1"}},
    {'title': 'PTM', 'color': {'primary': '#1e90ff'},
     'start': datetime.datetime.now() - datetime.timedelta(minutes=240),
     'end': datetime.datetime.now() - datetime.timedelta(minutes=180), 'meta': {'location': "A2"}},
]


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def default():
    return jsonify('hello'), {"Content-Type": "application/json"}


@app.route('/api/students/all', methods=['GET'])
def get_list_of_students():
    my_query1 = query_db("select Studenci.id, Studenci.firstName, Studenci.lastName, Obecnosci.[group] from Studenci, Obecnosci WHERE Studenci.id = Obecnosci.id;", )
    # return jsonify('OK'), {"Content-Type": "application/octet-stream"}
    return jsonify(my_query1), {"Content-Type": "application/json"}
    # return jsonify(students), {"Content-Type": "application/json"}


@app.route('/api/lecture/latest', methods=['GET'])
def get_latest_lecture():
    cur2 = cnxn.cursor()
    cur3 = cnxn.cursor()

    cur2.execute("select className from Obecnosci where nr = 1")
    data_class = str(cur2.fetchall())
    # data_class = query_db("select className from Obecnosci where nr = 1")
    cur3.execute("select [group] from Obecnosci where nr = 1")
    data_group = str(cur3.fetchall())
    # data_group = query_db("select [group] from Obecnosci where nr = 1")
    my_query3 = query_db("select Studenci.id, Studenci.firstName, Studenci.lastName, Obecnosci.[group], Obecnosci.isPresent from Studenci, Obecnosci WHERE Studenci.id = Obecnosci.id;", )
    return jsonify(className=data_class,
                   classGroupName=data_group,
                   classStartDate=datetime.datetime.now(),
                   classEndDate=datetime.datetime.now() + datetime.timedelta(minutes=90),
                   studentsList=my_query3), {"Content-Type": "application/json"}


@app.route('/api/lecture/latest', methods=['PUT'])
def update_latest_lecture():

    # i = 0
    request_data = json.loads(request.data)
    print(request_data)
    print(request_data[0]['id'])
    print(request_data[0]['isPresent'])
    print(request_data[1]['id'])
    print(request_data[1]['isPresent'])
    cur5 = cnxn.cursor()
    cur5.execute("""UPDATE AttendanceApp_db.dbo.Obecnosci SET isPresent = 1 WHERE id = '013697D7';""")


    # for i in range(1):
    #     cur4 = cnxn.cursor()
    #     # j = i + 1
    #     cur4.execute("UPDATE AttendanceApp_db.dbo.Obecnosci SET isPresent = " + bool_to_bit(request_data[i]['isPresent']) + " where id = \'" + str(request_data[i]['id']) + "\';")

    students_attendance.clear()

    for s in request_data:
        # j = i + 1
        # cur4.execute("UPDATE Obecnosci SET isPresent = " + str(bit_to_bool(request_data[i]['isPresent'])) + " where nr = " + str(j))
        # i += 1
        students_attendance.append(s)
    print(students_attendance)
    return jsonify(students_attendance), {"Content-Type": "application/json"}


@app.route('/api/calendar/all', methods=['GET'])
def get_from_calendar():
    return jsonify(calendar_data), {"Content-Type": "application/json"}


@app.route('/api/students/all', methods=['POST'])
def read_from_file():
    print(request.files.get('myFileName').filename)
    return jsonify('OK'), {"Content-Type": "application/octet-stream"}


def bool_to_bit(x):
    if x == True:
        x = 1
    if x == False:
        x = 0
    return str(x)


@app.route('/api/student', methods=['POST'])
def add_new_student():
    return jsonify('OK'), {"Content-Type": "application/octet-stream"}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
