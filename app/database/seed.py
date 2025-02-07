# This file contains seeding functions

# main database instance
from app.database import ( database )

# models
from app.database.models.user import ( User, UserRoleEnum, hash_user_password )

def seed_default_admin():
    '''
    Creates the default user to be added to the database.
    '''
    _username = "admin"
    _password = "1234"
    _hashed_password = hash_user_password(_password)
    _email = "admin@blog-zero.com"
    _role = UserRoleEnum.EDITOR

    # GUARD: create the record if it does not exist
    if not User.query.filter_by(username=_username).first():
        # create the default user
        _default_user = User(
            username=_username,
            password_hash=_hashed_password,
            email=_email,
            role=_role
        )

        #save the default user
        database.session.add(_default_user)
        database.session.commit()
    
    return
    