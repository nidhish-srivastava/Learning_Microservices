from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['appointment_db']
appointments_collection = db['appointments']

# Patient Service URL (Change the URL based on where the Patient Service is hosted)
PATIENT_SERVICE_URL = "http://localhost:5000/patients"

@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    patient_id = data['patient_id']
    date = data['date']
    time = data['time']
    doctor = data['doctor']
    
    # Validate patient details by calling Patient Service
    response = requests.get(f"{PATIENT_SERVICE_URL}/{patient_id}")
    
    if response.status_code != 200:
        return jsonify({"error": "Invalid patient ID"}), 400
    
    # If patient is valid, save appointment to the database
    appointment = {
        'patient_id': patient_id,
        'date': date,
        'time': time,
        'doctor': doctor
    }
    result = appointments_collection.insert_one(appointment)
    return jsonify({"message": "Appointment created successfully", "id": str(result.inserted_id)}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = []
    for appointment in appointments_collection.find():
        appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string for JSON response
        appointments.append(appointment)
    return jsonify(appointments)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
