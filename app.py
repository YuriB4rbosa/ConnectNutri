from flask import Flask
import os
from dotenv import load_dotenv
from database import criar_tabelas
from controllers.routes import configurar_rotas

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'chave-provisoria-segura')

configurar_rotas(app)


if __name__ == '__main__':
    with app.app_context():
        criar_tabelas()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)