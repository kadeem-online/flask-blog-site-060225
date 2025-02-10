# This file contains seeding functions

import click

# main database instance
from app.database import (database)
from faker import (Faker)
from flask import (Flask, current_app)
from flask_sqlalchemy import (SQLAlchemy)
from typing import (List)

# models
from app.database.models import (Post, PostStatusEnum, User, UserRoleEnum)

class BlogZeroSeeder():

    def __init__(self, database: SQLAlchemy):
        self.database = database
        self.fake = Faker()
        return

    def init_app(self, app: Flask):
        '''
        Initialize the seeder within a specific flask application instance context.
        '''
        app.cli.add_command(self.seed_commands)
        return self

    def test_output(self):
        '''Use to test if the seeder methods can be run on the cli.'''
        print(f"I can seed a dummy uuid: {self.fake.uuid4()}")
        return
    
    def _create_user( 
        self,
        user_name:str|None = None,
        pass_phrase:str|None = None,
        email:str|None = None,
        role:UserRoleEnum|None = None,
    ):
        '''
        Creates a new User object.
        '''
        _username = user_name if user_name else self.fake.user_name()
        _password = pass_phrase if pass_phrase else "1234"
        _hashed_password = User.hash_user_password(_password)
        _email = email if email else self.fake.email()
        _role = role if role else self.fake.random_element(elements=list(UserRoleEnum))

        # GUARD: check if a record with the username exists
        if User.query.filter_by(username=_username).first():
            print(f"User with the username: '{_username}' already exists.")
            return None

        # GUARD: check if a record with the email exists
        if User.query.filter_by(email=_email).first():
            print(f"User with the email: '{_email}' already exists.")
            return None
        
        # create the user
        _user = User(
            username=_username,
            password_hash=_hashed_password,
            email=_email,
            role=_role
        )

        # save the user in the database
        self.database.session.add(_user)
        self.database.session.commit()

        # return the user
        return _user

    @click.group("seed")
    def seed_commands():
        '''
        Seed commands for Blog Zero
        '''
        pass

    @seed_commands.command("admin")
    def seed_admin_account():
        '''
        Seeds the default 'admin' user, with the default password of '1234'
        '''
        _seeder = BlogZeroSeeder(current_app.extensions['sqlalchemy'])
        _admin = _seeder._create_user(
            "admin",
            "1234",
            "admin@blog-zero.com",
            UserRoleEnum.EDITOR
        )

        if _admin is None:
            print("Admin record already exists")
        else:
            print("Admin record created successfully")
        return

    @seed_commands.command("content")
    def seed_default_content():
        '''
        Generates dummy content for the site.
        '''
        print("Generate dummy content for blog zero here.")
        return
