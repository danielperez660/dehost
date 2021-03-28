from flask import Flask, render_template, request, redirect, url_for, g, Response, session
from database_manager import DBManager
from skynet_manager import SkyManager

import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "d16683620814b0fc868c47c6ff3195b5"
app.config['UPLOAD_FOLDER'] = "temp/"
app.config['MAX_CONTENT_PATH'] = 16 * 16 * 1024

DB = DBManager()
sia = SkyManager()
files = []


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
    global files
    files = []
    g.states = ("deselected", "selected", "deselected")
    status_code = Response(status=400)

    try:
        for i in request.files:
            files.append(request.files[i])
            request.files[i].save(os.path.join("temp", secure_filename(i)))
    except Exception as e:
        print(e)
        return status_code

    for i in files:
        if not allowed_files(i.filename):
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
        chain_link = uploader(chain)
        link = "test"

        if chain_link:
            DB.add_website(name, session['username'], chain, link, chain_link)
        else:
            redirect(url_for(page_not_found))

        return redirect(url_for("index"))


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if request.method == 'POST':
        return redirect(url_for('settings'))

    g.states = ("deselected", "deselected", "selected")
    return render_template("settings.html")


@app.route('/<name>', methods=["GET"])
def site(name):
    url = DB.find_website_name(name)
    print(url)
    # downloader(url)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


def allowed_files(file):
    # Add the checking of magic numbers (file signature)
    # TODO: maybe add a flash if disallowed filetypes
    # TODO: Add a flash if no index.html is found

    extensions = ["html", "css", "png", "svg", "jpg", "jpeg", "js"]
    ext = file.split(".")[-1].lower()
    if ext not in extensions:
        return False
    return True


def uploader(chain):
    link = None

    if chain == "Sia":
        print("Uploading to Sia")

        if len(files) == 1:
            link = sia.submit_file(file=files[0])
            # Add response for waiting to upload
        elif len(files) == 0:
            return None
        else:
            link = sia.submit_folder(folder=files)

    elif chain == "IPFS":
        print("Uploading to IPFS")

    return link


def downloader(url):
    return sia.fetch_file(url)


if __name__ == '__main__':
    app.run(debug=True)
