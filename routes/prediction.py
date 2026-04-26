from flask import Blueprint, request, jsonify
from models import SearchHistory
from database import db
from predictor import Predictor

prediction_bp = Blueprint("prediction", __name__)

predictor = Predictor("artifacts")

@prediction_bp.route("/predict", methods=["POST"])
def predict():
    data      = request.get_json()
    drug_name = data.get("drug_name", "").strip()
    user_id   = data.get("user_id")
    top_k     = data.get("top_k", 20)

    if not drug_name:
        return jsonify({"error": "drug_name is required"}), 400

    results, error = predictor.predict_for_drug(drug_name, top_k=top_k)
    if error:
        return jsonify({"error": error}), 404

    # Log search history
    search = SearchHistory(
        user_id=user_id,
        input_value=drug_name,
        input_type="drug_name"
    )
    db.session.add(search)
    db.session.flush()
    db.session.commit()

    return jsonify({
        "drug":        drug_name,
        "search_id":   search.id,
        "predictions": results
    })
