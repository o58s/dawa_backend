from flask import Blueprint, request, jsonify
from models import Prediction
from database import db

prediction_bp = Blueprint("prediction", __name__)

@prediction_bp.route("/prediction", methods = ["POST"])
def prediction():
    data = request.get_json()
    prediction = Prediction(
        search_id = data["search_id"],
        drug_id=data["drug_id"],
        disease_id=data["disease_id"],
        protein_id=data["protein_id"],
        confidence_score=data.get("confidence_score"),
        docking_score=data.get("docking_score"),
        mechanism_of_action=data.get("mechanism_of_action")

    )
    db.session.add(prediction)
    db.session.commit()
    return jsonify({"prediction_id": prediction.id})