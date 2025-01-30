import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ACCOUNT_SERVICE_URL = "http://account_service:5001"
NOTIFICATION_SERVICE_URL = "http://notification_service:5003"

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = data.get("amount")

    # Check sender balance
    sender_balance_response = requests.get(f"{ACCOUNT_SERVICE_URL}/balance/{sender}")
    if sender_balance_response.status_code != 200:
        return jsonify({"error": "Sender account not found"}), 404

    sender_balance = sender_balance_response.json()["balance"]
    if sender_balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    # Deduct amount from sender
    requests.post(f"{ACCOUNT_SERVICE_URL}/update_balance", json={"user_id": sender, "amount": -amount})

    # Add amount to receiver
    requests.post(f"{ACCOUNT_SERVICE_URL}/update_balance", json={"user_id": receiver, "amount": amount})

    # Notify users
    requests.post(f"{NOTIFICATION_SERVICE_URL}/notify", json={"user_id": sender, "message": f"Sent ${amount} to {receiver}"})
    requests.post(f"{NOTIFICATION_SERVICE_URL}/notify", json={"user_id": receiver, "message": f"Received ${amount} from {sender}"})

    return jsonify({"message": "Transaction successful"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
