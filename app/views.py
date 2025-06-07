from flask import Blueprint, render_template, request, Response, redirect, url_for, jsonify
from . import wg
import config

main = Blueprint("main", __name__)

def check_auth(username, password):
    return username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD

def authenticate():
    return Response(
        "Authentication required", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

@main.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@main.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")

@main.route("/peers", methods=["GET", "POST"])
def peers():
    return render_template("peers.html")

@main.route("/add", methods=["GET", "POST"])
def new_peer():
    message = None
    if request.method == "POST":
        name = request.form["name"]
        ip = request.form["ip"]
        if name:
            metadata, success = wg.add_peer(name, ip)
            if success:
                message = f"Peer '{name}' added successfully."
            else:
                message =f"IP '{ip}' already exists!"
                
    return render_template("new_peer.html", message=message)

@main.route("/api/peers")
def get_peers():
    peers = []
    return jsonify(peers)