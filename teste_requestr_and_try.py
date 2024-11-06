import requests

url = 'localhost:5000/allpost'

def procurando_posts():
    try:
        r = requests.get(url, timeout=5)
        return  f'status code: {r.status_code}: requisição feita com sucesso! :)' if r.ok else f'status_code: {r.status_code}: Não foi porsivel completa a requisição. :('
    
    except requests.exceptions.InvalidSchema as error: 
       return "Erro HTTP ou HTTPS: Você precisa incluir métodos válidos.", error.args[0]

    except requests.exceptions.ReadTimeout as error: 
         return "HTTP Error" , error.args[0]

        

var = procurando_posts()
print(var)




