from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database
accounts = {
    "user1": {"balance": 1000},
    "user2": {"balance": 2000}
}

@app.route('/balance/<user_id>', methods=['GET'])
def get_balance(user_id):
    if user_id in accounts:
        return jsonify({"user_id": user_id, "balance": accounts[user_id]["balance"]})
    return jsonify({"error": "Account not found"}), 404

@app.route('/update_balance', methods=['POST'])
def update_balance():
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    if user_id in accounts:
        accounts[user_id]["balance"] += amount
        return jsonify({"message": "Balance updated", "user_id": user_id, "new_balance": accounts[user_id]["balance"]})
    return jsonify({"error": "Account not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
