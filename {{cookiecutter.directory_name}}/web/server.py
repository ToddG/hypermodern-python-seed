from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World from {{cookiecutter.project_name}}!'

if __name__ == '__main__':
    # THINK CAREFULLY ABOUT HOW THIS IS EXPOSED IN A REAL APP!!!
    app.run(host="0.0.0.0", port=8080)
