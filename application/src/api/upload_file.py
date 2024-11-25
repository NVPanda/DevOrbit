import os
from flask import Flask, request, send_from_directory
from flask_restx import Api, Namespace, Resource, fields
import sqlite3
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

# Caminho onde as imagens serão salvas
caminho_img = 'application/src/static/fotos'
os.makedirs(caminho_img, exist_ok=True)
# Namespace para as rotas
api = Namespace('files', description='Operações com arquivos', path='/files')

# Modelo para a resposta de upload
upload_model = api.model('UploadResponse', {
    'filename': fields.String(description='Nome do arquivo', example='example.jpg'),
    'content_type': fields.String(description='Tipo de conteúdo', example='image/jpeg'),
    'size': fields.Integer(description='Tamanho do arquivo em bytes', example=1234),
    'user_id': fields.Integer(description='ID do usuário associado', example=1)
})
@api.route('/uploadfile/<int:user_id>')  # Aqui o tipo int é explicitado
class UploadFile(Resource):
    @api.expect(api.parser().add_argument('file', type='file', location='files'))
    @api.response(200, 'Success', upload_model)
    def post(self, user_id):
        """
        Realiza o upload de um arquivo e associa ao usuário pelo ID.
        """
        uploaded_file = request.files.get('file')
        
        # Verifica se o arquivo foi enviado
        if not uploaded_file:
            return {"error": "Nenhum arquivo enviado"}, 400

        # Conectar ao banco e verificar se o usuário existe
        conn = sqlite3.connect(os.getenv("BANCO_DB"))
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM usuarios WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if user is None:
            conn.close()
            return {"error": "Usuário não encontrado"}, 404

        # Define o caminho relativo da imagem
        relative_file_path = os.path.join('fotos', uploaded_file.filename)  # Ex: 'fotos/foto.jpg'

        # Salva o caminho relativo no banco de dados
        cursor.execute("UPDATE usuarios SET photo = ? WHERE id = ?", (relative_file_path, user_id))
        conn.commit()

        # Salva o arquivo no diretório de uploads
        file_path = os.path.join(caminho_img, uploaded_file.filename)
        uploaded_file.save(file_path)

        conn.close()

        return {
            "filename": uploaded_file.filename,
            "content_type": uploaded_file.content_type,
            "size": os.path.getsize(file_path),
            "user_id": user_id
        }, 200

@api.route('/<int:user_id>', endpoint='get_file')
class GetFile(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'File not found')
    def get(self, user_id):
        """
        Retorna a imagem do usuário pelo ID.
        """
        conn = sqlite3.connect(os.getenv("BANCO_DB"))
        cursor = conn.cursor()

        cursor.execute("SELECT photo FROM usuarios WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user is None or user[0] is None:
            return {"error": "User not found or no photo available"}, 404

        # Caminho relativo da imagem
        relative_file_path = user[0]

        # Verificar se o arquivo realmente existe no diretório
        if not os.path.exists(os.path.join(caminho_img, relative_file_path)):
            return {"error": "File not found"}, 404

        # Garantir que o caminho seja acessível e retorne o arquivo corretamente
        return send_from_directory(os.path.join(caminho_img), relative_file_path)




def register_file_routes(api_instance: Api):
    """
    Função para registrar o namespace no objeto principal da API.
    """
    api_instance.add_namespace(api)
