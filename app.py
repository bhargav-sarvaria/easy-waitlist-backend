from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from mongo import *
from message_service import *
from key_config import *
from url_shortner import *

app = Flask(__name__)


@app.route('/', methods=['get'])
def test():
    return 'test'


@app.route('/getWaitlist', methods=['post'])
@cross_origin()
def request_get_waitlist():
    if request.method == 'POST':
        place_id = request.args.get('place_id')
        result = get_waitlist(str(place_id))
        if result:
            print(jsonify({'success': True, 'data': result}))
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'error': True})
    return jsonify({'error': True})


@app.route('/getPlaceName', methods=['POST'])
@cross_origin()
def getPlaceName():
    if request.method == 'POST':
        print(request.json)
        place_id = request.json['place_id']
        return get_place_name(place_id)
    return jsonify({'error': True, 'message': 'Not a post request'})


@app.route('/isServed', methods=['POST'])
@cross_origin()
def isServed():
    if request.method == 'POST':
        print(request.json)
        place_id = request.json['place_id']
        wait_id = request.json['wait_id']
        return is_served(place_id, wait_id)
    return jsonify({'error': True, 'message': 'Not a post request'})


@app.route('/getWaitlistPos', methods=['GET'])
@cross_origin()
def request_get_waitlist_position():
    if request.method == 'GET':
        place_id = request.args.get('place_id')
        result = get_waitlist_position(str(place_id))
        if result:
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'error': True})
    return jsonify({'error': True})


@app.route('/setWaitlist', methods=['post'])
@cross_origin()
def request_set_waitlist():
    if request.method == 'POST':
        print(request.json)
        place_id = request.json['place_id']
        user = request.json['user']
        add_users = request.json['users']
        request_type = request.json['request_type']

        result = set_waitlist(str(place_id), add_users, request_type, user)
        if result:
            if request_type == 'Add':
                short_url = shorten(APP_URL + 'lobby/' + str(place_id) + '?wid=' + str(user['wait_id']))
                print(short_url)
                send_sms(add_users[-1]['name'], add_users[-1]['mobile_no'], short_url)
            return jsonify({'success': True})
        else:
            return jsonify({'error': True})
    return jsonify({'error': True})


@app.route('/register', methods=['post'])
@cross_origin()
def register():
    print(request.json)
    if request.method == 'POST':
        name = request.json['name']
        email = request.json['email']
        mobile_no = request.json['mobile_no']
        password = request.json['password']

        _id = abs(hash(email)) % (10 ** 5)

        if checkIfEmailExists(email):
            return jsonify({'error': True, 'message': 'Given Email-id is already registered'})

        if checkIfMobileNoExists(mobile_no):
            return jsonify({'error': True, 'message': 'Given Mobile No. is already registered'})

        user = {"_id": _id, "name": name, "mobile_no": mobile_no, "email": email, "password": password}
        register_user(user)
        return jsonify({'success': True, '_id': _id})

    return jsonify({'error': True, 'message': 'Not a post request'})


@app.route('/login', methods=['POST'])
@cross_origin()
def check():
    if request.method == 'POST':
        print(request.json)
        email = request.json['email']
        password = request.json['password']
        return check_login(email, password)
    return jsonify({'error': True, 'message': 'Not a post request'})


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    # app.run(threaded=True, port=5000)
    # run_simple('0.0.0.0', 9000, app)
    app.run(host='0.0.0.0')

