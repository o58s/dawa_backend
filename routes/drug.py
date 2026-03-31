from flask import Blueprint, request, jsonify
from models import Drug
from database import db

drug_bp = Blueprint("drug", __name__)

@drug_bp.route("/add_drug", methods = ["POST"])
def add_drug():
    data = request.get_json()
    drug = Drug(
        
        name = data["name"],
        smiles = data["smiles"],
        formula = data["formula"],
        molecular_weight = data["molecular_weight"],
        status = data["status"],
        original_indication = data["original_indication"]
    )
    db.session.add(drug)
    db.session.commit()
    return jsonify({"message": "Drug added successfully"})
