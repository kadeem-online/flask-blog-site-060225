# Central location for extensions used by the flask app.

from flask_login import ( LoginManager )

# admin pages login manager
login_manager = LoginManager()
login_manager.login_view = 'admin.admin_login'