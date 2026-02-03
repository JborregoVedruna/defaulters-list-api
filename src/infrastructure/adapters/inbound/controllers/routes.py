from flask import Blueprint, request, jsonify
from src.application.mediator import Mediator
from src.application.commands.save_debt import SaveDebtCommand
from src.application.queries.get_debts import GetDebtsQuery
from src.application.queries.get_debts_by_dni import GetDebtsByDniQuery
from src.domain.models.debt import Debt
from src.domain.models.pagination import Pageable
from pydantic import ValidationError

def create_debt_blueprint(mediator: Mediator) -> Blueprint:
    bp = Blueprint("debts", __name__)

    @bp.route("/", methods=["POST"])
    def save_debt():
        try:
            debt_data = request.get_json()
            debt = Debt(**debt_data)
            command = SaveDebtCommand(debt=debt)
            result = mediator.send(command)
            return jsonify(result.model_dump()), 201
        except ValidationError as e:
            return jsonify(e.errors()), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @bp.route("/", methods=["GET"])
    def get_debts():
        try:
            page = int(request.args.get("page", 0))
            size = int(request.args.get("size", 10))
            sort = request.args.get("sort", "uuid")
            
            pageable = Pageable(page=page, size=size, sort=sort)
            query = GetDebtsQuery(pageable=pageable)
            result = mediator.send(query)
            
            return jsonify(result.model_dump()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @bp.route("/dni/<debtor_dni>", methods=["GET"])
    def get_debts_by_dni(debtor_dni):
        try:
            page = int(request.args.get("page", 0))
            size = int(request.args.get("size", 10))
            sort = request.args.get("sort", "uuid")
            
            pageable = Pageable(page=page, size=size, sort=sort)
            query = GetDebtsByDniQuery(debtor_dni=debtor_dni, pageable=pageable)
            result = mediator.send(query)
            
            return jsonify(result.model_dump()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return bp
