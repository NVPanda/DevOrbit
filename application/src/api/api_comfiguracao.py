# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# from dotenv import load_dotenv
# from datetime import datetime
# import sqlite3
# import os

# load_dotenv()

# fastapi_app = FastAPI()
# caminho_img = 'application/src/static/fotos'
# os.makedirs(caminho_img, exist_ok=True)


# # Configuração do CORS
# fastapi_app.add_middleware(
#     CORSMiddleware,
#    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],

#     allow_credentials=True,
#     allow_methods=["*"],  # Permite todos os métodos HTTP
#     allow_headers=["*"],  # Permite todos os cabeçalhos
# )

# @fastapi_app.post("/banner/uploadfile/{user_id}")

# async def upload_banner(user_id: int, file: UploadFile = File(...)):
#     if not file:
#         return JSONResponse({"error": "Arquivo não enviado"}, status_code=400)
    
#     conn = sqlite3.connect(os.getenv("BANCO_DB"))
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM usuarios WHERE id = ?", (user_id,))
#     user = cursor.fetchone()
    
#     if not user:
#         return JSONResponse({"error": "Usuário não encontrado"}, status_code=404)
    
#     ext = os.path.splitext(file.filename)[1]
#     banner_filename = f"banner_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
#     relative_file_path = os.path.join("fotos", banner_filename)
#     banner_path = os.path.join(caminho_img, banner_filename)
    
#     with open(banner_path, "wb") as f:
#         f.write(await file.read())
    
#     cursor.execute(
#         "UPDATE usuarios SET banner = ? WHERE id = ?", 
#         (relative_file_path, user_id)
#     )
#     conn.commit()
#     conn.close()
    
#     return {
#         "result": 200,
#         "filename": banner_filename,
#         "content_type": file.content_type,
#         "size": os.path.getsize(banner_path),
#         "user_id": user_id,
#         "banner_url": f"http://127.0.0.1:5000/files/{banner_filename}"
#     }, 200
             

# @fastapi_app.get("/api")
# async def read_root():
#        return {"mesagem": "Hello World"}
