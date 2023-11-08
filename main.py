from flask import Flask, render_template  

app = Flask(__name__)

@app.route('/albert')
def hello_albert():
    return render_template("index.html")  

@app.route('/alfred')
def hello_alfred():
    return render_template("index2.html")  

if __name__ == '__main__':
    app.run(debug=True)


