from flask_sqlalchemy import SQLAlchemy
from application.src.__main__ import db

class Cadastro:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email




class Usuarios(db.Model):
    pass