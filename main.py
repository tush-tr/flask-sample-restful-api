from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
app = Flask(__name__)
data = [
    {
        'id':1,
        'name': 'Rocky',
        'breed': 'germen shephered',
        'age': 2
    },
    {
        'id':2,
        'name': 'Tommy',
        'breed': 'Labra',
        'age': 1
    }
]

# TODO: Get Request stuff (showing data)

@app.route('/',methods =['GET'])
def show():
    return jsonify({'data':data})
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
        'breed': request.json.get('breed'," "),
        'age': request.json.get('age')
    }
    # Append to main data list
    data.append(added)
    return jsonify({'data': added}), 201
# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Jabb","breed":"labra","age":3}' http://localhost:5000




if __name__ == '__main__':
    app.run(debug=True)