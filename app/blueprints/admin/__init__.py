# File controling the admin routes

from flask import ( Blueprint, render_template )

ADMIN_BP = Blueprint("admin", __name__, url_prefix="/admin")

@ADMIN_BP.get("/")
@ADMIN_BP.get("/home")
def admin_home():
    '''
    The admin dahsboard home page route handler.
    '''
    return render_template("/admin/home.jinja2")