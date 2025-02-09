# File controling the admin routes

from app.database import ( database )
from app.database.models import ( User )
from app.forms import ( AdminLoginForm )
from flask import ( Blueprint, redirect, render_template, url_for )
from flask_login import ( login_required, login_user, logout_user )
from sqlalchemy import ( select )

ADMIN_BP = Blueprint("admin", __name__, url_prefix="/admin")

@ADMIN_BP.get("/")
@ADMIN_BP.get("/home")
@login_required
def admin_home():
    '''
    The admin dahsboard home page route handler.
    '''
    return render_template("/admin/home.jinja2")

@ADMIN_BP.get("/login")
def admin_login():
    '''
    The admin login page route GET handler.
    '''

    _adminLoginForm = AdminLoginForm()
    return render_template("admin/login.jinja2", adminLoginForm=_adminLoginForm)

@ADMIN_BP.post("/login")
def admin_login_post():
    '''
    The admin login page route POST handler.
    '''
    _adminLoginForm = AdminLoginForm()

    # GUARD: ensure form validation.
    if _adminLoginForm.validate_on_submit() == False:
        return render_template("admin/login.jinja2", adminLoginForm = _adminLoginForm)
    
    # Verify the an account with the username exists
    _user = User.query.filter_by(username=_adminLoginForm.name.data).first()

    # GUARD: handle none existing account
    if _user is None:
        _adminLoginForm.name.errors.append('The username you entered is not connected to any account.')
        return render_template("admin/login.jinja2", adminLoginForm = _adminLoginForm)
    
    # GUARD: handle invlaid credentials
    if User.verify_user_password(_user.password_hash, _adminLoginForm.password.data) is False:
        _adminLoginForm.name.errors.append('Invalid credentials.')
        return render_template("admin/login.jinja2", adminLoginForm = _adminLoginForm)
    
    # sign in the user and redirect to the admin homepage.
    login_user(_user)
    return redirect( url_for("admin.admin_home") )

@ADMIN_BP.route("/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))