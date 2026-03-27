from database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Drug(db.Model):
    __tablename__ = "drugs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    smiles = db.Column(db.Text)
    formula = db.Column(db.String(100))
    molecular_weight = db.Column(db.Float)
    status = db.Column(db.String(50))  
    original_indication = db.Column(db.Text)


class Disease(db.Model):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    icd_code = db.Column(db.String(20), unique=True)
    category = db.Column(db.String(100))


class Protein(db.Model):
    __tablename__ = "proteins"

    id = db.Column(db.Integer, primary_key=True)
    uniprot_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    gene_name = db.Column(db.String(100))
    sequence = db.Column(db.Text)


class SearchHistory(db.Model):
    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    input_value = db.Column(db.Text, nullable=False)
    input_type = db.Column(db.String(50))  
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("searches", cascade="all, delete-orphan"))


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey("search_history.id", ondelete="CASCADE"), nullable=False)
    drug_id = db.Column(db.Integer, db.ForeignKey("drugs.id", ondelete="CASCADE"), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False)
    protein_id = db.Column(db.Integer, db.ForeignKey("proteins.id", ondelete="CASCADE"), nullable=False)
    confidence_score = db.Column(db.Float)  
    docking_score = db.Column(db.Float)
    mechanism_of_action = db.Column(db.Text)
    predicted_at = db.Column(db.DateTime, default=datetime.utcnow)

    search = db.relationship("SearchHistory", backref=db.backref("predictions", cascade="all, delete-orphan"))
    drug = db.relationship("Drug")
    disease = db.relationship("Disease")
    protein = db.relationship("Protein")