from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/pages/index.html")
def pages_index():
    return render_template("/pages/index.html")

app.run()