import sqlite3
import os

def get_db_connection():
    return sqlite3.connect('FeedDatabase.db')

def initialize_posts_schema():
    # Inicializa a tabela de posts, se ainda não existir
    banco = get_db_connection()
    cursor = banco.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            post_img TEXT
        )
        """
    )
    banco.commit()
    banco.close()

def create_post(nome, post_img):
    # Insere um post no banco de dados
    banco = get_db_connection()
    cursor = banco.cursor()
    cursor.execute("""
        INSERT INTO posts(nome, post_img) VALUES(?, ?)
    """, (nome, post_img))
    banco.commit()
    banco.close()
