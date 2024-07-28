import requests
import json
import openai
import pandas as pd
from flask import Flask, request, render_template
from get_results import GetResults


app = Flask(__name__)

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
    app.run(debug=True)