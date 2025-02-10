import os

from app.blueprints import ( ADMIN_BP, ROOT_BP )
from app.database import ( database, migrate )
from app.database.models import ( User, Post )
from app.extensions import ( login_manager )
from dotenv import ( load_dotenv )
from flask import ( Flask, render_template )

# load env variables
load_dotenv()

def create_app():
    '''
    Returns an instance of a flask application containing Blog Zero
    '''

    # create Flask instance
    _app = Flask(__name__)

    # check dev variables
    _is_dev_mode = False
    try:
        if( os.environ.get("FLASK_MODE") == "development" ):
            _is_dev_mode = True

            # ensure the vite server is set
            if( os.environ.get("VITE_DEV_SERVER") is None ):
                _message = (
                    "A VITE_DEV_SERVER URL is required if running the project in development mode. "
                    "Please set the required env variable before restarting the server."
                )
                raise Exception(_message)
                
    except Exception as error:
        print(f"**VITE DEV SERVER ERROR: {error}\n")
        raise error

    # configure the application
    _app.config.from_mapping(
        IS_DEV=_is_dev_mode,
        VITE_DEV_SERVER = os.environ.get("VITE_DEV_SERVER"),
        SECRET_KEY= os.environ.get("SECRET_KEY", "dev-secret-key"),

        # Check if a database has been set if none default to sqlite db
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "sqlite:///blog_zero.db")
    )

    # GUARD: ensure the instance folder exists
    try:
        os.makedirs(_app.instance_path)
    except OSError:
        pass

    # connect the app to the database
    database.init_app(_app)

    # connect the migration utility
    migrate.init_app(_app, database)

    # connect the login manager
    login_manager.init_app(_app)

    # register the root blueprint
    _app.register_blueprint(ROOT_BP)

    # register the root blueprint
    _app.register_blueprint(ADMIN_BP)

    # return the app instance
    return _app

if __name__ == "__main__":
    _app = create_app()
    _app.run()