from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



import os
from dotenv import load_dotenv


load_dotenv()
class Server:
    def __init__(self):
        api = FastAPI(
           title="API-DevOrbit",
           version='1.0.0'
        )

        UPLOAD_DIR = "/tmp/uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        #base_url = "https://api-devorbirt.onrender.com/files/"

        api.add_middleware(
            CORSMiddleware,
        allow_origins=[
            
            "http://127.0.0.1:5000",
            "http://localhost:5000", # TEST
            "http://127.0.0.1:5000/devorbit/feed/"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

server = Server()