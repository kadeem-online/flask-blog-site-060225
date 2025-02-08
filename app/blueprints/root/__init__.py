# This blueprint manages the base routes available to the public.

from flask import ( Blueprint, render_template )

ROOT_BP = Blueprint('root', __name__)

@ROOT_BP.route("/")
def index():
    return render_template("root/index.jinja2")