import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify, make_response, current_app, flash
from contextlib import closing
from flask_cors import CORS, cross_origin
import json 
from functools import update_wrapper

# configuration
DATABASE = os.path.join(os.getcwd(), '/home/renard/Desktop/virtualenv/venv/boatLinkDatabase/boatLinkDatabase.db')
JSON_PARAMETRES = os.path.join(os.getcwd(), '/home/renard/Desktop/virtualenv/venv/boatLinkDatabase/parametres.json')
JSON_STATUS = os.path.join(os.getcwd(), '/home/renard/Desktop/virtualenv/venv/boatLinkDatabase/key.json')
# Never leave debug mode activated in a production system, because it will allow users to execute code on the server!
DEBUG = True

# create our application
application = Flask(__name__)
application.config.from_object(__name__)
cors = CORS(application, resorces={r'/*': {"origins": '*'}})
def connect_db():
    """Connects to the specific database."""
    return sqlite3.connect(application.config['DATABASE'])


@application.before_request
def before_request():
    # without the try/except block, nginx will implode if there's an exception
    try:
        g.db = connect_db()
    except:
        print("Error connecting to db")



@application.teardown_request
def teardown_request(exception):
    try:
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()
    except:
        print("Error closing db")

@application.route('/')
def index():
    return render_template('index.html')


@application.route("/get-live-data",methods=['GET', 'POST'])
def live_data():
    con = connect_db()
    con.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    cur = con.cursor()
    cur.execute("SELECT * FROM envoiContinuT WHERE id = (SELECT MAX(id) FROM envoiContinuT);")
    recs = cur.fetchall()
    rows = [ dict(rec) for rec in recs ]
    rows_json = json.dumps(rows)
    return rows_json

@application.route("/get-init-data",methods=['GET', 'POST'])
def init_data():
    try:
        con = connect_db()
        con.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
        cur = con.cursor()
        cur.execute("SELECT * FROM envoiInitT WHERE id = (SELECT MAX(id) FROM envoiInitT);")
        recs = cur.fetchall()
        rows = [ dict(rec) for rec in recs ]
        rows_json = json.dumps(rows)
        return rows_json
    except:
        flash("Erreur survenue lors de la récupération de données")


@application.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

@application.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)

@application.route('/login', methods=['POST'])
def do_admin_login():
    try:
        con = connect_db()
        con.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
        cur = con.cursor()
        cur.execute("SELECT pseudo FROM adminT WHERE pseudo = ? AND password = ?", (request.form['username'], request.form['password']))
        if cur.fetchone() is None:
            flash("Nom d'utilisateur ou mot de passe incorrect")
            return render_template("login_page.html")
        else:
            session['logged_in'] = True
            return index() 
    except:
        flash("Erreur est survenue lors de la connexion")

@application.route('/add-admin',methods=['POST'])
def add_admin():
    if request.method == "POST":
        try:
            postdata = request.get_json(silent=True)
            con = connect_db()
            print("1")
            con.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
            cur = con.cursor()
            cur.execute("SELECT * FROM adminT WHERE pseudo = ? ", postdata['username'])
            print("2")
            if cur.fetchone() is None:
                print("3")
                cur.execute("INSERT INTO adminT (pseudo, password) VALUES (?,?)", (postdata['username'], postdata['password']))
                flash("L'administrateur a été ajouté avec succès")
                return render_template("admin_settings.html")
            else:
                flash("L'administrateur existe déjà")
        except:
            flash("Erreur survenue lors de l'ajout de l'administrateur ")
    print("4")
    return render_template("admin_settings.html") 


@application.route("/logout")
def logout():
    try:
        session['logged_in'] = False
        return index()
    except:
        flash("Erreur survenue lors de la déconnexion")

@application.route("/get-admin-data", methods=['GET', 'POST'])
def get_admin_data():
    try:
        if(session['logged_in'] == True):
            con = connect_db()
            con.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
            cur = con.cursor()
            cur.execute("SELECT pseudo FROM adminT;")
            recs = cur.fetchall()
            rows = [ dict(rec) for rec in recs ]
            rows_json = json.dumps(rows)
            return rows_json
        else:
            return index()
    except:
        flash("Erreur survenue lors de la récupération de données administrateurs")

@application.route("/get-stat-data",methods=['POST'])
def get_stat_data():
    if request.method == "POST":
        try:
            postdata = request.get_json(force=True)
            param = postdata['param']
            course = postdata['vitesse_bateau']
            con = connect_db()
            con.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
            cur = con.cursor()
            cur.execute("SELECT heure, minute, seconde, "+param+" FROM envoiContinuT WHERE vitesse_bateau = "+course+";")
            recs = cur.fetchall()
            rows = [dict(rec) for rec in recs ]
            rows_json = json.dumps(rows)
            print(rows_json)
            return rows_json
        except:
            flash("Erreur survenue lors de la récupération de données")
    return render_template('statistiques.html')

@application.route("/get-course-data",methods=['GET', 'POST'])
def get_course_data():
    if request.method == "GET":
        try:
            con = connect_db()
            con.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
            cur = con.cursor()
            cur.execute("SELECT DISTINCT vitesse_bateau FROM envoiContinuT")
            recs = cur.fetchall()
            rows = [dict(rec) for rec in recs ]
            rows_json = json.dumps(rows)
            return rows_json
        except:
            flash("Erreur survenue lors de la récupération des courses")
    return render_template('statistiques.html')


# Error handlers

@application.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(error), 400)

@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify(error), 404)

@application.errorhandler(500)
def server_error(error):
    return make_response(jsonify(error), 500)

def make_error(status_code, message, sub_code=None, action=None, **kwargs):
    """
    Error with custom message.
    """
    data = {
        'status': status_code,
        'message': message,
    }
    if action:
        data['action'] = action
    if sub_code:
        data['sub_code'] = sub_code
    data.update(kwargs)
    response = jsonify(data)
    response.status_code = status_code
    return response


if __name__ == "__main__":
    application.secret_key = os.urandom(12)
    application.run(host='160.98.31.214')

