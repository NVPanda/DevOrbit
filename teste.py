import sqlite3
from flask_login import current_user

class Post:
    def __init__(self, titulo, post, post_img):
        self.user_id = current_user.id  # ID do usuário logado
        self.nome = current_user.username  # Nome do usuário logado
        self.titulo = titulo
        self.post = post
        self.post_img = post_img

    @staticmethod
    def get_db_connection():
        """Conecta ao banco de dados."""
        return sqlite3.connect('feedDatabase.db')

    def save_to_db(self):
        """Salva o post no banco de dados."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Executa o comando SQL para inserir os dados no banco
            cursor.execute(
                """
                INSERT INTO posts (user_id, nome, titulo, post, post_img) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (self.user_id, self.nome, self.titulo, self.post, self.post_img)
            )
            conn.commit()
            print("Post salvo no banco de dados com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao salvar post no banco de dados: {e}")
            raise
        finally:
            conn.close()
