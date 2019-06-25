import datetime
import json
import pandas as pd
import pyodbc
from flask import Flask, jsonify, make_response, request

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'localhost'
database = 'AttendanceApp_db4'
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
    return (r[0] if r else None) if one else r


my_query = query_db("select Studenci.id, Studenci.firstName, Studenci.lastName, Obecnosci.[group] from Studenci, Obecnosci WHERE Studenci.id = Obecnosci.id;", )
print(my_query)



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
    my_query1 = query_db("select Studenci.nr_indeksu, Studenci.firstName, Studenci.lastName from Studenci;", )
    print(my_query1)
    return jsonify(my_query1), {"Content-Type": "application/json"}


@app.route('/api/lecture/latest', methods=['GET'])
def get_latest_lecture():
    cur2 = cnxn.cursor()
    cur3 = cnxn.cursor()
    cur2.execute("select className from Przedmioty where classID = 1")
    a1 = str(cur2.fetchone())
    b1 = a1.rstrip("\'), ")
    data_class = b1.lstrip("(\'")
    cur3.execute("select [group] from Obecnosci where nr = 1")
    a2 = str(cur3.fetchone())
    b2 = a2.rstrip("\'), ")
    data_group = b2.lstrip("(\'")
    my_query3 = query_db("select Studenci.id, Studenci.firstName, Studenci.lastName, Obecnosci.[group], Obecnosci.isPresent from Studenci, Obecnosci WHERE Studenci.id = Obecnosci.id;", )
    return jsonify(className=data_class,
                   classGroupName=data_group,
                   classStartDate=datetime.datetime.now(),
                   classEndDate=datetime.datetime.now() + datetime.timedelta(minutes=90),
                   studentsList=my_query3), {"Content-Type": "application/json"}


@app.route('/api/lecture/latest', methods=['PUT'])
def update_latest_lecture():

    i = 0
    request_data = json.loads(request.data)
    print(request_data)
    print(request_data[0]['id'])
    print(request_data[0]['isPresent'])
    print(request_data[1]['id'])
    print(request_data[1]['isPresent'])

    students_attendance.clear()
    cur4 = cnxn.cursor()
    for s in request_data:
        print("UPDATE Obecnosci SET isPresent = " + bool_to_bit(
            request_data[i]['isPresent']) + " where id = \'" + str(request_data[i]['id']) + "\';")
        cur4.execute("UPDATE Obecnosci SET isPresent = " + bool_to_bit(
            request_data[i]['isPresent']) + " where id = \'" + str(request_data[i]['id']) + "\';")
        cnxn.commit()
        i += 1
        students_attendance.append(s)
    print(students_attendance)
    return jsonify(students_attendance), {"Content-Type": "application/json"}


@app.route('/api/calendar/all', methods=['GET'])
def get_from_calendar():
    return jsonify(calendar_data), {"Content-Type": "application/json"}



def bool_to_bit(x):
    if x == True:
        x = 1
    if x == False:
        x = 0
    return str(x)


@app.route('/api/student', methods=['POST'])
def add_new_student():
    request_data = json.loads(request.data)
    print(request_data)
    print("INSERT INTO Studenci(firstName,lastName,nr_indeksu,id) VALUES(\'" + str(request_data['firstName']) + "\',\'" + str(request_data['lastName']) + "\'," + str(request_data['id']) + ",\'" + str(request_data['cardId']) + "\')")
    cur6 = cnxn.cursor()
    cur6.execute("INSERT INTO Studenci(firstName,lastName,nr_indeksu,id) VALUES(\'" + str(request_data['firstName']) + "\',\'" + str(request_data['lastName']) + "\'," + str(request_data['id']) + ",\'" + str(request_data['cardId']) + "\')")
    cnxn.commit()
    return jsonify('OK'), {"Content-Type": "application/octet-stream"}


@app.route('/api/report', methods=['POST'])
def generate_report():
    request_data = json.loads(request.data)
    print(request_data)
    cur7 = cnxn.cursor()
    if request_data['type'] == 'student':
        print("SELECT * FROM Obecnosci Where id = \'" + request_data['id'] + '\'')
        df = pd.read_sql("SELECT * FROM Obecnosci Where id = \'" + str(request_data['id']) + '\'', cnxn)
        print(df)
        f = open('report-student-' + str(request_data['id']) + '.txt', "w")
        f.write("REPORT FOR STUDENT WITH ID: " + str(request_data['id']) + "\n")
        f.write("\n" + str(df))
        f.close()
        writer = pd.ExcelWriter('excel-student-' + str(request_data['id']) + '.xlsx')
        df.to_excel(writer, 'DataFrame')
        writer.save()
    if request_data['type'] == 'class':
        print("SELECT * FROM Obecnosci WHERE classID = " + request_data['id'])
        df = pd.read_sql("SELECT * FROM Obecnosci WHERE classID = " + str(request_data['id']), cnxn)
        print(df)
        f = open('report-class-' + str(request_data['id']) + '.txt', "w")
        f.write("REPORT FOR CLASS WITH ID: " + str(request_data['id']) + "\n")
        f.write("\n" + str(df))
        f.close()
        writer = pd.ExcelWriter('excel-class-' + str(request_data['id']) + '.xlsx')
        df.to_excel(writer, 'DataFrame')
        writer.save()
    return jsonify(request_data), {"Content-Type": "application/json"}

@app.route('/api/students/file', methods=['GET'])
def export_students_list():
    print("SELECT * FROM Studenci")
    df1 = pd.read_sql("SELECT * FROM Studenci", cnxn)
    print(df1)
    df1.to_csv(r'Students_List.csv')
    return jsonify('OK'), {"Content-Type": "application/octet-stream"}

@app.route('/api/card/recent', methods=['GET'])
def get_last_card_id():
    cur8 = cnxn.cursor()

    cur8.execute("select lastCardID from cardID where id = 1")
    a = str(cur8.fetchone())
    b = a.rstrip("\'), ")
    x = b.lstrip("(\'")
    print(x)
    return jsonify(x), {"Content-Type": "application/json"}


@app.route('/api/students/file', methods=['POST'])
def read_from_file():
    print(request.files.get('myFileName').filename)
    return jsonify('OK'), {"Content-Type": "application/octet-stream"}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)