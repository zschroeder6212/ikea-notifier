from flask import render_template, send_from_directory


# path /
def index():
    return render_template("index.html")


# path /favicon.ico
def favicon():
    return send_from_directory('static', path='img/favicon.ico')
