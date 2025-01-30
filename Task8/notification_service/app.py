from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    print(f"Notification for {user_id}: {message}")
    return jsonify({"message": "Notification sent"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
