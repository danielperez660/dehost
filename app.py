from flask import Flask, render_template, request, redirect, url_for, g, Response
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
    return render_template("drop.html")


@app.route('/new/<hashed>', methods=["POST"])
def file_manager(hashed):
    g.states = ("deselected", "selected", "deselected")
    files = []
    status_code = Response(status=400)

    try:
        for i in request.files:
            files.append(i)
    except Exception:
        print("No Files")
        return status_code

    for i in files:
        if not allowed_files(i):
            print("Invalid Format")
            return status_code

    return redirect(url_for('confirm'))


@app.route("/confirm", methods=["GET"])
def confirm():
    g.states = ("deselected", "selected", "deselected")
    return render_template("confirm.html")


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if request.method == 'POST':
        return redirect(url_for('settings'))

    g.states = ("deselected", "deselected", "selected")
    return render_template("settings.html")


def allowed_files(file):
    # Add the checking of magic numbers (file signature)
    extensions = ["html", "css", "png", "svg", "jpg", "jpeg"]
    ext = file.split(".")[-1].lower()
    if ext not in extensions:
        return False
    return True


if __name__ == '__main__':
    app.run(debug=True)
