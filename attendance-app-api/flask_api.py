import codecs
import csv
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
    my_query3 = query_db("select Studenci.nr_indeksu, Studenci.firstName, Studenci.lastName, Obecnosci.[group], Obecnosci.isPresent from Studenci, Obecnosci WHERE Studenci.id = Obecnosci.id;", )
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
    print(request_data[0]['nr_indeksu'])
    print(request_data[0]['isPresent'])
    print(request_data[1]['nr_indeksu'])
    print(request_data[1]['isPresent'])

    students_attendance.clear()
    cur4 = cnxn.cursor()
    for s in request_data:
        print("UPDATE Obecnosci SET isPresent = " + bool_to_bit(
            request_data[i]['isPresent']) + "from Obecnosci, Studenci where Obecnosci.id = Studenci.id and Studenci.nr_indeksu = " + str(request_data[i]['nr_indeksu']))
        cur4.execute("UPDATE Obecnosci SET isPresent = " + bool_to_bit(
            request_data[i]['isPresent']) + "from Obecnosci, Studenci where Obecnosci.id = Studenci.id and Studenci.nr_indeksu = " + str(request_data[i]['nr_indeksu']))
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
    print("INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id) values('2019-06-12',1,'TI-1', '15:10','16:40',0," + ",\'" + str(request_data['cardId']) + "\')")
    cur9 = cnxn.cursor()
    cur9.execute("INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id) values('2019-06-12',1,'TI-1', '15:10','16:40',0," + "\'" + str(request_data['cardId']) + "\')")
    cnxn.commit()
    return jsonify('OK'), {"Content-Type": "application/octet-stream"}


@app.route('/api/report', methods=['POST'])
def generate_report():
    request_data = json.loads(request.data)
    print(request_data)
    cur11 = cnxn.cursor()
    cur12 = cnxn.cursor()
    if request_data['type'] == 'student':
        print("select lastName from Studenci where nr_indeksu = \'" + str(request_data['id']) + '\'')
        cur11.execute("select lastName from Studenci where nr_indeksu = \'" + str(request_data['id']) + '\'')
        a = str(cur11.fetchone())
        b = a.rstrip("\'), ")
        x = b.lstrip("(\'")
        print("select Przedmioty.classID, Przedmioty.className, Obecnosci.[group], Obecnosci.[data], "
                         "Obecnosci.classStartDate, Obecnosci.classEndDate, Obecnosci.isPresent from Studenci, "
                         "Obecnosci, Przedmioty where nr_indeksu = \'" + str(request_data['id']) + '\'' +"and Studenci.id = Obecnosci.id and Przedmioty.classID = Obecnosci.classID")
        df = pd.read_sql("select Przedmioty.classID, Przedmioty.className, Obecnosci.[group], Obecnosci.[data], "
                         "Obecnosci.classStartDate, Obecnosci.classEndDate, Obecnosci.isPresent from Studenci, "
                         "Obecnosci, Przedmioty where nr_indeksu = \'" + str(request_data['id']) + '\'' +"and Studenci.id = Obecnosci.id and Przedmioty.classID = Obecnosci.classID", cnxn)
        print(df)
        f = open('report-student-' + str(x) + '.txt', "w")
        f.write("REPORT FOR STUDENT WITH ID: " + str(request_data['id']) + "\n")
        f.write("STUDENT SURNAME: " + str(x) + "\n")
        f.write("\n" + str(df))
        f.close()
        writer = pd.ExcelWriter('excel-student-' + str(x) + '.xlsx')
        df.to_excel(writer, 'DataFrame')
        writer.save()
        file_data = codecs.open('report-student-' + str(x) + '.txt', 'rb').read()
        response = make_response()
        response.data = file_data
    if request_data['type'] == 'class':
        print("select className from Przedmioty where classID = \'" + request_data['id'] + '\'')
        cur12.execute("select className from Przedmioty where classID = " + request_data['id'])
        a = str(cur12.fetchone())
        b = a.rstrip("\'), ")
        x = b.lstrip("(\'")
        print("select Studenci.nr_indeksu, Studenci.lastName, Studenci.firstName, Obecnosci.[group], "
                         "Obecnosci.[data], Obecnosci.classStartDate, Obecnosci.classEndDate, "
                         "Obecnosci.isPresent from Studenci, Obecnosci where classID = " + str(request_data['id']) +" and Studenci.id = Obecnosci.id")
        df = pd.read_sql("select Studenci.nr_indeksu, Studenci.lastName, Studenci.firstName, Obecnosci.[group], "
                         "Obecnosci.[data], Obecnosci.classStartDate, Obecnosci.classEndDate, "
                         "Obecnosci.isPresent from Studenci, Obecnosci where classID = " + str(request_data['id']) +" and Studenci.id = Obecnosci.id", cnxn)
        print(df)
        f = open('report-class-' + str(x) + '.txt', "w")
        f.write("REPORT FOR CLASS WITH ID: " + str(request_data['id']) + "\n")
        f.write("\n" + str(df))
        f.close()
        writer = pd.ExcelWriter('excel-class-' + str(x) + '.xlsx')
        df.to_excel(writer, 'DataFrame')
        writer.save()
        file_data = codecs.open('report-class-' + str(x) + '.txt', 'rb').read()
        response = make_response()
        response.data = file_data
    return response, 200, {"Content-Type": "blob"}

@app.route('/api/students/file', methods=['GET'])
def export_students_list():
    print("SELECT * FROM Studenci")
    df1 = pd.read_sql("SELECT * FROM Studenci", cnxn)
    print(df1)
    df1.to_csv(r'Students_List.csv')
    file_data = codecs.open('Students_List.csv', 'rb').read()
    response = make_response()
    response.data = file_data
    return response, {"Content-Type": "blob"}

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
    file = request.files['myFileName']
    if file:
        filename = file.filename
        file.save(filename)
    cur13 = cnxn.cursor()
    cur13.execute("TRUNCATE TABLE Studenci")
    cnxn.commit()
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row1 in csv_reader:
            if(line_count==0):
                line_count+=1
                continue
            else:
                print(f'\t{row1[2]},{row1[3]},{row1[4]},{row1[5]}')
                cur13.execute(
                "INSERT INTO Studenci(firstName,lastName,nr_indeksu,id) VALUES(\'" + str(row1[2]) + "\',\'" + str(
                    row1[3]) + "\'," + str(row1[4]) + ",\'" + str(row1[5]) + "\')")
                cnxn.commit()
                line_count += 1

    return jsonify('OK'), {"Content-Type": "application/octet-stream"}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
