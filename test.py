import threading
from flask import Flask
from flask_spyne import Spyne

app = Flask(__name__)
spyne = Spyne(app)

class TestProject():
    def testMethod():
        return "Test Succesful"

if __name__ == '__main__':
    app.run(host = '127.0.5.1')