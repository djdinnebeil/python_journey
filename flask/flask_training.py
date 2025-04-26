from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/greet/<name>', methods=['GET', 'POST'])
def greet(name):
    if len(name) > 100:
        return jsonify(error='Name too long'), 400
    if any(c in name for c in ['<', '>', '{', '}', ';']):
        return jsonify(error='Invalid characters in name'), 400
    if request.method == 'POST':
        return jsonify(message=f'This is POST by {name}.')
    return jsonify(message=f'Hello, {name}!')

@app.errorhandler(404)
def not_found_error(error):
    return jsonify(error='Resource not found'), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify(error='Method not allowed'), 405

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify(error='An unexpected error occurred'), 500

if __name__ == '__main__':
    app.run(debug=True)
