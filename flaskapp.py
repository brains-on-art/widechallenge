from flask import Flask, request, jsonify, current_app
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def tree_by_year():
    """GET with a year as a query param"""
    year= request.args.get('year')
    if year:
        # current_app.logger.info("POST {}".format(result))
        return jsonify({'success': True, 'tree': 'asdf'}), 200
    else:
        # current_app.logger.warning("IMAGE POST FAILED")
        return jsonify({'success': False}), 400
