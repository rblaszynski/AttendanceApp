from flask import Flask, jsonify, abort, request, make_response
import json
import datetime

app = Flask(__name__, static_url_path="")
now = datetime.datetime.now()
endDate = datetime.datetime(now.year, now.month, now.day, now.hour+1, now.minute+30)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/students/all', methods=['GET'])
def get_list_of_students():
    students = []
    return jsonify(students), {"Content-Type": "application/json"}


@app.route('/lecture/latest', methods=['GET'])
def get_latest_lecture():
    students = []
    return jsonify(className='class name',
                   classGroupName="group name",
                   classStartDate=now,
                   classEndDate=endDate), {"Content-Type": "application/json"}


@app.route('/calendar/all', methods=['GET'])
def get_from_calendar():
    calendar_data = []
    return jsonify(calendar_data), {"Content-Type": "application/json"}


@app.route('/students/all', methods=['POST'])
def read_from_file(filename):
    f = open(filename, 'r')
    print(f.read())
    return jsonify(filename=filename), {"Content-Type": "application/json"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
