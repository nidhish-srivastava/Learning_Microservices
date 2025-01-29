from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['patient_db']
patients_collection = db['patients']

@app.route('/patients',methods = ['POST'])
def add_patient():
    data = request.json
    name = data['name']
    dob = data['dob']
    email = data['email']

    patient = {
        "name": name,
        "dob" : dob,
        "email" : email
    }
    result = patients_collection.insert_one(patient)
    return jsonify({"message": "Patient added successfully", "id": str(result.inserted_id)}), 201

@app.route('/patients/<string:id>',methods=['GET'])
def get_patient(id):
    patient = patients_collection.find_one({"_id" : ObjectId(id)})

    if not patient:
        return jsonify({"error" : "Patient not found"}),404
    
    patient['_id'] = str(patient['_id'])  # Convert ObjectId to string for JSON response
    return jsonify(patient)

if __name__ == '__main__':
    app.run(debug=True, port=5000)