from flask import Flask, render_template, request, redirect, url_for, g
from database_manager import DBManager

app = Flask(__name__)
DB = DBManager()


@app.route('/', methods=["POST", "GET"])
@app.route('/sites', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))

    g.states = ("selected", "deselected", "deselected")
    return render_template("main_console.html")


@app.route('/new', methods=["POST", "GET"])
def sites():
    if request.method == 'POST':
        return redirect(url_for('sites'))

    g.states = ("deselected", "selected", "deselected")
    return render_template("deploy_new.html", )


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if request.method == 'POST':
        return redirect(url_for('settings'))

    g.states = ("deselected", "deselected", "selected")
    return render_template("settings.html")


if __name__ == '__main__':
    app.run()
