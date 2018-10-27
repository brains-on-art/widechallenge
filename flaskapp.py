from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
from branch_mapper import get_tree
from graph import get_graph_output

app = Flask(__name__)
# CORS(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('demo.html')

@app.route('/tree_by_year', methods=['GET'])
def tree_by_year():
    """GET with a year as a query param"""
    year= request.args.get('year')
    if int(year) < 1900:
        return jsonify({'success': True, 'tree': get_tree(year)}), 200
    else:
        return jsonify({'success': False}), 400

@app.route('/dynamic', methods=['GET'])
def dynamic():
    return render_template('dynamic.html')

@app.route('/graph_by_year', methods=['GET'])
def graph_by_year():
    year = request.args.get('year')
    width = request.args.get('width')
    height = requests.args.get('height')
    if year < 1900:
        return jsonify({'success': True, 'tree': get_graph_output(year,width,height)}), 200
    else:
        return jsonify({'success': False}), 400