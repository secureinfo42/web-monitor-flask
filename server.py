#!/usr/bin/env python3

##################################################################################################################################
#    ┏━┓┏━┓┏━┓   ╻ ╻┏━╸┏┓ 
#    ┣━┫┣━┛┣━┛   ┃╻┃┣╸ ┣┻┓
#    ╹ ╹╹  ╹     ┗┻┛┗━╸┗━┛
###

from flask import Flask, render_template, request, redirect, url_for, session
from backend import scan

app = Flask(__name__)

# Routes #########################################################################################################################

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        url = request.form['url']   
        reported_data = scan.scan(request.form['url'])
        return render_template('report.html', result=reported_data )
    if request.method == 'GET':
        return render_template('index.html' )

# Run flask ######################################################################################################################

if __name__ == '__main__':

    app.run(debug=True,port=5000)
