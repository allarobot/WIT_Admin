from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/record")
def record():
    return render_template("/pages/record.html")

@app.route("/file_import")
def file_import():
    return render_template("/pages/file_import.html")

@app.route("/index")
def index():
    return render_template("/pages/index.html")


@app.route("/jsw",methods=['GET','POST'])
def jsw():
    return "jsw"

@app.route("/ditmco",methods=['GET','POST'])
def ditmco():
    return "pvg"

@app.route("/clear",methods=['GET','POST'])
def clear():
    return "clear"
app.run()