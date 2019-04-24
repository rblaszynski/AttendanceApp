from flask import Flask, jsonify, make_response

app = Flask(__name__, static_url_path="")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
