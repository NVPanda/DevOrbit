import os
from flask import Flask, request, send_from_directory
from flask_restx import Api, Namespace, Resource, fields

# Diretório de upload
UPLOAD_DIR = os.path.abspath("application/src/static/uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Namespace para as rotas
api = Namespace('files', description='Operações com arquivos', path='/files')  # Aqui especificamos o path para a URL correta

# Modelo para a resposta de upload
upload_model = api.model('UploadResponse', {
    'filename': fields.String(description='Nome do arquivo', example='example.txt'),
    'content_type': fields.String(description='Tipo de conteúdo', example='text/plain'),
    'size': fields.Integer(description='Tamanho do arquivo em bytes', example=1234),
})

@api.route('/uploadfile/')
class UploadFile(Resource):
    @api.expect(api.parser().add_argument('file', type='file', location='files'))
    @api.response(200, 'Success', upload_model)
    def post(self):
        """
        Realiza o upload de um arquivo.
        """
        uploaded_file = request.files.get('file')  # Mudança aqui
        if not uploaded_file:
            return {"error": "Nenhum arquivo enviado"}, 400

        file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
        uploaded_file.save(file_path)

        return {
            "filename": uploaded_file.filename,
            "content_type": uploaded_file.content_type,
            "size": os.path.getsize(file_path),
        }, 200

@api.route('/<string:file_name>')  # Corrigido para a rota sem duplicação
class GetFile(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'File not found')
    def get(self, file_name):
        """
        Retorna um arquivo pelo nome.
        """
        file_path = os.path.join(UPLOAD_DIR, file_name)
        print(f"Verificando o arquivo em: {file_path}")  # Adicionado para debug
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            return {"error": "File not found"}, 404

        # Retornar o arquivo do diretório de upload
        return send_from_directory(UPLOAD_DIR, file_name)


def register_file_routes(api_instance: Api):
    """
    Função para registrar o namespace no objeto principal da API.
    """
    api_instance.add_namespace(api)


