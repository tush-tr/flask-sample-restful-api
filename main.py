from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from data import data
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
app = Flask(__name__)

# TODO: Authentication
@auth.get_password
def get_password(username):
    if username == 'tushar':
        return 'mycode'
    return None
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
# $ curl -u tushar:mycode -i http://localhost:5000

# TODO: Get Request stuff (showing data)
@app.route('/', methods=['GET'])
@auth.login_required
def show():
    return jsonify({'data': data})
# curl -i http://localhost:5000

# For getting data of a specific id
@app.route('/<int:data_id>', methods=['GET'])
def showwithid(data_id):
    showdata = [showdata for showdata in data if showdata['id'] == data_id]
    if len(showdata) == 0:
        abort(404)
    return jsonify({'task': showdata[0]})

# curl -i http://localhost:5000/id-number


# TODO: Error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# TODO: Post request stuff(adding more data)
@app.route('/', methods=['POST'])
def create_data():

    if not request.json or not 'name' in request.json:
        abort(400)
    # TODO: Make a schema for data to add to main data list
    added = {
        'id': data[-1]['id'] + 1,
        'name': request.json['name'],
        'breed': request.json.get('breed', " "),
        'age': request.json.get('age')
    }
    # Append to main data list
    data.append(added)
    return jsonify({'data': added}), 201
# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Jabb","breed":"labra","age":3}' http://localhost:5000

# TODO: PUT method
@app.route('/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    updata = [updata for updata in data if updata['id'] == data_id]
    if len(updata) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    if 'breed' in request.json and type(request.json['breed']) is not str:
        abort(400)
    if 'age' in request.json and type(request.json['age']) is not int:
        abort(400)
    updata[0]['name'] = request.json.get('name', updata[0]['name'])
    updata[0]['breed'] = request.json.get('breed', updata[0]['breed'])
    updata[0]['age'] = request.json.get('age', updata[0]['age'])
    return jsonify({'Updated Data': updata[0]})
# curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"Jack","breed":"pug","age":3}' http://localhost:5000/2


# TODO: DELETE Method
@app.route('/<int:data_id>', methods=['DELETE'])
def delete_task(task_id):
    deldata = [deldata for deldata in data if deldata['id'] == task_id]
    if len(deldata) == 0:
        abort(404)
    data.remove(deldata[0])
    return jsonify({'result': True})



if __name__ == '__main__':
    app.run(debug=True)
