import sqlite3
from flask_login import UserMixin

class Cadastro:
    def __init__(self, name: str, last_name: str, email: str, age: int, password: str):
        self.name = name.capitalize()
        self.last_name = last_name
        self.email = email
        self.age = age
        self.password = password

class Login:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

def my_db():
    banco = sqlite3.connect('usuarios.db')
    return banco, banco.cursor()

def create_database():
    banco, cursor = my_db()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        password TEXT NOT NULL,
        photo TEXT DEFAULT '/home/lansvx/criativacao/application/src/static/uploads/1_20241124191119.jpg'
        
        )'''
    )
    banco.commit()
    banco.close()

def add_user(user: Cadastro):
    banco, cursor = my_db()
    try:
        cursor.execute('''
        INSERT INTO usuarios (name, last_name, email, age, password) values (?,?,?,?,?)''',
        (user.name, user.last_name, user.email, user.age, user.password))
        banco.commit()
    except sqlite3.IntegrityError:
        return 'Email já cadastrado', None
    finally:
        banco.close()

def check_user_login(login: Login):
    banco, cursor = my_db()
    cursor.execute('''
    SELECT id, name FROM usuarios WHERE email = ? AND password = ?''',
    (login.email, login.password))
    user = cursor.fetchone()
    banco.close()
    

    if user:
        return True, user[0], user[1]  # Retorne o ID e o nome do usuário
    else:
        return False, None, None  # Retorne False se o usuário não for encontrado

# Função para adicionar a coluna 'bio' se não existir
def add_column():
    banco, cursor = my_db()
    
    # Verifica se a coluna 'bio' já existe
    cursor.execute("PRAGMA table_info(usuarios)")
    columns = [column[1] for column in cursor.fetchall()]  # Obtém todos os nomes das colunas

    if 'bio' not in columns:
        # Adiciona a coluna 'bio' à tabela 'usuarios'
        cursor.execute("ALTER TABLE usuarios ADD COLUMN bio TEXT")
        banco.commit()
        print("Coluna 'bio' adicionada com sucesso.")
    else:
       pass

    banco.close()

class User(UserMixin):
    def __init__(self, user_id: str, username: str):
        self.id = user_id
        self.username = username

    @staticmethod
    def get(user_id):
        banco, cursor = my_db()
        cursor.execute('SELECT id, name FROM usuarios WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        banco.close()
        if user:
            return True, (user[0], user[1])
        return None 
