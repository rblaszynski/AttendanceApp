import datetime
import json

from flask import Flask, jsonify, make_response, request

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
    return jsonify(students), {"Content-Type": "application/json"}


@app.route('/api/lecture/latest', methods=['GET'])
def get_latest_lecture():
    return jsonify(className='CLASS_NAME',
                   classGroupName="GROUP_NAME",
                   classStartDate=datetime.datetime.now(),
                   classEndDate=datetime.datetime.now() + datetime.timedelta(minutes=90),
                   studentsList=students_attendance), {"Content-Type": "application/json"}


@app.route('/api/lecture/latest', methods=['PUT'])
def update_latest_lecture():
    request_data = json.loads(request.data)
    students_attendance.clear()
    for s in request_data:
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


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
