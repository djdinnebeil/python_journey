from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'World')
    return jsonify({'message': f'Hello, {name}!'})

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    return jsonify({'message': 'Datar received', 'data': data})

@app.route('/user', methods=['GET', 'POST'])
def greet_user():
    try:
        # Access form data
        data = request.form.to_dict()
        print(f"Received data: {data}")

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        return jsonify({'message': 'Data received', 'data': data})
    except Exception as e:
        return jsonify({'error': 'Failed to parse form data', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
