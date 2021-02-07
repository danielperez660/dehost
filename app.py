from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))

    states = ("selected", "deselected", "deselected")
    return render_template("base.html", states=states)


@app.route('/sites', methods=["POST", "GET"])
def sites():
    if request.method == 'POST':
        return redirect(url_for('sites'))

    states = ("deselected", "selected", "deselected")
    return render_template("base.html", states=states)


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if request.method == 'POST':
        return redirect(url_for('settings'))

    states = ("deselected", "deselected", "selected")
    return render_template("base.html", states=states)


if __name__ == '__main__':
    app.run()
