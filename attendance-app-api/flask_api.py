import datetime

from flask import Flask, jsonify, make_response

app = Flask(__name__, static_url_path="")
students = [
    {'id': 111111, 'firstName': 'Michał', 'lastName': 'Andrzejewski', 'group': 'TI-1'},
    {'id': 222222, 'firstName': 'Przemysław', 'lastName': 'Barłóg', 'group': 'TI-2'},
    {'id': 333333, 'firstName': 'Dominik', 'lastName': 'Błaszczyk', 'group': 'TI-3'},
    {'id': 444444, 'firstName': 'Robert', 'lastName': 'Błaszyński', 'group': 'TI-4'},
]

calendar_data = [
    {'title': 'TSM', 'color': {'primary': '#ad2121'}, 'start': datetime.datetime.now(),
     'end': datetime.datetime.now() + datetime.timedelta(minutes=90), 'meta': {'location': "A1"}},
    {'title': 'PTM', 'color': {'primary': '#1e90ff'},
     'start': datetime.datetime.now() + datetime.timedelta(minutes=105),
     'end': datetime.datetime.now() + datetime.timedelta(minutes=200), 'meta': {'location': "A2"}},
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
                   studentsList=students), {"Content-Type": "application/json"}


@app.route('/api/calendar/all', methods=['GET'])
def get_from_calendar():
    return jsonify(calendar_data), {"Content-Type": "application/json"}


@app.route('/api/students/all', methods=['POST'])
def read_from_file(filename):
    f = open(filename, 'r')
    print(f.read())
    return jsonify(filename=filename), {"Content-Type": "application/json"}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
