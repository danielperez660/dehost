from flask import Flask, render_template, request, redirect, url_for, g, Response, session
from database_manager import DBManager
from skynet_manager import SkyManager

app = Flask(__name__)
app.secret_key = "d16683620814b0fc868c47c6ff3195b5"
DB = DBManager()
sia = SkyManager()


@app.route('/', methods=["POST", "GET"])
@app.route('/sites', methods=["POST", "GET"])
def index():
    session['username'] = "admin"

    if request.method == 'POST':
        return redirect(url_for('index'))

    g.states = ("selected", "deselected", "deselected")
    sites_list = DB.find_websites_for(session['username'])
    return render_template("main_console.html", sites_list=sites_list)


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


@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    g.states = ("deselected", "selected", "deselected")
    if request.method == "GET":
        return render_template("confirm.html")
    elif request.method == "POST":
        name = request.form['name']
        chain = request.form['chain']
        link = uploader(chain)

        DB.add_website(name, session['username'], chain, link)

        return redirect(url_for("index"))


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if request.method == 'POST':
        return redirect(url_for('settings'))

    g.states = ("deselected", "deselected", "selected")
    return render_template("settings.html")


def allowed_files(file):
    # Add the checking of magic numbers (file signature)
    extensions = ["html", "css", "png", "svg", "jpg", "jpeg", "js"]
    ext = file.split(".")[-1].lower()
    if ext not in extensions:
        return False
    return True


def uploader(chain):
    link = "SomeFuckingLink idk"

    if chain == "Sia":
        print("Uploading to Sia")
        # sia.submit_file(file="this is a file")
    elif chain == "IPFS":
        print("Uploading to IPFS")

    return link


if __name__ == '__main__':
    app.run(debug=True)
