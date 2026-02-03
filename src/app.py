import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

from src.application.mediator import Mediator
from src.application.commands.save_debt import SaveDebtCommand, SaveDebtHandler
from src.application.queries.get_debts import GetDebtsQuery, GetDebtsHandler
from src.application.queries.get_debts_by_dni import GetDebtsByDniQuery, GetDebtsByDniHandler
from src.infrastructure.adapters.outbound.mongo_debt_repository import MongoDebtRepository
from src.infrastructure.adapters.inbound.controllers.routes import create_debt_blueprint

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Dependencies
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("MONGO_DB_NAME", "caixabank_debts")
    
    client = MongoClient(mongo_uri)
    repository = MongoDebtRepository(client, db_name)

    # Mediator setup
    mediator = Mediator()
    
    # Handlers registration (Manual DI)
    save_debt_handler = SaveDebtHandler(repository)
    get_debts_handler = GetDebtsHandler(repository)
    get_debts_by_dni_handler = GetDebtsByDniHandler(repository)
    
    mediator.register_handler(SaveDebtCommand, save_debt_handler)
    mediator.register_handler(GetDebtsQuery, get_debts_handler)
    mediator.register_handler(GetDebtsByDniQuery, get_debts_by_dni_handler)

    # Register Blueprints
    app.register_blueprint(create_debt_blueprint(mediator), url_prefix="/api/v1/debts")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=int(os.getenv("PORT", "5000")))