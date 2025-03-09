import os
import pickle
import re
from datetime import datetime
import pandas as pd  # for reading Excel/CSV files

from flask import Flask, request, jsonify
from flask.json.provider import DefaultJSONProvider
from bson import ObjectId
from pymongo import MongoClient
from scipy.sparse import csr_matrix


# Custom JSON provider to handle ObjectId serialization
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


app = Flask(__name__)
app.json_provider_class = CustomJSONProvider
app.json = app.json_provider_class(app)

# Load baseline limits from Excel file
LIMITS_FILE = "compliance_dataset.xlsx"
try:
    limits_df = pd.read_excel(LIMITS_FILE)
    # Assuming one row with baseline limits; convert it to a dictionary.
    baseline_limits = limits_df.iloc[0].to_dict()
    print("Baseline limits loaded:", baseline_limits)
except Exception as e:
    print(f"Failed to load baseline limits from {LIMITS_FILE}: {e}")
    baseline_limits = {}

# Load trained model and vectorizer
MODEL_PATH = "models/compliance_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(
        "Model or vectorizer file missing. Ensure both pickle files exist."
    )

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Configure MongoDB connection
try:
    client = MongoClient("mongodb://localhost:27017/")
    client.admin.command("ping")
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise e

db = client.CompliAI
hsCodesCollection = db["hscodes"]
complianceReportCollection = db["complianceChecks"]

# Banned products and countries
BANNED_PRODUCTS = {
    "Tiger Skin",
    "Ivory",
    "Snake Venom",
    "Peacock Feathers",
    "Opium",
    "Cocaine",
    "Heroin",
    "Red Sandalwood",
    "Indian Currency (in bulk)",
    "Certain E-waste",
    "Antiques over 100 years old",
    "Organs",
    "Tissues",
    "Blood",
    "Bones",
    "Methylamine",
    "Red Phosphorus",
    "Acetic Anhydride",
    "Old laptops",
    "batteries",
}

BANNED_COUNTRIES = {"North Korea", "Pakistan", "Iran", "China"}

# Compliance Requirements (Base Requirements by Category)
REQUIRED_DOCUMENTS = {
    "Electronics": [
        "Technical Specifications",
        "User Manual",
        "RoHS Compliance Document",
    ],
    "Pharmaceuticals": [
        "FDA Approval",
        "Clinical Trial Results",
        "Product Safety Data Sheet (SDS)",
    ],
    "Machinery": [
        "Safety Certificate",
        "Inspection Report",
        "CE Declaration of Conformity",
    ],
    "Automotive": ["Emission Test Report", "Vehicle Safety Inspection Report"],
    "Construction": ["Building Permit", "Environmental Impact Assessment"],
    "Food & Beverage": [
        "Health Safety Certification",
        "FDA Food Facility Registration",
    ],
    "Energy & Utilities": [
        "Energy Efficiency Report",
        "Environmental Compliance Certificate",
    ],
    "Medical Devices": [
        "ISO 13485 Compliance Report",
        "Product Registration Certificate",
    ],
    "Textiles & Apparel": ["Chemical Safety Report", "Material Compliance Certificate"],
}

REQUIRED_APPROVALS = {
    "Electronics": ["FCC Approval", "CE Marking Approval"],
    "Pharmaceuticals": [
        "FDA Drug Approval",
        "EMA (European Medicines Agency) Approval",
    ],
    "Machinery": ["OSHA Safety Approval", "EPA Emissions Compliance"],
    "Automotive": [
        "NHTSA (National Highway Traffic Safety Administration) Approval",
        "DOT (Department of Transportation) Approval",
    ],
    "Construction": [
        "Local Government Building Permit Approval",
        "Fire Safety Compliance Approval",
    ],
    "Food & Beverage": [
        "USDA (United States Department of Agriculture) Approval",
        "FDA Labeling Compliance Approval",
    ],
    "Energy & Utilities": [
        "Federal Energy Regulatory Commission (FERC) Approval",
        "EPA Environmental Compliance Approval",
    ],
    "Medical Devices": [
        "FDA 510(k) Clearance",
        "EU MDR (Medical Device Regulation) Approval",
    ],
    "Textiles & Apparel": [
        "Oeko-Tex Certification Approval",
        "REACH Compliance Approval",
    ],
}

REQUIRED_CERTIFICATIONS = {
    "Electronics": [
        "ISO 9001 (Quality Management)",
        "UL (Underwriters Laboratories) Certification",
    ],
    "Pharmaceuticals": [
        "GMP (Good Manufacturing Practices)",
        "ISO 22716 (Cosmetic GMP)",
    ],
    "Machinery": [
        "ISO 45001 (Occupational Health & Safety)",
        "CE (Conformité Européenne) Certification",
    ],
    "Automotive": ["ISO 26262 (Functional Safety)", "SAE J3061 (Cybersecurity)"],
    "Construction": [
        "LEED (Leadership in Energy & Environmental Design) Certification",
        "ISO 14001 (Environmental Management)",
    ],
    "Food & Beverage": [
        "HACCP (Hazard Analysis and Critical Control Points)",
        "ISO 22000 (Food Safety)",
    ],
    "Energy & Utilities": ["ISO 50001 (Energy Management)", "LEED Certification"],
    "Medical Devices": [
        "ISO 13485 (Medical Device Quality)",
        "FDA cGMP (Current Good Manufacturing Practice)",
    ],
    "Textiles & Apparel": [
        "GOTS (Global Organic Textile Standard)",
        "Fair Trade Certification",
    ],
}


def check_compliance_for_payload(data: dict) -> dict:
    """
    Process a payload (dictionary) to perform compliance check.
    Returns a dictionary with compliance result.
    """
    reasons = []

    # --- HS Code Check ---
    hscode = data.get("hscode", "")
    if not hscode:
        reasons.append("HS code is missing.")
    else:
        hs_entry = hsCodesCollection.find_one({"hscode": hscode})
        if not hs_entry:
            reasons.append(f"HS code {hscode} not found in records.")

    # --- Extract additional compulsory fields ---
    item_name = data.get("item_name", "").strip()
    if not item_name:
        reasons.append("Item name is missing.")

    courier = data.get("courier", "").strip()
    if not courier:
        reasons.append("Courier information is missing.")

    # --- Use baseline limits from Excel ---
    min_weight = float(baseline_limits.get("min_weight", 0))
    max_weight = float(baseline_limits.get("max_weight", float("inf")))
    min_length = float(baseline_limits.get("min_length", 0))
    max_length = float(baseline_limits.get("max_length", float("inf")))
    min_breadth = float(baseline_limits.get("min_breadth", 0))
    max_breadth = float(baseline_limits.get("max_breadth", float("inf")))
    min_height = float(baseline_limits.get("min_height", 0))
    max_height = float(baseline_limits.get("max_height", float("inf")))

    # --- Extract user provided input ---
    input_text = data.get("input_text", "").strip()
    weight = float(data.get("weight", 0) or 0)
    length = float(data.get("length", 0) or 0)
    breadth = float(data.get("breadth", 0) or 0)
    height = float(data.get("height", 0) or 0)
    origin_country = data.get("OriginCountry", "").strip()
    declared_value = float(data.get("declared_value", 0) or 0)

    # --- Validate dimensions against baseline limits ---
    if not (min_weight <= weight <= max_weight):
        reasons.append("Weight is out of allowed range.")
    if not (min_length <= length <= max_length):
        reasons.append("Length is out of allowed range.")
    if not (min_breadth <= breadth <= max_breadth):
        reasons.append("Breadth is out of allowed range.")
    if not (min_height <= height <= max_height):
        reasons.append("Height is out of allowed range.")
    if not origin_country:
        reasons.append("Origin country is missing.")
    if not declared_value:
        reasons.append("Declared value is missing.")
    if not input_text:
        reasons.append("Product description is missing.")

    # --- Check for banned products ---
    banned_detected = {
        item for item in BANNED_PRODUCTS if item.lower() in input_text.lower()
    }
    reasons.extend([f"{item} is prohibited." for item in banned_detected])

    # --- Check for banned countries ---
    if origin_country in BANNED_COUNTRIES:
        reasons.append(f"Import from {origin_country} is restricted.")

    # --- Category detection ---
    input_lower = input_text.lower()
    if "electronics" in input_lower:
        category = "Electronics"
    elif any(word in input_lower for word in ["medicine", "drug", "pharmaceutical"]):
        category = "Pharmaceuticals"
    elif "machine" in input_lower or "equipment" in input_lower:
        category = "Machinery"
    else:
        category = "Other"

    required_docs = REQUIRED_DOCUMENTS.get(category, [])
    required_approvals = REQUIRED_APPROVALS.get(category, [])
    required_certifications = REQUIRED_CERTIFICATIONS.get(category, [])

    # --- Check declared value thresholds and add required documents ---
    # Thresholds (in INR):
    # > 1 Lakh: Self-declaration
    # > 25 Lakh: Bank Realization Certificate (BRC), Letter of Credit (if applicable)
    # > 1 Crore: Customs Valuation Certificate, CA Certificate
    if declared_value > 100000:
        required_docs = required_docs.copy()
        required_docs.append("Self-declaration")
        reasons.append("Declared value exceeds 1 Lakh INR: Self-declaration required.")
    if declared_value > 2500000:
        required_docs.append("Bank Realization Certificate (BRC)")
        required_docs.append("Letter of Credit (if applicable)")
        reasons.append(
            "Declared value exceeds 25 Lakh INR: BRC and Letter of Credit required."
        )
    if declared_value > 10000000:
        required_docs.append("Customs Valuation Certificate")
        required_docs.append("CA Certificate")
        reasons.append(
            "Declared value exceeds 1 Crore INR: Customs Valuation Certificate and CA Certificate required."
        )

    # --- Append a general message if any category-based docs exist ---
    if required_docs or required_approvals or required_certifications:
        reasons.append("Product requires additional documents or approvals.")

    # --- Vectorize input text and predict compliance ---
    input_vector = vectorizer.transform([input_text])
    if not isinstance(input_vector, csr_matrix):
        reasons.append("Error in vectorization. Check the TF-IDF model.")
    else:
        prediction = model.predict(input_vector)
        if prediction[0] == 0:
            reasons.append("Product description does not meet compliance standards.")

    compliance_status = "Compliant" if not reasons else "Flagged"

    result = {
        "hscode": hscode,
        "item_name": item_name,
        "courier": courier,
        "input_text": input_text,
        "weight": weight,
        "length": length,
        "breadth": breadth,
        "height": height,
        "OriginCountry": origin_country,
        "declared_value": declared_value,
        "status": compliance_status,
        "reasons": reasons,
        "required_documents": required_docs,
        "required_approvals": required_approvals,
        "required_certifications": required_certifications,
        "timestamp": datetime.now().isoformat(),
    }
    return result


@app.route("/api/compliance-check", methods=["POST"])
def compliance_check():
    try:
        data = request.json
        result = check_compliance_for_payload(data)
        # Store the result in MongoDB
        db_result = complianceReportCollection.insert_one(result)
        result["_id"] = db_result.inserted_id
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/compliance-check-file", methods=["POST"])
def compliance_check_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Determine file type by extension
        filename = file.filename.lower()
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)
        else:
            return (
                jsonify(
                    {"error": "Unsupported file format. Upload CSV or Excel file."}
                ),
                400,
            )

        results = []
        # Process each row as a compliance payload
        for _, row in df.iterrows():
            payload = row.to_dict()
            result = check_compliance_for_payload(payload)
            db_result = complianceReportCollection.insert_one(result)
            result["_id"] = db_result.inserted_id
            results.append(result)

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# New route to fetch all compliance reports
@app.route("/api/compliance-reports", methods=["GET"])
def get_all_reports():
    try:
        reports = list(complianceReportCollection.find())
        return jsonify(reports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/suggest", methods=["GET"])
def suggest_items():
    try:
        hscode = request.args.get("hscode")
        description = request.args.get("description")

        if hscode:
            item = hsCodesCollection.find_one({"hscode": hscode})
            if item:
                related_items = list(
                    hsCodesCollection.find({"parent": item["parent"]}, {"_id": 0})
                )
                return jsonify({"related_items": related_items})
            return jsonify({"error": "HS Code not found"}), 404
        elif description:
            regex_pattern = re.compile(description, re.IGNORECASE)
            related_items = list(
                hsCodesCollection.find({"description": regex_pattern}, {"_id": 0})
            )
            if related_items:
                return jsonify({"related_items": related_items})
            return jsonify({"error": "No matching descriptions found"}), 404

        return jsonify({"error": "Provide either hscode or description"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
