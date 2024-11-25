# import os
# import aiosqlite
# from fastapi import APIRouter, File, UploadFile, HTTPException
# from pathlib import Path
# from dotenv import load_dotenv
# from flask import Flask

# # Carrega as variáveis de ambiente do .env
# load_dotenv()

# def comfig():
#     api = APIRouter()

#     @api.post("/uploadfile/{Iduser}/{file_name}")
#     async def upload_file(Iduser: int, file_name: str, file: UploadFile = File(...)):
#         # Caminho onde as fotos serão salvas
#         upload_path = Path("uploads")
#         upload_path.mkdir(parents=True, exist_ok=True)  # Cria a pasta caso não exista

#         # Verifica se o arquivo enviado é uma imagem (por exemplo, png, jpg, jpeg)
#         if file.content_type not in ["image/png", "image/jpeg"]:
#             raise HTTPException(status_code=400, detail="Invalid file type. Only PNG and JPEG are allowed.")

#         # Salva o arquivo com o nome fornecido
#         file_path = upload_path / file_name
#         with open(file_path, "wb") as f:
#             f.write(await file.read())

#         # Atualiza o banco de dados
#         async with aiosqlite.connect(os.getenv("BANCO_DB")) as banco:
#             async with banco.cursor() as cursor:
#                 # Verifica se o usuário existe no banco de dados
#                 cursor.execute("SELECT id FROM usuarios WHERE id = ?", (Iduser,))
#                 user = await cursor.fetchone()

#                 if user is None:
#                     raise HTTPException(status_code=404, detail="User not found")

#                 # Atualiza o campo "photo" do usuário
#                 cursor.execute("UPDATE usuarios SET photo = ? WHERE id = ?", (str(file_path), Iduser))
#                 await banco.commit()

#         return {"message": "File uploaded successfully", "file_path": str(file_path)}

#     return api
