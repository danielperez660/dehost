from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))

    g.states = ("selected", "deselected", "deselected")
    return render_template("main_console.html")


@app.route('/sites', methods=["POST", "GET"])
def sites():
    if request.method == 'POST':
        return redirect(url_for('sites'))

    g.states = ("deselected", "selected", "deselected")
    return render_template("main_console.html", )


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if request.method == 'POST':
        return redirect(url_for('settings'))

    g.states = ("deselected", "deselected", "selected")
    return render_template("main_console.html")


if __name__ == '__main__':
    app.run()
