from flask import Blueprint, request, jsonify
from models import SearchHistory
from database import db

search_bp = Blueprint("search", __name__)

@search_bp.route("/search", methods = ["POST"])
def search():
    data = request.get_json()
    search = SearchHistory(
        user_id = data["user_id"],
        input_value = data["input_value"],
        input_type = data["input_type"]
    )
    db.session.add(search)
    db.session.commit()
    return jsonify({"search_id": search.id})
