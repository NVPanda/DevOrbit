

class Cadastro:
    def __init__(self, name: str, last_name: str, email: str, age: int, password: str):
        self.name = name.capitalize()
        self.last_name = last_name
        self.email = email
        self.age = age
        self.password = password


class UserInformation: 
    def __init__(self, username, name, email, occupation):
        self.username = username
        self.name = name
        self.email = email
        self.occupation = occupation


class Login:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class Links:
    def __init__(self, github=None, likedin=None, site=None):
        self.github = github
        self.likedin = likedin
        self.site = site