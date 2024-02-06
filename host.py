from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return {"servers": "21", "users": "987"}

def run():
  app.run(host='0.0.0.0',port=2020)

def alive():  
    t = Thread(target=run)
    t.start()