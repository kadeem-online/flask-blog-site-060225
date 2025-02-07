# This file manages the SQLAchemy instance for 'Blog Zero'

from flask_migrate import ( Migrate )
from flask_sqlalchemy import ( SQLAlchemy)

# Main connection to the database
database = SQLAlchemy()

# Migration utility
migrate = Migrate()