import datetime

from flask import Flask, jsonify, make_response

app = Flask(__name__, static_url_path="")
now = datetime.datetime.now()
endDate = datetime.datetime.now() + datetime.timedelta(minutes=90)


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
    students = []
    groups = ['PT-1', 'PZ-1']
    student = {}
    student['id'] = 111111
    student['firstName'] = 'Michal'
    student['lastName'] = 'Andrzejewski'
    student['groups'] = groups
    students.append(student)

    student = {}
    student['id'] = 22222
    student['firstName'] = 'Przemyslaw'
    student['lastName'] = 'Barlog'
    student['groups'] = groups
    students.append(student)

    student = {}
    student['id'] = 33333
    student['firstName'] = 'Dominik'
    student['lastName'] = 'Blaszczyk'
    student['groups'] = groups
    students.append(student)

    student = {}
    student['id'] = 44444
    student['firstName'] = 'Robert'
    student['lastName'] = 'Blaszynski'
    student['groups'] = groups
    students.append(student)

    return jsonify(students), {"Content-Type": "application/json"}


@app.route('/api/lecture/latest', methods=['GET'])
def get_latest_lecture():
    students = []
    return jsonify(className='class name',
                   classGroupName="group name",
                   classStartDate=now,
                   classEndDate=endDate), {"Content-Type": "application/json"}


@app.route('/api/calendar/all', methods=['GET'])
def get_from_calendar():
    calendar_data = []
    return jsonify(calendar_data), {"Content-Type": "application/json"}


@app.route('/api/students/all', methods=['POST'])
def read_from_file(filename):
    f = open(filename, 'r')
    print(f.read())
    return jsonify(filename=filename), {"Content-Type": "application/json"}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
