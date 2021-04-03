from pymongo import MongoClient
from flask import jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId

cluster = MongoClient('mongodb+srv://bhargavsarvaria:bhargav19@mywaitlist.abq9n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['myWaitlist']

users = db['users']


def deleteUser(wait_id, place_id):
    result = db[place_id].delete_one({'wait_id': int(wait_id)})
    if result is not None:
        return  True
    else:
        return False


def createPlaceCollection(place_id):
    place_id = str(place_id)
    result = db[place_id]
    result.insert_one({"name":"test"})
    print(result)


def get_waitlist(place_id):
    try:
        # results = db[place_id].find({})
        results = db[place_id].find({}, {'_id': 0})
        return dumps(list(results))
    except Exception as e:
        print(e)


def get_waitlist_position(place_id):
    try:
        # results = db[place_id].find({})
        results = db[place_id].find({}, {'_id': 0, 'wait_id': 1, 'name': 1})
        return dumps(list(results))
    except Exception as e:
        print(e)


def set_waitlist(place_id, waitlist, request_type, user):
    try:
        if (len(waitlist)) == 0:
            db[place_id].drop()
        else:
            db[place_id].delete_many({})
            db[place_id].insert_many(waitlist)

        print(user)

        if request_type == 'Remove':
            db[place_id + ' served'].insert_one(user)

        if request_type == 'Undo':
            db[place_id + ' served'].delete_one({'wait_id': int(user['wait_id'])})
        return True
    except Exception as e:
        print(e)
        return False


def get_place_name(place_id):
    result = users.find_one({"_id": int(place_id)})
    if result is not None:
        return jsonify({'success': True, 'place_name': str(result['name'])})
    else:
        return False


def is_served(place_id, wait_id):
    result = db[place_id + ' served'].find_one({"wait_id": int(wait_id)})
    if result is not None:
        return jsonify({'success': True, 'is_served': True})
    else:
        return jsonify({'success': True, 'is_served': False})


def checkIfEmailExists(email):
    results = users.find({"email": email})
    if results.count() > 0:
        return True
    return False


def checkIfMobileNoExists(mobile_no):
    results = users.find({"mobile_no": mobile_no})
    if results.count() > 0:
        return True
    return False


def register_user(user):
    users.insert_one(user)


def check_login(email, password):
    result = users.find_one({"email": email})
    print(result)
    message = ''

    if result is None:
        message = 'Couldn\'t find your email address'
    else:
        if password == str(result['password']):
            response = jsonify({'success': True, '_id': str(result['_id'])})
            return response
        else:
            message = 'The password entered is incorrect.'

    response = jsonify({'error': True, 'message': message})
    return response


def generate_id(s):
    return abs(hash(s)) % (10 ** 5)
