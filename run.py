from application.src.__main__ import create_app  # Corrigido

app = create_app()

if __name__ == '__main__':
    app.run(port=8000)
