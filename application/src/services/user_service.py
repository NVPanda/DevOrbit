from flask import flash, redirect, url_for
from application.src.database.users.configure_users import my_db


def get_user_info(usuario): # This function receives current.username
    banco, cursor = my_db()
    
    # Fetching all the user's information from the database
    cursor.execute(
        'SELECT id, photo, bio, github, likedin, site, followers, following, banner, name FROM usuarios WHERE name = ?',
        (usuario,)
    )
    user = cursor.fetchone()

    if not user:
        flash('Usuário não encontrado.', 'error')
        return None  # caso o usuário não seja encontrado

    # Directly return a dictionary list with the information
    return [{
        'user_photo': user[1],
        'bio': user[2],
        'github': user[3],
        'linkedin': user[4],
        'site': user[5],
        'followers': user[6],
        'following': user[7],
        'banner': user[8],
        'username': user[9]
    }]

    

def UserData(usuario): # This function receives current_user.id:
    banco, cursor = my_db()
    
    # Fetch the logged-in user's information:
    cursor.execute(
        'SELECT id, username,  occupation FROM user_information WHERE id = ?',
        (usuario,)
    )
    user = cursor.fetchone()
   
    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('home.home_page'))  # Redireciona caso o usuário não seja encontrado

     # Directly return a dictionary list with the information
    return [{
        'id': user[0],
        'username': user[1],
        'occupation': user[2]
        
    }]

