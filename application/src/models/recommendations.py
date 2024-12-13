from dotenv import load_dotenv
import os
import sqlite3
import random


# Carregar variáveis de ambiente
load_dotenv()



# Função para formatar nomes de usuários
def format_user_name(full_name):
    # Divide o nome completo em palavras
    name_parts = full_name.split()
    
    # Pega o primeiro nome, ou um valor padrão se o nome estiver vazio
    if name_parts:
        first_name = name_parts[0]
    else:
        return "Usuário"

    # Limita o comprimento do nome (por exemplo, no máximo 10 caracteres)
    max_length = 10
    if len(first_name) > max_length:
        return first_name[:max_length] + "..."  # Trunca nomes longos
    return first_name

# Pegar todos os usuários e mostrar 0-10 no front como recomendação
def recommendationsUser():
    db_path = os.getenv('BANCO_DB', 'usuarios.db')  # Obtém o caminho do banco de dados
    try:
        # Conecta ao banco de dados
        banco = sqlite3.connect(db_path)
        cursor = banco.cursor()

        limit = random.randint(2,4)
      

        # Busca os primeiros 10 usuários da tabela
        cursor.execute(f"SELECT * FROM usuarios LIMIT {limit}")
        users = cursor.fetchall()

        # Formata os dados para exibição
        recommendations = []
        for user in users:
            recommendations.append({
                "id": user[0],       
                "name": format_user_name(user[2]),  
                "user_photo": user[7] if user[7] else None
                
            })
        
        random.shuffle(recommendations)
            

        # Retorna os dados formatados
        return recommendations

    except Exception as e:
        print(f"Erro ao buscar os usuários: {e}")
        return []
    finally:
        banco.close()  # Sempre feche a conexão ao terminar

