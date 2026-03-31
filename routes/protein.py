from flask import Blueprint, request, jsonify
from models import Protein
from database import db

protein_bp = Blueprint("protein", __name__)

@protein_bp.route("/add_protein", methods = ["POST"])
def add_protein():
    data = request.get_json()
    protein = Protein(
        name = data["name"],
        uniprot_id = data["uniprot_id"],
        gene_name = data["gene_name"],
        sequence = data["sequence"]
    )
    db.session.add(protein)
    db.session.commit()
    return jsonify({"message": "Protein added successfully"})