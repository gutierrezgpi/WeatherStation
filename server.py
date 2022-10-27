from flask import Flask
from flask import render_template
from datetime import datetime
import csv

import datalogger1 as dl

app = Flask(__name__)

@app.route('/')
def index():

    date = datetime.now().strftime("%Y-%m-%d")
    #date = "2022-10-23"

    dl.convert(date)

    data_file = open("data/data-"+date+".csv", "r")
    data_file = csv.reader(data_file, delimiter=",")
    data_file = list(data_file)
    data_file_size = len(data_file)

    now = data_file[data_file_size-1]
    
    return render_template('index.html', now=now)
