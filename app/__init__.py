import os

from .blueprints.root import ( ROOT_BP )
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
        VITE_DEV_SERVER = os.environ.get("VITE_DEV_SERVER")
    )

    # register the root blueprint
    _app.register_blueprint(ROOT_BP)
    

    # return the app instance
    return _app

if __name__ == "__main__":
    _app = create_app()
    _app.run()