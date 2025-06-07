from flask import Blueprint, render_template, request, Response, redirect, url_for
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
    message = None
    if request.method == "POST":
        peer_name = request.form.get("peer_name")
        if peer_name:
            wg.add_peer(peer_name)
            message = f"Peer '{peer_name}' added successfully."
    return render_template("index.html", message=message)

