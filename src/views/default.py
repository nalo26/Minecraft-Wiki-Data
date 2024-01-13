from flask import Blueprint, redirect, request, url_for

view = Blueprint("default", __name__)


@view.route("/favicon.ico")
@view.route("/robots.txt")
def static_from_root():
    return redirect(url_for("static", filename=request.path[1:]))


@view.route("/")
def index():
    return "Main page"  # TODO
