import requests
import json
from dotenv import load_dotenv
import openai
import pandas as pd
from flask import Flask, request, render_template
# from get_results import GetResults
from get_results1 import GetResults
from flask_cors import CORS  # Import CORS

# dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def get_results():
    req = request.get_json()
    gr = GetResults(label=req['db_name'])
    result=gr.get_results(input_text= req['query'])
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
