from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    file = open("result.txt", "r")
    lines = file.readlines()
    return lines[0]
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')

