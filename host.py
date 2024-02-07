from flask import Flask, render_template
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return render_template('index.html', servers=11, users=1064)

def run():
  app.run(host='0.0.0.0',port=2020)

def alive():  
    t = Thread(target=run)
    t.start()