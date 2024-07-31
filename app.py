import requests
import json
from dotenv import load_dotenv
import openai
import pandas as pd
from flask import Flask, request, render_template, jsonify
# from get_results import GetResults
from get_results1 import GetResults
from flask_cors import CORS  # Import CORS

# dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [ "http://localhost:3003", "http://127.0.0.1:3003", "https://main.dbjnrfke1zuu7.amplifyapp.com", "https://staging.dbjnrfke1zuu7.amplifyapp.com" ]}})  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def get_results():
    req = request.get_json()
    gr = GetResults(label=req['db_name'])
    result=gr.get_results(input_text= req['query'])
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Change '*' to specific origin if needed
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
