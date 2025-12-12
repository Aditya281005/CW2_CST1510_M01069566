import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from flask import Flask, jsonify, request
from data.db import connect_database
from data.incidents import get_all_incidents
from data.datasets import get_all_datasets
from data.tickets import get_all_tickets
from data.users import get_all_users

app = Flask(__name__)

@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    try:
        df = get_all_incidents()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    try:
        df = get_all_datasets()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    try:
        df = get_all_tickets()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        df = get_all_users()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
