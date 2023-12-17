from flask import Flask, request, jsonify
from flask_cors import CORS
from court_case_search import getResponse

app = Flask(__name__)
CORS(app)

@app.route('/api/generate_response', methods=['POST'])
def generate_response():
    data = request.get_json()
    user_input = data.get('user_input', '')
    response = getResponse(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
