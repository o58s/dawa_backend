from flask import Blueprint, request, jsonify
from models import Disease
from database import db

disease_bp = Blueprint("disease", __name__)

@disease_bp.route("/add_disease", methods = ["POST"])
def add_disease():
    data = request.get_json()
    disease = Disease(
        name = data["name"],
        icd_code = data["icd_code"],
        category = data["category"]
    )
    db.session.add(disease)
    db.session.commit()
    return jsonify({"message": "Disease added successfully"})